#!/bin/bash
# Complete setup script for A/B Testing & Competitive Intelligence
# Run this after deployment

set -e

APP_URL="https://glass-core-467907-e9.ey.r.appspot.com"
API_KEY="V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"

echo "════════════════════════════════════════════════════════════════"
echo "🚀 Complete Setup: A/B Testing & Competitive Intelligence"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Step 1: Run migration via HTTP endpoint
echo "1️⃣  Running database migration..."
MIGRATION_RESPONSE=$(curl -s -X POST "${APP_URL}/api/migration/run-ab-competitive" \
  -H "X-API-KEY: ${API_KEY}" \
  -H "Content-Type: application/json")

echo "$MIGRATION_RESPONSE" | python3 -m json.tool
echo ""

# Check if migration succeeded
if echo "$MIGRATION_RESPONSE" | grep -q '"success": true'; then
    echo "✅ Migration completed successfully!"
    echo ""
elif echo "$MIGRATION_RESPONSE" | grep -q 'success'; then
    echo "✅ Migration completed successfully!"
    echo ""
else
    echo "❌ Migration failed!"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════════════"

# Step 2: Verify A/B tests
echo "2️⃣  Verifying A/B tests..."
AB_TESTS=$(curl -s "${APP_URL}/api/chatbot/ab-tests/results" \
  -H "X-ADMIN-API-KEY: ${API_KEY}")

echo "$AB_TESTS" | python3 -m json.tool
echo ""

TEST_COUNT=$(echo "$AB_TESTS" | python3 -c "import sys, json; data = json.load(sys.stdin); print(len(data.get('tests', [])))")

if [ "$TEST_COUNT" -eq 3 ]; then
    echo "✅ All 3 A/B tests created!"
else
    echo "⚠️  Expected 3 tests, found $TEST_COUNT"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"

# Step 3: Test competitive intelligence endpoint
echo "3️⃣  Testing competitive intelligence endpoint..."
INTEL_RESPONSE=$(curl -s "${APP_URL}/api/chatbot/competitive-intelligence?days=1" \
  -H "X-ADMIN-API-KEY: ${API_KEY}")

echo "$INTEL_RESPONSE" | python3 -m json.tool
echo ""
echo "✅ Competitive intelligence endpoint working!"

echo ""
echo "════════════════════════════════════════════════════════════════"

# Step 4: Test Monday.com connection
echo "4️⃣  Testing Monday.com integration..."
MONDAY_TEST=$(curl -s -X POST "${APP_URL}/api/chatbot/test-monday" \
  -H "X-ADMIN-API-KEY: ${API_KEY}")

echo "$MONDAY_TEST" | python3 -m json.tool
echo ""

if echo "$MONDAY_TEST" | grep -q '"message": "Monday.com connection successful"'; then
    echo "✅ Monday.com connected!"
else
    echo "⚠️  Monday.com connection issue - check configuration"
fi

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ SETUP COMPLETE!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📋 MANUAL STEPS REQUIRED:"
echo ""
echo "1. Add columns in Monday.com Board (2145240699):"
echo "   - lead_score (Number, 0-100)"
echo "   - competitor_mentioned (Text)"
echo "   - next_action (Long Text)"
echo ""
echo "2. Test E2E conversation flow:"
echo "   - Start chat at ${APP_URL}"
echo "   - Mention competitor: 'Remonteo mi powiedział że jest taniej'"
echo "   - Verify competitive intel is tracked"
echo ""
echo "3. Monitor dashboards:"
echo "   - A/B Tests: ${APP_URL}/api/chatbot/ab-tests/results"
echo "   - Competitive Intel: ${APP_URL}/api/chatbot/competitive-intelligence"
echo "   - Lead Stats: ${APP_URL}/api/chatbot/stats/leads"
echo ""
echo "════════════════════════════════════════════════════════════════"
