# Deployment Guide - Chat Improvements V2.4

## 📋 Pre-deployment Checklist

- [x] Code committed to repository
- [ ] Database migration ready
- [ ] Cron configuration ready
- [ ] Environment variables configured
- [ ] Frontend widget updated

## 🗄️ Database Migration

### Local Development
```bash
# Run migration locally
python src/migrations/add_chat_improvements_v24.py

# Verify columns
python -c "
from src.main import app, db
from sqlalchemy import inspect
with app.app_context():
    inspector = inspect(db.engine)
    print('ChatConversation columns:', [c['name'] for c in inspector.get_columns('chat_conversations')])
    print('ChatMessage columns:', [c['name'] for c in inspector.get_columns('chat_messages')])
"
```

### Google Cloud SQL (Production)
```bash
# Connect to Cloud SQL
gcloud sql connect novahouse-db --user=postgres

# Run SQL commands
ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS conversation_summary TEXT;
ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS needs_human_review BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS followup_count INTEGER DEFAULT 0;
ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS last_followup_at TIMESTAMP;
ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS is_followup BOOLEAN DEFAULT FALSE;

# Verify
\d chat_conversations
\d chat_messages
```

## ⏰ Cron Jobs Setup

### 1. Deploy cron.yaml to GAE
```bash
# Deploy cron configuration
gcloud app deploy cron.yaml --project=your-project-id

# Verify cron jobs
gcloud app cron describe --project=your-project-id
```

### 2. Configure CRON_API_KEY
```bash
# Generate secure key
CRON_KEY=$(openssl rand -base64 32)

# Add to app.yaml
echo "CRON_API_KEY: '$CRON_KEY'" >> app.yaml.secret

# Or set in GCP Console
# App Engine > Settings > Environment Variables
# Add: CRON_API_KEY = <generated-key>
```

### 3. Test Cron Endpoints
```bash
# Test locally
export CRON_API_KEY="your-test-key"
curl -X POST http://localhost:8080/api/cron/test \
  -H "X-CRON-KEY: $CRON_API_KEY"

# Test production (after deployment)
curl -X POST https://your-app.appspot.com/api/cron/test \
  -H "X-CRON-KEY: $CRON_API_KEY"
```

## 🚀 Deployment Steps

### 1. Run Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test suites
pytest tests/test_sentiment_service.py -v
pytest tests/test_followup_automation.py -v
```

### 2. Deploy to GAE
```bash
# Deploy application
gcloud app deploy app.yaml --project=your-project-id

# Deploy cron jobs
gcloud app deploy cron.yaml --project=your-project-id

# Monitor deployment
gcloud app logs tail -s default
```

### 3. Run Database Migration
```bash
# SSH to GAE instance or use Cloud Shell
gcloud app ssh

# Run migration
cd /srv
python src/migrations/add_chat_improvements_v24.py
```

### 4. Verify Deployment
```bash
# Check health endpoint
curl https://your-app.appspot.com/api/health

# Test chat endpoint
curl -X POST https://your-app.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Witam",
    "session_id": "test-session-123"
  }'

# Check cron jobs status
gcloud app cron describe
```

## 🧪 Post-Deployment Testing

### 1. Test Sentiment Analysis
```bash
# Send frustrated message
curl -X POST https://your-app.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "To jest okropne, nic nie działa!",
    "session_id": "test-sentiment-001"
  }'

# Expected: sentiment.should_escalate = true
```

### 2. Test Proactive Suggestions
```bash
# Start conversation
curl -X POST https://your-app.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Witam",
    "session_id": "test-suggestions-001"
  }'

# Expected: suggestions array with quick actions
```

### 3. Test Multi-turn Dialog
```bash
# First message
curl -X POST https://your-app.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Jaki jest koszt pakietu złotego?",
    "session_id": "test-multiturn-001"
  }'

# Reference previous context
curl -X POST https://your-app.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "a srebrnego?",
    "session_id": "test-multiturn-001"
  }'

# Expected: Expanded to "Jaki jest koszt pakietu srebrnego?"
```

### 4. Test Follow-up Automation
```bash
# Create abandoned conversation
curl -X POST https://your-app.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Ile kosztuje remont?",
    "session_id": "test-followup-001"
  }'

# Wait 24h or manually trigger cron
curl -X POST https://your-app.appspot.com/api/cron/send-followups \
  -H "X-CRON-KEY: $CRON_API_KEY"

# Check conversation for followup_count > 0
```

### 5. Test Widget with Suggestions
```html
<!-- Test widget locally -->
<!DOCTYPE html>
<html>
<head>
    <title>Widget Test</title>
</head>
<body>
    <h1>Test Chatbot Widget</h1>

    <script>
        window.NOVAHOUSE_API_URL = 'https://your-app.appspot.com';
    </script>
    <script src="https://your-app.appspot.com/static/widget.js"></script>
</body>
</html>
```

## 📊 Monitoring

### 1. Check Logs
```bash
# Real-time logs
gcloud app logs tail -s default

# Filter by service
gcloud app logs read --service=default --limit=50

# Check cron execution logs
gcloud logging read "resource.type=gae_app AND logName=projects/your-project/logs/appengine.googleapis.com%2Frequest_log" --limit=50
```

### 2. Monitor Metrics
- **Sentiment Escalations**: Count of `needs_human_review=true`
- **Follow-up Success**: Conversion rate after follow-ups
- **Multi-turn Resolution**: Accuracy of reference resolution
- **Session Timeouts**: Number of sessions requiring reengagement

### 3. Database Queries
```sql
-- Check sentiment escalations
SELECT COUNT(*)
FROM chat_conversations
WHERE needs_human_review = TRUE;

-- Check follow-up stats
SELECT
  followup_count,
  COUNT(*) as conversations
FROM chat_conversations
GROUP BY followup_count;

-- Check high-value abandoned leads
SELECT
  session_id,
  context_data,
  started_at,
  followup_count
FROM chat_conversations
WHERE followup_count = 0
  AND ended_at IS NULL
  AND started_at < NOW() - INTERVAL '24 hours'
ORDER BY started_at DESC;
```

## 🔧 Troubleshooting

### Cron Jobs Not Running
```bash
# Check cron configuration
gcloud app cron describe

# Check IAM permissions
gcloud projects get-iam-policy your-project-id

# Manually trigger cron
curl -X POST https://your-app.appspot.com/api/cron/send-followups \
  -H "X-CRON-KEY: $CRON_API_KEY"
```

### Database Migration Failed
```bash
# Check connection
gcloud sql connect novahouse-db --user=postgres

# Rollback if needed
ALTER TABLE chat_conversations DROP COLUMN IF EXISTS conversation_summary;
ALTER TABLE chat_conversations DROP COLUMN IF EXISTS needs_human_review;
ALTER TABLE chat_conversations DROP COLUMN IF EXISTS followup_count;
ALTER TABLE chat_conversations DROP COLUMN IF EXISTS last_followup_at;
ALTER TABLE chat_messages DROP COLUMN IF EXISTS is_followup;

# Re-run migration
python src/migrations/add_chat_improvements_v24.py
```

### Widget Not Showing Suggestions
```javascript
// Check browser console for errors
// Verify API response format
console.log(data.suggestions);

// Expected format:
// [
//   { "title": "Zobacz cennik", "payload": "Jaki jest cennik?" },
//   { "title": "Umów spotkanie", "payload": "Chcę umówić spotkanie" }
// ]
```

## 📈 Expected Impact

After deployment, expect:
- **+30-50%** conversion rate from sentiment-based escalations
- **+20-30%** lead recovery from automated follow-ups
- **+40%** user engagement from proactive suggestions
- **-25%** session abandonment from timeout reengagement
- **+15%** context accuracy from multi-turn dialog resolution

## 🎯 Next Steps

1. Monitor performance for 1 week
2. A/B test follow-up message variants
3. Fine-tune sentiment thresholds based on false positive rate
4. Add more suggestion templates for different states
5. Integrate with CRM for follow-up tracking

## 📞 Support

If issues arise:
1. Check logs: `gcloud app logs tail -s default`
2. Verify database columns exist
3. Confirm CRON_API_KEY is set
4. Test endpoints manually with curl
5. Review error traces in Cloud Console
