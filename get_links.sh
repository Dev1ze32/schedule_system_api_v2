#!/bin/bash

# --- CONFIGURATION ---
UTILS_DIR="/mnt/c/Users/HP-PAVILION/Documents/programming/faculty-scheduling-portal/src/utils"
DOTENV_PATH="./.env"

# --- NETWORK INFO ---
LOCAL_IP=$(hostname -I | awk '{print $1}')
PORT=5000
# The script will force this to be the active URL
LAN_URL="http://${LOCAL_IP}:${PORT}/api"

echo "------------------------------------------------"
echo "🔍 SCANNING FOR CLOUDFLARE & LAN INFO..."

# 1. Get the latest Tunnel URL
RAW_TUNNEL=$(docker logs cloudflared-tunnel 2>&1 | grep -o 'https://.*\.trycloudflare\.com' | tail -n 1)
TUNNEL_URL="${RAW_TUNNEL}/api"

if [ -z "$RAW_TUNNEL" ]; then
    echo "⚠️  WARNING: Cloudflare link not found."
    TUNNEL_URL="OFFLINE"
fi

echo "✅ TARGET LAN:  $LAN_URL"
echo "✅ CLOUDFLARE:  $TUNNEL_URL"
echo "------------------------------------------------"

# 2. UPDATE BACKEND (.env)
if [ -f "$DOTENV_PATH" ]; then
    sed -i "s|CLIENT_URL=.*|CLIENT_URL=$RAW_TUNNEL|g" "$DOTENV_PATH"
    echo "📝 Backend: Updated CORS origin in .env"
fi

# 3. UPDATE FRONTEND (The Fix)
echo "📝 Frontend: Updating API_BASE_URL in $UTILS_DIR..."

# Use a very specific regex to find the variable and replace the WHOLE line.
# This ensures LAN_URL is inside the quotes and TUNNEL_URL is just a comment.
find "$UTILS_DIR" -name "*.js" -type f -exec sed -i "s|^.*API_BASE_URL.*=.*|export const API_BASE_URL = \"$LAN_URL\"; // Cloudflare: $TUNNEL_URL|g" {} +

echo "✨ JS files updated. Default is now LAN ($LOCAL_IP)."

# 4. RESTART API
echo "🔄 Restarting API container..."
docker compose up -d --no-deps api

echo ""
echo "🚀 CAMPUSNAV READY"
echo "📍 Primary (LAN): $LAN_URL"
echo "------------------------------------------------"