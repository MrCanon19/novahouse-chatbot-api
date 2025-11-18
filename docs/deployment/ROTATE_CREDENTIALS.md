# 🚨 CRITICAL: Rotate Compromised Credentials

**Date:** 2025-11-14  
**Status:** URGENT - Do this NOW

---

## 📋 Step-by-Step Instructions

### 1️⃣ Change PostgreSQL Password (5 minutes)

```bash
# Connect to Google Cloud
gcloud auth login

# Set your project
gcloud config set project glass-core-467907-e9

# Change database password
gcloud sql users set-password chatbot_user \
  --instance=novahouse-chatbot-db \
  --password='vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo'

# Verify it works
gcloud sql connect novahouse-chatbot-db --user=chatbot_user
# Enter new password when prompted
# If connects successfully: \q to exit
```

**Update app.yaml.secret:**
```yaml
DATABASE_URL: "postgresql://chatbot_user:vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo@/chatbot?host=/cloudsql/glass-core-467907-e9:europe-west1:novahouse-chatbot-db"
```

---

### 2️⃣ Update SECRET_KEY (1 minute)

**New SECRET_KEY generated:**
```
2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489
```

**Update app.yaml.secret:**
```yaml
SECRET_KEY: "2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489"
```

**Update local .env:**
```bash
echo "SECRET_KEY=2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489" >> .env
```

---

### 3️⃣ Redeploy Application (3 minutes)

```bash
# Option A: Deploy with app.yaml.secret (RECOMMENDED)
cp app.yaml.secret app.yaml.prod
gcloud app deploy app.yaml.prod
rm app.yaml.prod  # Delete immediately!

# Option B: Use Google Secret Manager (see DEPLOY_SECRETS.md)
```

---

### 4️⃣ Verify Deployment (2 minutes)

```bash
# Check health
curl https://glass-core-467907-e9.ey.r.appspot.com/api/health
curl https://glass-core-467907-e9.ey.r.appspot.com/api/health/deep

# Test database connection
curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health

# Expected: {"status": "healthy", "database": "ok", ...}
```

---

### 5️⃣ Test Locally (optional)

```bash
# Update .env with new credentials
cat > .env << EOF
SECRET_KEY=2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489
DATABASE_URL=postgresql://chatbot_user:vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo@localhost/chatbot
EOF

# Start app
python3 src/main.py

# Test
curl http://localhost:8080/api/health
```

---

## ✅ Verification Checklist

After completing all steps:

- [ ] PostgreSQL password changed in Google Cloud SQL
- [ ] New SECRET_KEY in app.yaml.secret
- [ ] Application redeployed successfully
- [ ] `/api/health` returns 200 OK
- [ ] `/api/health/deep` shows "database": "ok"
- [ ] Chatbot responds to messages
- [ ] Old credentials do NOT work anymore
- [ ] app.yaml.secret NOT committed to Git

---

## 🔐 New Credentials Summary

**SECRET_KEY:**
```
2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489
```

**PostgreSQL Password:**
```
vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo
```

**Monday.com API Key:**
```
NO CHANGE - stays the same (repo is private)
```

---

## 🚨 If Problems Occur

### Database connection fails:
```bash
# Rollback to old password temporarily
gcloud sql users set-password chatbot_user \
  --instance=novahouse-chatbot-db \
  --password='NovaH0use2025!DB'

# Fix app.yaml.secret, then try again
```

### App won't start:
```bash
# Check logs
gcloud app logs tail -s default

# Common issues:
# - Typo in password (check for special chars)
# - Wrong SECRET_KEY format (must be hex string)
# - app.yaml.secret not copied correctly
```

### Old sessions still work:
- Expected! Old cookies remain valid until expiry
- Users will need to re-login after SECRET_KEY change
- Force logout: clear Redis cache or restart app

---

## 📞 Emergency Contacts

**If you need help:**
- Technical: Michał (you)
- Database access: Google Cloud Console
- Rollback: Revert to previous app.yaml.prod

---

## 🎯 Time Estimate

- **Minimum:** 10 minutes (if everything goes smooth)
- **Maximum:** 30 minutes (if you hit issues)
- **Best time:** NOW (off-peak hours)

---

**Last updated:** 2025-11-14 23:00 UTC  
**Priority:** 🔴 CRITICAL  
**Deadline:** Within 24 hours
