#!/bin/bash
# Health check script for NovaHouse Chatbot
# Usage: ./health_check.sh [url]

set -e

URL="${1:-https://glass-core-467907-e9.ey.r.appspot.com}"

echo "🏥 Health Check: $URL"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Health endpoint
echo "1️⃣  Checking /api/health..."
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "${URL}/api/health")
HEALTH_BODY=$(echo "$HEALTH_RESPONSE" | sed '$d')
HEALTH_CODE=$(echo "$HEALTH_RESPONSE" | tail -n 1)

if [ "$HEALTH_CODE" -eq 200 ]; then
    echo -e "${GREEN}✅ Health check passed ($HEALTH_CODE)${NC}"
    echo "$HEALTH_BODY" | jq '.' 2>/dev/null || echo "$HEALTH_BODY"
else
    echo -e "${RED}❌ Health check failed ($HEALTH_CODE)${NC}"
    exit 1
fi

echo ""

# Test chat endpoint
echo "2️⃣  Checking /api/chat..."
CHAT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${URL}/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"message":"test"}')
CHAT_CODE=$(echo "$CHAT_RESPONSE" | tail -n 1)

if [ "$CHAT_CODE" -eq 200 ]; then
    echo -e "${GREEN}✅ Chat endpoint working ($CHAT_CODE)${NC}"
else
    echo -e "${YELLOW}⚠️  Chat endpoint returned $CHAT_CODE${NC}"
fi

echo ""

# Test knowledge endpoints
echo "3️⃣  Checking knowledge endpoints..."
for endpoint in "packages" "faq" "portfolio"; do
    RESP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${URL}/api/${endpoint}")
    if [ "$RESP_CODE" -eq 200 ]; then
        echo -e "${GREEN}✅ /${endpoint} OK${NC}"
    else
        echo -e "${RED}❌ /${endpoint} failed ($RESP_CODE)${NC}"
    fi
done

echo ""
echo -e "${GREEN}🎉 Health check complete!${NC}"
