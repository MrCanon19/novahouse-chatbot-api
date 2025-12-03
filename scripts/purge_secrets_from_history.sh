#!/bin/bash
# SCRIPT TO PURGE app.yaml FROM GIT HISTORY
# WARNING: This rewrites git history - coordinate with team!

set -e

echo "🔥 REMOVING app.yaml FROM GIT HISTORY"
echo "========================================"
echo ""
echo "⚠️  WARNING: This will rewrite git history!"
echo "⚠️  All team members will need to re-clone the repo."
echo ""
read -p "Are you sure? (type 'yes' to continue): " confirmation

if [ "$confirmation" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "📦 Step 1: Backup current repository..."
cd "$(dirname "$0")/.."
BACKUP_DIR="../novahouse-chatbot-api-backup-$(date +%Y%m%d_%H%M%S)"
cp -r . "$BACKUP_DIR"
echo "✅ Backup created: $BACKUP_DIR"

echo ""
echo "🔧 Step 2: Remove app.yaml from git history..."

# Method 1: git filter-repo (recommended)
if command -v git-filter-repo &> /dev/null; then
    echo "Using git-filter-repo..."
    git filter-repo --path app.yaml --invert-paths --force

elif command -v bfg &> /dev/null; then
    # Method 2: BFG Repo Cleaner (alternative)
    echo "Using BFG Repo Cleaner..."
    bfg --delete-files app.yaml

    echo "Cleaning up..."
    git reflog expire --expire=now --all
    git gc --prune=now --aggressive

else
    echo "❌ Neither git-filter-repo nor BFG is installed!"
    echo ""
    echo "Install one of them:"
    echo "  git-filter-repo: pip3 install git-filter-repo"
    echo "  BFG: brew install bfg"
    exit 1
fi

echo ""
echo "✅ Step 3: Verify app.yaml is gone..."
git log --all --full-history -- app.yaml | head -5
echo "(Should show nothing above)"

echo ""
echo "🚀 Step 4: Force push to remote..."
echo "⚠️  This will rewrite history on GitHub!"
echo ""
read -p "Force push to origin? (type 'yes'): " push_confirmation

if [ "$push_confirmation" == "yes" ]; then
    git push origin --force --all
    git push origin --force --tags
    echo "✅ Force pushed to origin"
else
    echo "⚠️  Remember to force push manually:"
    echo "   git push origin --force --all"
    echo "   git push origin --force --tags"
fi

echo ""
echo "🎉 DONE! app.yaml removed from git history."
echo ""
echo "📝 NEXT STEPS:"
echo "1. Tell team members to re-clone the repo"
echo "2. Verify secrets are gone: git log --all -- app.yaml"
echo "3. Keep app.yaml LOCAL ONLY (already in .gitignore)"
