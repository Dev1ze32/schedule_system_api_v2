"""
image_parser.py
---------------
Wraps TableLinesRemover + ScheduleDataExtractor into a single
process_image(path) function that returns:

    [{'day': 'Monday', 'event': 'CPP106', 'start': '07:00', 'end': '10:00'}, …]

Changes vs previous image_parser.py
--------------------------------------
1. TableLinesRemover  — synced with user's latest version (color families, etc.)
2. ScheduleDataExtractor.__init__  — synced with user's latest version
3. clean_text()  — 4-pass pipeline:
     Pass 0: strip tesseract noise warnings  ("Image small to scale …")
     Pass 1: fuzzy-match full string to known hour labels  (cutoff 0.45)
     Pass 2: token-level OCR corrections  (course codes, section separators)
     Pass 3: second fuzzy pass + quality score gate
4. extract_data()  — returns list; garbage events become event='N/A' so the
                     time slot is preserved and faculty can fix it on the site
5. process_image()  — public entry-point used by upload_service.py
"""

import cv2
import numpy as np
import os
import re
import subprocess
import difflib

# ─────────────────────────────────────────────────────────────────────────────
# Known non-class activity labels
# ─────────────────────────────────────────────────────────────────────────────
_KNOWN_PHRASES = [
    "Administrative Hours",
    "Consultation Hours",
    "Research Hours",
    "Community Extension Hours",
    "Break",
    "Quasi Hours",
    "Lunch",
]

# Tesseract internal warning that gets injected when a crop is too small
_TESSERACT_NOISE_RE = re.compile(
    r'(?i)(image\s+small\s+to\s+scale\s+\S+\s+width\s+\d+\s+line\s+cannot\s+recognized\s*)+',
    re.IGNORECASE,
)


# ─────────────────────────────────────────────────────────────────────────────
# Garbage-detection helpers
# ─────────────────────────────────────────────────────────────────────────────

def _strip_tesseract_noise(text: str) -> str:
    cleaned = _TESSERACT_NOISE_RE.sub('', text).strip()
    return re.sub(r'\s+', ' ', cleaned).strip()


def _has_tesseract_noise(text: str) -> bool:
    return bool(_TESSERACT_NOISE_RE.search(text))


def _score_event_quality(text: str) -> float:
    """
    Returns 0.0–1.0.  Threshold = 0.35.
      ≥ 0.35  → probably real data  (keep)
      < 0.35  → probably garbage    (return '' so caller stores N/A)

    Positive signals
      course code pattern  (CPP106, PSM113 …)  +0.50
      section pattern      (2CPEA, 3PSY-D …)   +0.30
      room token           (RM319 …)            +0.20
      known hour phrase    (fuzzy 0.45)         +0.60

    Negative signals
      > 8 tokens                                -0.40
      > 50 % of tokens are ≤ 2 chars           -0.30
    """
    if not text or len(text.strip()) < 3:
        return 0.0

    tokens = text.split()

    has_course  = bool(re.search(r'\b[A-Z]{2,}[A-Z0-9]\d{2,}\b', text))
    has_section = bool(re.search(r'\b\d[A-Z]{2,}[-]?[A-Z]?\b', text))
    has_room    = bool(re.search(r'\bRM\d+\b', text, re.I))
    is_known    = bool(difflib.get_close_matches(text, _KNOWN_PHRASES, n=1, cutoff=0.45))

    too_long     = len(tokens) > 8
    mostly_short = (sum(1 for t in tokens if len(t) <= 2) / max(len(tokens), 1)) > 0.50

    score = 0.0
    if has_course:   score += 0.50
    if has_section:  score += 0.30
    if has_room:     score += 0.20
    if is_known:     score += 0.60
    if too_long:     score -= 0.40
    if mostly_short: score -= 0.30

    return max(0.0, min(1.0, score))


# ─────────────────────────────────────────────────────────────────────────────
# PART 1: Image cleanup
# ─────────────────────────────────────────────────────────────────────────────

class TableLinesRemover:

    def __init__(self, image):
        self.image    = image.copy()
        self.original = image.copy()

    def execute(self):
        self.isolate_color_blocks()
        self.grayscale_image()
        self.threshold_image()
        self.invert_image()
        self.erode_vertical_lines()
        self.erode_horizontal_lines()
        self.combine_eroded_images()
        self.erase_lines_from_original()
        self.restore_color_blocks()
        self.crop_to_largest_table()
        return self.final_image

    def _make_solid_color_mask(self, hsv, min_area=200):
        raw = cv2.inRange(hsv, np.array([0, 30, 30]), np.array([180, 255, 255]))
        contours, _ = cv2.findContours(raw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        solid = np.zeros_like(raw)
        for cnt in contours:
            if cv2.contourArea(cnt) > min_area:
                cv2.drawContours(solid, [cnt], -1, 255, -1)
        return solid

    def isolate_color_blocks(self):
        hsv = cv2.cvtColor(self.original, cv2.COLOR_BGR2HSV)
        self.solid_color_mask = self._make_solid_color_mask(hsv)
        self.isolated_colors  = cv2.bitwise_and(
            self.original, self.original, mask=self.solid_color_mask
        )

    def grayscale_image(self):
        self.grey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def threshold_image(self):
        self.thresholded_image = cv2.threshold(self.grey, 150, 255, cv2.THRESH_BINARY)[1]

    def invert_image(self):
        self.inverted_image = cv2.bitwise_not(self.thresholded_image)

    def erode_vertical_lines(self):
        ver = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        self.vertical_lines = cv2.erode(self.inverted_image, ver, iterations=1)
        self.vertical_lines = cv2.dilate(self.vertical_lines, ver, iterations=1)

    def erode_horizontal_lines(self):
        hor = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        self.horizontal_lines = cv2.erode(self.inverted_image, hor, iterations=1)
        self.horizontal_lines = cv2.dilate(self.horizontal_lines, hor, iterations=1)

    def combine_eroded_images(self):
        self.combined_lines = cv2.add(self.vertical_lines, self.horizontal_lines)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        self.combined_lines = cv2.dilate(self.combined_lines, kernel, iterations=1)

    def erase_lines_from_original(self):
        self.image_without_lines = self.original.copy()
        self.image_without_lines[self.combined_lines == 255] = [255, 255, 255]

    def restore_color_blocks(self):
        inv_color_mask = cv2.bitwise_not(self.solid_color_mask)
        bg_area        = cv2.bitwise_and(
            self.image_without_lines, self.image_without_lines, mask=inv_color_mask
        )
        self.final_image = cv2.add(bg_area, self.isolated_colors)

    def crop_to_largest_table(self):
        kernel       = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        closed_lines = cv2.morphologyEx(self.combined_lines, cv2.MORPH_CLOSE, kernel)
        contours, _  = cv2.findContours(closed_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        best_box = None
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w * h > max_area:
                max_area = w * h
                best_box = (x, y, w, h)

        if best_box is not None:
            x, y, w, h = best_box
            p  = -5
            self.final_image = self.final_image[
                max(0, y - p) : min(self.final_image.shape[0], y + h + p),
                max(0, x - p) : min(self.final_image.shape[1], x + w + p),
            ]


# ─────────────────────────────────────────────────────────────────────────────
# PART 2: OCR & geometric extraction
# ─────────────────────────────────────────────────────────────────────────────

class ScheduleDataExtractor:

    def __init__(self, cropped_image, work_dir="/tmp/ocr_crops"):
        self.image    = cropped_image
        self.img_h, self.img_w = self.image.shape[:2]
        self.work_dir = work_dir
        os.makedirs(work_dir, exist_ok=True)

        hsv       = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        gray_full = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        self.color_families = [
            cv2.inRange(hsv, np.array([35,  40,  20]), np.array([85,  255, 200])),  # Dark Green
            cv2.inRange(hsv, np.array([90,  40,  40]), np.array([130, 255, 255])),  # Blue
            cv2.bitwise_or(                                                          # Red/Peach
                cv2.inRange(hsv, np.array([0,   40, 100]), np.array([15,  255, 255])),
                cv2.inRange(hsv, np.array([160, 40, 100]), np.array([180, 255, 255])),
            ),
            cv2.inRange(hsv, np.array([15,  20, 150]), np.array([35,  255, 255])),  # Yellow/Beige
        ]

        self.color_mask = np.zeros(self.image.shape[:2], dtype=np.uint8)
        ink_in_color    = np.zeros(self.image.shape[:2], dtype=np.uint8)

        for i, fam_mask in enumerate(self.color_families):
            ck       = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            fam_mask = cv2.morphologyEx(fam_mask, cv2.MORPH_CLOSE, ck)
            self.color_mask = cv2.bitwise_or(self.color_mask, fam_mask)

            if i == 0:
                smooth = cv2.medianBlur(gray_full, 3)
                _, thresh = cv2.threshold(smooth, 40, 255, cv2.THRESH_BINARY_INV)
                min_area, min_h = 5, 6
            elif i == 1:
                smooth = cv2.bilateralFilter(cv2.medianBlur(gray_full, 5), 9, 75, 75)
                thresh = cv2.adaptiveThreshold(
                    smooth, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 14
                )
                min_area, min_h = 15, 6
            else:
                smooth = cv2.medianBlur(gray_full, 5)
                thresh = cv2.adaptiveThreshold(
                    smooth, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 8
                )
                min_area, min_h = 12, 6

            raw_ink    = cv2.bitwise_and(thresh, thresh, mask=fam_mask)
            family_ink = np.zeros(self.image.shape[:2], dtype=np.uint8)
            n, labels, stats, _ = cv2.connectedComponentsWithStats(raw_ink, connectivity=8)
            for lbl in range(1, n):
                if stats[lbl, cv2.CC_STAT_AREA] >= min_area and stats[lbl, cv2.CC_STAT_HEIGHT] >= min_h:
                    family_ink[labels == lbl] = 255

            ink_in_color = cv2.bitwise_or(ink_in_color, family_ink)

        _, bw_outside     = cv2.threshold(gray_full, 150, 255, cv2.THRESH_BINARY_INV)
        bw_outside_masked = cv2.bitwise_and(
            bw_outside, bw_outside, mask=cv2.bitwise_not(self.color_mask)
        )
        nk      = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        bw_open = cv2.morphologyEx(bw_outside_masked, cv2.MORPH_OPEN, nk, iterations=1)

        self.ocr_mask             = cv2.bitwise_or(bw_open, ink_in_color)
        self.bw_image_for_viewing = cv2.bitwise_not(self.ocr_mask)

    # ── helpers ──────────────────────────────────────────────────────────────

    def generate_time_slots(self):
        times  = []
        hour   = 6
        minute = 0
        while hour < 21:
            start = f"{hour:02d}:{minute:02d}"
            minute += 30
            if minute == 60:
                minute = 0
                hour  += 1
            times.append((start, f"{hour:02d}:{minute:02d}"))
        return times

    def ocr_crop(self, box, index):
        x, y, w, h = box
        pad  = 4
        x1   = max(0, x - pad);  y1 = max(0, y - pad)
        x2   = min(self.img_w, x + w + pad);  y2 = min(self.img_h, y + h + pad)

        crop    = self.ocr_mask[y1:y2, x1:x2]
        inv     = cv2.bitwise_not(crop)
        min_dim = min(inv.shape[1], inv.shape[0])
        scale   = 4.0 if min_dim < 30 else 3.0
        inv     = cv2.resize(inv, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        psm  = 7 if (h < 20 or w < 60) else 6
        path = os.path.join(self.work_dir, f"crop_{index}.jpg")
        cv2.imwrite(path, inv)

        out = subprocess.getoutput(f'tesseract "{path}" stdout --psm {psm}')
        return " ".join(out.strip().split())

    def clean_text(self, text: str) -> str:
        """
        4-pass cleaning pipeline.
        Returns '' when text is unrecoverable garbage
        (caller stores event='N/A' but keeps the time slot).
        """
        # Pass 0: remove tesseract internal warnings, check what survives
        if _has_tesseract_noise(text):
            text = _strip_tesseract_noise(text)
            if not text:
                return ''

        cleaned = re.sub(r'[^A-Za-z0-9\-\s]', ' ', text)
        compact = re.sub(r'\s+', ' ', cleaned).strip()
        if not compact:
            return ''

        # Pass 1: fuzzy match against known hour labels (generous cutoff)
        m = difflib.get_close_matches(compact, _KNOWN_PHRASES, n=1, cutoff=0.45)
        if m:
            return m[0]

        # Pass 2: token-level OCR corrections
        known_prefixes = ['PSM', 'PSE', 'CPP', 'RM', 'PSY', 'NSTP', 'CHM', 'BCH']
        final_words = []
        for word in compact.split():
            # Fix known-prefix tokens
            matched_pfx = None
            for pfx in known_prefixes:
                if word.upper().startswith(pfx) or (
                    len(word) >= 3 and
                    difflib.SequenceMatcher(None, word[:len(pfx)].upper(), pfx).ratio() > 0.70
                ):
                    matched_pfx = pfx
                    break

            if matched_pfx and len(word) >= 4:
                suffix = word[len(matched_pfx):]
                for a, b in [('O','0'),('o','0'),('I','1'),('i','1'),('l','1'),('G','6'),('S','5')]:
                    suffix = suffix.replace(a, b)
                word = matched_pfx + suffix

            # Fix section separators
            if '-' in word:
                parts = word.split('-')
                if len(parts) == 2:
                    if parts[0] and parts[0][0] in 'iIlL':
                        parts[0] = '1' + parts[0][1:]
                    if parts[1] in ('8', 'b'):
                        parts[1] = 'B'
                    if parts[1] in ('0', 'o'):
                        parts[1] = 'D'
                    word = '-'.join(parts)

            # Drop pure noise tokens
            if len(word) <= 3 and word.islower() and word not in ('a', 'to', 'am', 'pm'):
                continue
            if re.fullmatch(r'[^A-Za-z0-9]+', word):
                continue

            final_words.append(word)

        final_string = ' '.join(final_words)
        if not final_string:
            return ''

        # Pass 3: second fuzzy pass after corrections
        m2 = difflib.get_close_matches(final_string, _KNOWN_PHRASES, n=1, cutoff=0.50)
        if m2:
            return m2[0]

        # Pass 4: quality gate — garbage → empty string
        if _score_event_quality(final_string) < 0.35:
            return ''

        return final_string

    # ── box categorisation ────────────────────────────────────────────────────

    def categorize_boxes(self):
        self.time_boxes  = []
        self.day_boxes   = []
        self.event_boxes = []

        tcw = int(self.img_w * 0.18)   # time-column width
        hrh = int(self.img_h * 0.10)   # header-row height

        # Colored event blocks
        ck = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        for fm in self.color_families:
            opened      = cv2.morphologyEx(fm, cv2.MORPH_OPEN, ck)
            cnts, _     = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in cnts:
                x, y, w, h = cv2.boundingRect(cnt)
                if w > 20 and h > 20:
                    p = 4
                    self.event_boxes.append((x - p, y - p, w + p * 2, h + p * 2))

        # Time slots (left zone)
        tz = self.ocr_mask.copy();  tz[:, tcw:] = 0
        td = cv2.dilate(tz, cv2.getStructuringElement(cv2.MORPH_RECT, (15, 2)), iterations=1)
        for cnt in cv2.findContours(td, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 10 and h > 5 and y > hrh:
                self.time_boxes.append((x, y, w, h))

        # Day headers (top zone)
        dz = self.ocr_mask.copy();  dz[hrh:, :] = 0;  dz[:, :tcw] = 0
        dd = cv2.dilate(dz, cv2.getStructuringElement(cv2.MORPH_RECT, (20, 5)), iterations=1)
        for cnt in cv2.findContours(dd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
            x, y, w, h = cv2.boundingRect(cnt)
            if w > 40 and h > 10:
                self.day_boxes.append((x, y, w, h))

        # Floating text (white background)
        ez = self.ocr_mask.copy();  ez[:hrh, :] = 0;  ez[:, :tcw] = 0
        ed = cv2.dilate(ez, cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5)), iterations=1)
        floating = []
        for cnt in cv2.findContours(ed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]:
            x, y, w, h = cv2.boundingRect(cnt)
            if w < 10 or h < 10:
                continue
            cx, cy = x + w // 2, y + h // 2
            if not any(gx <= cx <= gx + gw and gy <= cy <= gy + gh
                       for (gx, gy, gw, gh) in self.event_boxes):
                floating.append([x, y, w, h])

        # Smart vertical merge
        merged_any = True
        while merged_any:
            merged_any = False
            for i in range(len(floating)):
                for j in range(i + 1, len(floating)):
                    b1, b2 = floating[i], floating[j]
                    xo = max(0, min(b1[0]+b1[2], b2[0]+b2[2]) - max(b1[0], b2[0]))
                    mw = min(b1[2], b2[2])
                    if mw > 0 and (xo / mw) > 0.5:
                        yd = max(b1[1], b2[1]) - min(b1[1]+b1[3], b2[1]+b2[3])
                        if -10 <= yd <= 30:
                            nx = min(b1[0], b2[0]);  ny = min(b1[1], b2[1])
                            nw = max(b1[0]+b1[2], b2[0]+b2[2]) - nx
                            nh = max(b1[1]+b1[3], b2[1]+b2[3]) - ny
                            floating[i] = [nx, ny, nw, nh]
                            del floating[j]
                            merged_any = True
                            break
                if merged_any:
                    break

        for box in floating:
            self.event_boxes.append(tuple(box))

    # ── main extraction (returns list) ───────────────────────────────────────

    def extract_data(self) -> list:
        """
        Run full extraction.  Returns list of dicts: {day, event, start, end}.

        Garbage events are NOT dropped — they are kept with event='N/A'
        so the time slot is preserved and faculty can correct them on the site.
        """
        self.categorize_boxes()
        time_slots = self.generate_time_slots()

        self.days = []
        for i, box in enumerate(self.day_boxes):
            text = self.ocr_crop(box, f"day_{i}")
            if len(text) >= 3:
                self.days.append({
                    'text':     text,
                    'center_x': box[0] + box[2] // 2,
                    'bottom_y': box[1] + box[3],
                })

        if not self.days:
            return []

        grid_top    = sum(d['bottom_y'] for d in self.days) / len(self.days)
        row_height  = (self.img_h - grid_top) / len(time_slots)

        results = []
        for i, (x, y, w, h) in enumerate(self.event_boxes):
            # Time mapping
            si = max(0, min(int(round((y - grid_top) / row_height)),         len(time_slots) - 1))
            ei = max(si + 1, min(int(round((y + h - grid_top) / row_height)), len(time_slots)))

            start_time = time_slots[si][0]
            end_time   = time_slots[ei - 1][1]

            # Day
            cx       = x + w // 2
            day_text = min(self.days, key=lambda d: abs(d['center_x'] - cx))['text']

            # OCR + clean
            raw  = self.ocr_crop((x, y, w, h), f"event_{i}")
            text = self.clean_text(raw)

            # Garbage → N/A (time is still valuable)
            if not text:
                text = 'N/A'

            results.append({'day': day_text, 'event': text, 'start': start_time, 'end': end_time})

        return results


# ─────────────────────────────────────────────────────────────────────────────
# Public entry-point
# ─────────────────────────────────────────────────────────────────────────────

def process_image(file_path: str) -> list:
    image = cv2.imread(file_path)
    if image is None:
        return []
    cleaned  = TableLinesRemover(image).execute()
    return ScheduleDataExtractor(cleaned).extract_data()


# ─────────────────────────────────────────────────────────────────────────────
# Standalone runner
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    src = sys.argv[1] if len(sys.argv) > 1 else "new_sched_1.jpg"
    img = cv2.imread(src)
    if img is None:
        print(f"Error: Could not load '{src}'.")
        sys.exit(1)

    os.makedirs("./process_images/table_lines_remover/", exist_ok=True)
    os.makedirs("./process_images/ocr_table_tool/",      exist_ok=True)

    remover  = TableLinesRemover(img)
    cleaned  = remover.execute()
    cv2.imwrite("schedule_final_colored.jpg", cleaned)
    print("Success! Cleaned color image saved as 'schedule_final_colored.jpg'")

    extractor = ScheduleDataExtractor(cleaned)
    cv2.imwrite("schedule_final_bw_mask.jpg", extractor.bw_image_for_viewing)
    print("Success! Black & White text mask saved as 'schedule_final_bw_mask.jpg'")

    day_order = {d: i for i, d in enumerate(
        ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    )}
    results = sorted(
        extractor.extract_data(),
        key=lambda r: (day_order.get(r['day'].lower(), 99), r['start'])
    )

    print("\n" + "=" * 50)
    print(" EXTRACTED SCHEDULE EVENTS")
    print("=" * 50)
    for b in results:
        print(f"DAY:   {b['day']}")
        print(f"TIME:  {b['start']} to {b['end']}")
        print(f"EVENT: {b['event']}")
        print("-" * 50)