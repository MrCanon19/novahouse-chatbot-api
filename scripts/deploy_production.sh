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

# app.yaml.secret already has full structure, use it directly
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

# gcloud app deploy requires app.yaml in the project root
# Create temporary app.yaml from app.yaml.secret (app.yaml is in .gitignore)
echo "📤 Preparing deployment..."
if [ -f "app.yaml" ]; then
    echo "⚠️  app.yaml already exists, backing up..."
    mv app.yaml app.yaml.backup.$(date +%s)
fi

cp app.yaml.secret app.yaml

echo "📤 Deploying to Google App Engine..."
echo "   Using app.yaml (created from app.yaml.secret)"

# Deploy (app.yaml is in .gitignore, so it won't be committed)
gcloud app deploy app.yaml \
    --quiet \
    --project=glass-core-467907-e9 \
    --version="$(date +%Y%m%d%H%M%S)"

# Wait a moment for deployment to start
sleep 2

# Clean up - remove app.yaml (it's in .gitignore)
rm -f app.yaml
echo "✅ app.yaml cleaned up (was temporary)"

# Restore backup if it existed
if ls app.yaml.backup.* 1> /dev/null 2>&1; then
    mv app.yaml.backup.* app.yaml
    echo "✅ Restored original app.yaml"
fi

echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 App URL: https://glass-core-467907-e9.ey.r.appspot.com"
echo "🔗 Health check: https://glass-core-467907-e9.ey.r.appspot.com/api/health"
echo ""
echo "📊 Check logs: gcloud app logs tail -s default --project=glass-core-467907-e9"

