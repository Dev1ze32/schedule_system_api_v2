#!/bin/bash

LOGFILE="/home/raspi/Documents/labitigs/startup.log"
exec > >(tee -a "$LOGFILE") 2>&1

echo "========================================"
echo "STARTUP: $(date)"
echo "========================================"

PORTAL_DIR="/home/raspi/Documents/labitigs/faculty-scheduling-portal"
MAP_DIR="/home/raspi/Documents/labitigs/pnc-map"
API_DIR="/home/raspi/Documents/labitigs/schedule_system_api-main"
PORT_API=5000
PORT_WEB=5174

HOTSPOT_SSID="Group 19 Kiosk"
HOTSPOT_CON="kiosk-hotspot"
LOCAL_IP="10.42.0.1"

# --- STEP 1: Start Hotspot ---
echo "Setting up hotspot: '${HOTSPOT_SSID}'..."

# Delete existing connection to avoid duplicates on reboot
nmcli connection delete "$HOTSPOT_CON" 2>/dev/null || true

# Create open hotspot (no wifi-sec section = truly open network)
nmcli connection add \
    type wifi \
    ifname wlan0 \
    con-name "$HOTSPOT_CON" \
    autoconnect no \
    ssid "$HOTSPOT_SSID" \
    mode ap \
    ipv4.method shared \
    ipv4.addresses "${LOCAL_IP}/24"

# Bring it up
nmcli connection up "$HOTSPOT_CON"

# Wait until hotspot is confirmed active
echo "Waiting for hotspot to be active..."
for i in $(seq 1 15); do
    if nmcli connection show --active | grep -q "$HOTSPOT_CON"; then
        echo "Hotspot is active."
        break
    fi
    echo "Waiting... (${i})"
    sleep 2
done

if ! nmcli connection show --active | grep -q "$HOTSPOT_CON"; then
    echo "ERROR: Hotspot failed to start."
    exit 1
fi

echo "Hotspot '${HOTSPOT_SSID}' is live at ${LOCAL_IP} (open network)"

# --- STEP 2: Start Docker (API) ---
echo "Starting API via docker compose..."
cd "$API_DIR" && docker compose up -d
echo "Docker started."
sleep 5

# --- STEP 3: Update .env files ---
DOTENV_PORTAL="$PORTAL_DIR/.env"
if [ -f "$DOTENV_PORTAL" ]; then
    sed -i "s|VITE_API_URL=.*|VITE_API_URL=http://${LOCAL_IP}:${PORT_API}/api|g" "$DOTENV_PORTAL"
    sed -i "s|VITE_WEB_REDIRECT=.*|VITE_WEB_REDIRECT=http://${LOCAL_IP}:${PORT_WEB}/|g" "$DOTENV_PORTAL"
    echo "faculty-scheduling-portal .env updated:"
    grep "VITE_API_URL\|VITE_WEB_REDIRECT" "$DOTENV_PORTAL"
else
    echo "ERROR: .env not found at $DOTENV_PORTAL"
fi

DOTENV_MAP="$MAP_DIR/.env"
if [ -f "$DOTENV_MAP" ]; then
    sed -i "s|VITE_API_URL=.*|VITE_API_URL=http://${LOCAL_IP}:${PORT_API}/api|g" "$DOTENV_MAP"
    sed -i "s|VITE_FSP_URL=.*|VITE_FSP_URL=http://${LOCAL_IP}:5173|g" "$DOTENV_MAP"
    echo "pnc-map .env updated:"
    grep "VITE_API_URL\|VITE_FSP_URL" "$DOTENV_MAP"
else
    echo "ERROR: .env not found at $DOTENV_MAP"
fi

# --- STEP 4: Start faculty-scheduling-portal FIRST (gets port 5173) ---
echo "Starting faculty-scheduling-portal on port 5173..."
cd "$PORTAL_DIR" && nohup npm run dev -- --host --port 5173 > /tmp/faculty-portal.log 2>&1 &
echo "faculty-portal PID: $!"

# Small delay so it claims 5173 before pnc-map starts
sleep 3

# --- STEP 5: Start pnc-map SECOND (gets port 5174) ---
echo "Starting pnc-map on port 5174..."
cd "$MAP_DIR" && nohup npm run dev -- --host --port 5174 > /tmp/pnc-map.log 2>&1 &
echo "pnc-map PID: $!"

echo "========================================"
echo "ALL SERVICES STARTED"
echo "  Hotspot: '${HOTSPOT_SSID}' (open, no password)"
echo "  API:     http://${LOCAL_IP}:${PORT_API}/api"
echo "  Portal:  http://${LOCAL_IP}:5173  <-- MAIN"
echo "  Map:     http://${LOCAL_IP}:5174"
echo "========================================"