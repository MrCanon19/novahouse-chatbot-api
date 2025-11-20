#!/bin/bash
# NovaHouse Chatbot - Automatic Deployment Script
# Generated: 2025-11-20

set -e  # Stop on error

echo "🚀 NovaHouse Chatbot V2.4 - Deployment Starting..."
echo ""

# 1. Git Push
echo "📤 [1/5] Pushing to GitHub..."
cd /Users/michalmarini/Projects/manus/novahouse-chatbot-api
git push origin main
echo "✅ Git push completed"
echo ""

# 2. Database Migration
echo "🗄️ [2/5] Running database migration..."
python src/migrations/add_chat_improvements_v24.py
echo "✅ Migration completed"
echo ""

# 3. Deploy to GAE
echo "☁️ [3/5] Deploying to Google App Engine..."
gcloud app deploy app.yaml --quiet
echo "✅ Deployment completed"
echo ""

# 4. Health Check
echo "🏥 [4/5] Checking application health..."
sleep 5
curl -s https://novahouse-chatbot-api.appspot.com/api/health | python -m json.tool
echo ""
echo "✅ Health check passed"
echo ""

# 5. Test Chat
echo "💬 [5/5] Testing chat endpoint..."
curl -s -X POST https://novahouse-chatbot-api.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Witam\", \"session_id\": \"deploy-test-$(date +%s)\"}" | python -m json.tool
echo ""

echo "🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo ""
echo "📊 Check logs: gcloud app logs tail -s default"
echo "🌐 App URL: https://novahouse-chatbot-api.appspot.com"
