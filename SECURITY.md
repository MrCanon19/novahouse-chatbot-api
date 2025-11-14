# 🔒 Security Guidelines - NovaHouse Chatbot API

## ⚠️ CRITICAL: Before Production Deployment

### 1. SECRET_KEY Configuration
**STATUS:** ❌ VULNERABLE if not changed

```bash
# Generate secure key:
python -c "import os; print(os.urandom(32).hex())"

# Add to .env:
SECRET_KEY=your_generated_64_char_hex_string_here
```

**Why:** Default/hardcoded SECRET_KEY allows session hijacking, CSRF bypass, cookie forgery.

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
# Strong password format:
DATABASE_URL=postgresql://user:STRONG_PASSWORD_32CHARS@host/db

# Google Cloud SQL:
DATABASE_URL=postgresql://user:pass@/db?host=/cloudsql/PROJECT:REGION:INSTANCE
```

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
- ⚠️ Admin endpoints unprotected
- ⚠️ No JWT/OAuth implementation

**Recommended for production:**
```python
# Add to .env:
ADMIN_API_KEY=your_secret_admin_key_here

# Add decorator to admin routes:
from functools import wraps
from flask import request

def require_admin_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
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

- [ ] `SECRET_KEY` changed from default
- [ ] `.env` file NOT in git
- [ ] `FLASK_ENV=production` set
- [ ] CORS origins restricted
- [ ] HTTPS enabled
- [ ] Rate limiting tested
- [ ] File upload limits tested
- [ ] Admin endpoints protected with API key
- [ ] Database password is strong (32+ chars)
- [ ] Error handlers hide stack traces
- [ ] Dependencies scanned for vulnerabilities
- [ ] Backups scheduled and tested
- [ ] Logs reviewed for sensitive data leaks

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
