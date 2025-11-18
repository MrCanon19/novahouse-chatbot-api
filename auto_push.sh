#!/bin/zsh

# Auto-push script with logging and backup
LOG_FILE="/Users/michalmarini/Projects/manus/novahouse-chatbot-api/logs/auto_push.log"
BACKUP_DIR="/Users/michalmarini/Projects/manus/novahouse-chatbot-api/backups/automated"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$BACKUP_DIR"

echo "[$TIMESTAMP] Starting auto-push script" >> "$LOG_FILE"

cd /Users/michalmarini/Projects/manus/novahouse-chatbot-api

# Check if there are changes to commit
if [[ -n $(git status -s) ]]; then
    echo "[$TIMESTAMP] Changes detected, creating backup..." >> "$LOG_FILE"
    
    # Create backup before pushing
    BACKUP_NAME="backup_$(date +%Y%m%d_%H%M%S).tar.gz"
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" \
        --exclude='node_modules' \
        --exclude='venv' \
        --exclude='__pycache__' \
        --exclude='.git' \
        --exclude='backups' \
        . 2>> "$LOG_FILE"
    
    echo "[$TIMESTAMP] Backup created: $BACKUP_NAME" >> "$LOG_FILE"
    
    # Add and commit changes
    git add -A
    git commit -m "Auto: periodic workspace sync - $(date +%Y%m%d_%H%M%S)" >> "$LOG_FILE" 2>&1
    
    echo "[$TIMESTAMP] Changes committed" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] No changes to commit" >> "$LOG_FILE"
fi

# Try to push (even if no new commits, to push pending commits)
if git push origin main >> "$LOG_FILE" 2>&1; then
    echo "[$TIMESTAMP] Successfully pushed to origin/main" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] ERROR: Failed to push to origin/main" >> "$LOG_FILE"
    exit 1
fi

echo "[$TIMESTAMP] Auto-push completed successfully" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE"
