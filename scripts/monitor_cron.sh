#!/bin/zsh
# Monitor cron job execution and send notifications if it fails

LOG_FILE="/Users/michalmarini/Projects/manus/novahouse-chatbot-api/logs/auto_push.log"
ALERT_FILE="/Users/michalmarini/Projects/manus/novahouse-chatbot-api/logs/cron_alerts.log"

# Check if log file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "$(date): ERROR - Log file not found: $LOG_FILE" >> "$ALERT_FILE"
    exit 1
fi

# Check for recent errors in the log (last 1 hour)
RECENT_ERRORS=$(grep "ERROR" "$LOG_FILE" | tail -20)

if [ -n "$RECENT_ERRORS" ]; then
    echo "$(date): WARNING - Errors detected in auto-push logs:" >> "$ALERT_FILE"
    echo "$RECENT_ERRORS" >> "$ALERT_FILE"
    echo "----------------------------------------" >> "$ALERT_FILE"

    # Optional: Send notification (macOS)
    osascript -e 'display notification "Auto-push errors detected! Check logs." with title "Git Auto-Push Monitor"' 2>/dev/null || true
fi

# Check if last push was more than 2 hours ago
LAST_PUSH=$(grep "Successfully pushed" "$LOG_FILE" | tail -1)
if [ -z "$LAST_PUSH" ]; then
    echo "$(date): WARNING - No successful push found in logs" >> "$ALERT_FILE"
fi

echo "$(date): Cron monitoring check completed" >> "$ALERT_FILE"
