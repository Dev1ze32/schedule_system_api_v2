from bleach import clean

def sanitize_input(text):
    """
    Sanitizes input text to prevent XSS or injection attacks.
    Used for text fields like Subject Codes.
    """
    if not text:
        return text
    return clean(text.strip())