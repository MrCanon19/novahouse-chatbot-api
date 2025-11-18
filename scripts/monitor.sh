#!/bin/bash
# Performance Monitoring Script
# Monitors API performance in real-time

set -e

URL="${1:-http://localhost:8080}"
INTERVAL="${2:-5}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Real-time Performance Monitor - NovaHouse Chatbot      ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Monitoring: $URL"
echo "Interval: ${INTERVAL}s"
echo "Press Ctrl+C to stop"
echo ""

# Function to get response time
get_response_time() {
    local endpoint=$1
    local start=$(date +%s%3N)
    local status=$(curl -s -o /dev/null -w "%{http_code}" "${URL}${endpoint}" 2>/dev/null)
    local end=$(date +%s%3N)
    local duration=$((end - start))
    
    echo "${status}|${duration}"
}

# Monitor loop
while true; do
    timestamp=$(date +"%H:%M:%S")
    
    # Health check
    result=$(get_response_time "/api/health")
    status=$(echo $result | cut -d'|' -f1)
    duration=$(echo $result | cut -d'|' -f2)
    
    if [ "$status" = "200" ]; then
        if [ $duration -lt 200 ]; then
            color=$GREEN
            status_text="✓ HEALTHY"
        elif [ $duration -lt 500 ]; then
            color=$YELLOW
            status_text="⚠ SLOW"
        else
            color=$RED
            status_text="⚠ VERY SLOW"
        fi
    else
        color=$RED
        status_text="✗ ERROR"
    fi
    
    echo -e "${timestamp} | ${color}${status_text}${NC} | Status: ${status} | Time: ${duration}ms"
    
    sleep $INTERVAL
done
