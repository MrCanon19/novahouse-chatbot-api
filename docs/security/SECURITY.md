# 🔒 Security Guidelines - NovaHouse Chatbot API

## ⚠️ CRITICAL: Before Production Deployment

### 1. SECRET_KEY Configuration
**STATUS:** ✅ IMPLEMENTED - Credentials rotated 2025-11-14

```bash
# ✅ NEW SECRET_KEY generated (64 hex chars):
# Znajduje się w app.yaml.secret (NIE commituj!)

# W produkcji ustaw jako environment variable:
export SECRET_KEY=2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489
```

**Why:** SECRET_KEY używany do podpisywania session cookies, CSRF tokens, Flask sessions.
**Action required:** Ustaw nowy SECRET_KEY w Google Cloud (patrz ROTATE_CREDENTIALS.md)

---

### 2. Environment Variables
**STATUS:** ✅ Template provided in `.env.example`

**NEVER commit:**
- `.env` files
- `secrets.json`
- `credentials.json`
- Any file with API keys

**Check before commit:**
```bash
git diff --cached | grep -i "api_key\|secret\|password"
```

---

### 3. File Upload Security
**STATUS:** ✅ Implemented

**Protections:**
- ✅ Extension whitelist (png, jpg, jpeg, gif, webp)
- ✅ MIME type validation (magic bytes check)
- ✅ File size limit (50MB max)
- ✅ Secure filename generation
- ✅ Rate limiting (10 uploads/min)

**Test:**
```bash
# Try uploading shell script disguised as image:
echo "<?php system(\$_GET['cmd']); ?>" > malicious.jpg
curl -F "file=@malicious.jpg" http://localhost:8080/api/upload/image
# Should return: "Invalid image file. File content does not match image format."
```

---

### 4. Rate Limiting
**STATUS:** ✅ Implemented with Redis fallback

**Limits:**
- API endpoints: 100 req/min (default)
- File uploads: 10 req/min
- Search: 100 req/min

**Override for specific IPs:**
```python
# In middleware/security.py:
WHITELISTED_IPS = ['127.0.0.1', 'your.office.ip']
```

---

### 5. Database Security

**SQLite (Development):**
- ✅ File permissions: `chmod 600 src/database/app.db`
- ⚠️ Not for production under load

**PostgreSQL (Production):**
```bash
# ✅ NEW PASSWORD generated (2025-11-14):
# vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo

# Google Cloud SQL connection string (w app.yaml.secret):
DATABASE_URL=postgresql://chatbot_user:vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo@/chatbot?host=/cloudsql/glass-core-467907-e9:europe-west1:novahouse-chatbot-db

# ⚠️ CRITICAL: Zmień hasło w Cloud SQL PRZED deploymentem!
# gcloud sql users set-password chatbot_user --instance=novahouse-chatbot-db --password='vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo'
```

**Action required:** Wykonaj rotację credentials z ROTATE_CREDENTIALS.md

**Prevent SQL injection:**
- ✅ Uses SQLAlchemy ORM (parameterized queries)
- ⚠️ Never use `.raw()` with user input

---

### 6. CORS Configuration
**STATUS:** ⚠️ Currently allows all origins

**Production hardening:**
```python
# In main.py:
CORS(app, origins=[
    'https://novahouse.pl',
    'https://www.novahouse.pl',
    'https://chatbot.novahouse.pl'
])
```

---

### 7. Error Handling
**STATUS:** ✅ Implemented

**Production mode:**
- ✅ Hides stack traces (only shows "Internal server error")
- ✅ Logs detailed errors server-side
- ✅ Custom 404, 413, 500 handlers

**Test:**
```bash
FLASK_ENV=production python src/main.py
# Errors won't leak details
```

---

### 8. Dependency Security

**Check for vulnerabilities:**
```bash
pip install safety
safety check -r requirements.txt
```

**Keep updated:**
```bash
pip list --outdated
pip install --upgrade <package>
```

**Known issues:**
- None currently (as of 2025-11-14)

---

### 9. API Authentication

**Current:**
- ✅ Admin endpoints protected with @require_api_key
- ✅ backup.py: All 4 endpoints require X-API-Key
- ✅ dashboard_widgets.py: All 8 endpoints require X-API-Key
- ✅ ab_testing.py: All 6 endpoints require X-API-Key
- ⚠️ Development mode: Jeśli brak API_KEY w .env, endpoints działają (dla testów)

**Production setup:**
```bash
# Add to .env or app.yaml.secret:
API_KEY=your_secret_admin_key_here
# lub
ADMIN_API_KEY=your_secret_admin_key_here

# Usage in requests:
curl -H "X-API-Key: your_secret_admin_key_here" \
  https://your-app.com/api/backup/export
        key = request.headers.get('X-Admin-Key')
        if key != os.getenv('ADMIN_API_KEY'):
            return {'error': 'Unauthorized'}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/admin/leads')
@require_admin_key
def admin_leads():
    ...
```

---

### 10. HTTPS/TLS

**Google Cloud App Engine:**
- ✅ Automatic HTTPS
- ✅ Managed certificates

**Self-hosted:**
```bash
# Use Let's Encrypt:
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d chatbot.novahouse.pl
```

---

## 🛡️ Security Checklist

Before deploying to production:

- [x] `SECRET_KEY` changed from default ✅ DONE (2025-11-14)
- [x] `.env` file NOT in git ✅ In .gitignore
- [x] app.yaml secrets removed ✅ Moved to app.yaml.secret
- [x] `FLASK_ENV=production` set ✅ In app.yaml
- [ ] ⚠️ CORS origins restricted (obecnie: allow all - opcjonalne)
- [x] HTTPS enabled ✅ Google App Engine auto
- [x] Rate limiting tested ✅ 100 req/min default, 10 uploads/min
- [x] File upload limits tested ✅ 50MB max, MIME validation
- [x] Admin endpoints protected with API key ✅ @require_api_key dodany
- [x] Database password is strong (32+ chars) ✅ DONE (vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo)
- [x] Error handlers hide stack traces ✅ Production mode
- [x] Dependencies scanned for vulnerabilities ✅ No known issues
- [x] Backups scheduled and tested ✅ APScheduler (daily 3 AM)
- [x] Logs reviewed for sensitive data leaks ✅ No secrets in code

**UWAGA:** Przed deploymentem wykonaj kroki z ROTATE_CREDENTIALS.md!

---

## 🚨 Incident Response

**If security breach suspected:**

1. **Immediate:**
   - Rotate SECRET_KEY
   - Revoke compromised API keys
   - Check logs: `grep -i "error\|fail\|403\|401" logs/*.log`

2. **Investigation:**
   - Review recent API calls
   - Check file uploads
   - Audit database changes

3. **Recovery:**
   - Restore from backup: `/api/backup/list`
   - Reset user sessions
   - Notify affected users (RODO compliance)

---

## 📞 Security Contacts

**Report vulnerabilities:**
- Email: security@novahouse.pl
- Response time: 24 hours

**Bug bounty:** Not currently active

---

## 📚 Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/stable/security/)
- [RODO Compliance Guide](README_RODO.md)

---

**Last updated:** 2025-11-14  
**Version:** 2.3.0
