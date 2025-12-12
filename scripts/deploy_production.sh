#!/bin/bash
# NovaHouse Chatbot - Production Deployment Script
# This script ensures safe deployment with all required secrets

set -e  # Stop on error

echo "🚀 NovaHouse Chatbot - Production Deployment"
echo ""

# Check if app.yaml.secret exists
if [ ! -f "app.yaml.secret" ]; then
    echo "❌ ERROR: app.yaml.secret not found!"
    echo "   This file contains production secrets and is required for deployment."
    exit 1
fi

# Check if required secrets are in app.yaml.secret
echo "📋 Checking required secrets..."
REQUIRED_SECRETS=("SECRET_KEY" "ADMIN_API_KEY" "OPENAI_API_KEY" "DATABASE_URL")
MISSING_SECRETS=()

for secret in "${REQUIRED_SECRETS[@]}"; do
    if ! grep -q "^[[:space:]]*${secret}:" app.yaml.secret; then
        MISSING_SECRETS+=("$secret")
    fi
done

if [ ${#MISSING_SECRETS[@]} -ne 0 ]; then
    echo "❌ ERROR: Missing required secrets in app.yaml.secret:"
    for secret in "${MISSING_SECRETS[@]}"; do
        echo "   - $secret"
    done
    exit 1
fi

echo "✅ All required secrets found"
echo ""

# Create temporary deploy file with full path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DEPLOY_FILE="$PROJECT_DIR/app.yaml.deploy.$(date +%s)"

cd "$PROJECT_DIR"
cp app.yaml.secret "$DEPLOY_FILE"

echo "📤 Deploying to Google App Engine..."
gcloud app deploy "$DEPLOY_FILE" \
    --quiet \
    --project=glass-core-467907-e9 \
    --version="$(date +%Y%m%d%H%M%S)"

# Clean up
rm -f "$DEPLOY_FILE"
echo "✅ Deploy file cleaned up"

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 App URL: https://glass-core-467907-e9.ey.r.appspot.com"
echo "🔗 Health check: https://glass-core-467907-e9.ey.r.appspot.com/api/health"
echo ""
echo "📊 Check logs: gcloud app logs tail -s default --project=glass-core-467907-e9"

