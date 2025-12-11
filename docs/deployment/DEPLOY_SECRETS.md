# 🔐 Google Cloud Secret Manager Setup

## ⚠️ CRITICAL: app.yaml Leaked Secrets

**PROBLEM:** `app.yaml` w Git zawierał:
- SECRET_KEY
- DATABASE_URL z hasłem
- MONDAY_API_KEY

**ROZWIĄZANIE:** Użyj Google Secret Manager

---

## 🚀 Quick Fix (Immediate)

### 1. Rotate All Compromised Credentials

```bash
# 1. Generate new SECRET_KEY
python -c "import os; print(os.urandom(32).hex())"

# 2. Change database password
gcloud sql users set-password chatbot_user \
  --instance=novahouse-chatbot-db \
  --password=NEW_STRONG_PASSWORD_HERE

# 3. Revoke Monday.com token
# Go to: https://monday.com → Profile → Admin → API
# Delete old token, generate new one
```

### 2. Use app.yaml.secret Locally

```bash
# Copy template
cp app.yaml.secret app.yaml.prod

# Edit with real secrets
nano app.yaml.prod

# Deploy
gcloud app deploy app.yaml.prod

# Delete immediately
rm app.yaml.prod
```

---

## 🛡️ Best Practice: Google Secret Manager

### Setup (One-time)

```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secrets
echo -n "your-new-secret-key-64-chars" | \
  gcloud secrets create SECRET_KEY --data-file=-

echo -n "postgresql://user:NEW_PASSWORD@..." | \
  gcloud secrets create DATABASE_URL --data-file=-

echo -n "your-monday-api-key" | \
  gcloud secrets create MONDAY_API_KEY --data-file=-
```

### Update app.yaml

```yaml
runtime: python311
service: default

env_variables:
  FLASK_ENV: production
  MONDAY_BOARD_ID: "2145240699"

# Secrets from Secret Manager
beta_settings:
  cloud_sql_instances: "glass-core-467907-e9:europe-west1:novahouse-chatbot-db"

# Access secrets in code:
# import google.cloud.secretmanager as sm
# client = sm.SecretManagerServiceClient()
# secret = client.access_secret_version(
#   name="projects/PROJECT_ID/secrets/SECRET_KEY/versions/latest"
# )
# os.environ['SECRET_KEY'] = secret.payload.data.decode('UTF-8')
```

### Update main.py Startup

```python
# At top of src/main.py, before app creation:
def load_secrets():
    """Load secrets from Google Secret Manager in production"""
    if os.getenv('FLASK_ENV') == 'production':
        try:
            from google.cloud import secretmanager
            client = secretmanager.SecretManagerServiceClient()
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')

            secrets_to_load = ['SECRET_KEY', 'DATABASE_URL', 'MONDAY_API_KEY']
            for secret_name in secrets_to_load:
                name = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
                response = client.access_secret_version(name=name)
                os.environ[secret_name] = response.payload.data.decode('UTF-8')

            print("✅ Secrets loaded from Secret Manager")
        except Exception as e:
            print(f"⚠️ Failed to load secrets: {e}")

load_secrets()
```

---

## 🚨 Emergency: Leaked Secrets Cleanup

### If secrets already in Git history:

```bash
# 1. Remove from current commit
git rm app.yaml.backup app.yaml.secret
git commit -m "Remove leaked secrets"

# 2. Purge from Git history (DANGER!)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch app.yaml.backup' \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push (if you own the repo)
git push origin --force --all

# 4. Notify GitHub
# Go to: https://github.com/MrCanon19/chatbot-api/settings/secrets
# Remove any accidentally committed secrets
```

### Immediate Damage Control:

1. **Database:** Change password NOW
2. **Monday.com:** Revoke token NOW  
3. **SECRET_KEY:** Generate new one NOW
4. **Monitor:** Check Monday.com audit logs for suspicious activity
5. **Alert:** Notify team that credentials were compromised

---

## 📋 Checklist Before Next Deploy

- [ ] All secrets removed from `app.yaml`
- [ ] `app.yaml.secret` in `.gitignore`
- [ ] New SECRET_KEY generated
- [ ] Database password changed
- [ ] Monday.com API key regenerated
- [ ] Google Secret Manager configured
- [ ] Test deployment with new secrets
- [ ] Verify old credentials don't work
- [ ] Monitor logs for 24h post-deploy

---

## 🔍 Verify Secrets Not in Git

```bash
# Check current files
git grep -i "NovaH0use2025" -- ':!*.md' ':!DEPLOY_SECRETS.md'

# Check Git history (slow!)
git log -p | grep -i "NovaH0use2025"

# If found, use git-filter-branch above
```

---

## 📞 Support

**Security incident?**
- Rotate credentials FIRST
- Then contact: security@novahouse.pl

**Last updated:** 2025-11-14
