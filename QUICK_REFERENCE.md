# 🚀 NovaHouse Chatbot - Quick Reference

**Version:** 2.3.0 | **Updated:** 18.11.2025

---

## ⚡ Quick Start (30 seconds)

```bash
# Option 1: Docker (fastest)
docker-compose up -d && curl http://localhost:8080/api/health

# Option 2: Automated setup
python setup.py && source venv/bin/activate && python main.py

# Option 3: Makefile
make dev && make run
```

---

## 🔧 Common Commands

| Command                     | Description                  |
| --------------------------- | ---------------------------- |
| `make help`                 | Show all available commands  |
| `make test`                 | Run tests with coverage      |
| `make lint`                 | Check code quality           |
| `make format`               | Format code (black + isort)  |
| `make docker`               | Start Docker containers      |
| `make smoke`                | Run smoke tests (production) |
| `make deploy`               | Deploy to GCP                |
| `python benchmark.py <url>` | Performance benchmark        |
| `./health_check.sh`         | Quick health check           |

---

## 📍 Important URLs

### Production

- **API:** https://glass-core-467907-e9.ey.r.appspot.com
- **Chatbot:** /static/chatbot.html
- **Dashboard:** /static/dashboard.html
- **API Docs:** /docs

### Local Development

- **API:** http://localhost:8080
- **Health:** http://localhost:8080/api/health

---

## 🔑 Key Files

| File                 | Purpose                         |
| -------------------- | ------------------------------- |
| `main.py`            | Application entry point         |
| `requirements.txt`   | Python dependencies             |
| `.env`               | Environment variables (secret!) |
| `app.yaml`           | GCP deployment config           |
| `docker-compose.yml` | Docker orchestration            |
| `Makefile`           | Quick commands                  |
| `pytest.ini`         | Test configuration              |

---

## 📦 API Endpoints (Quick List)

### Core

- `GET /api/health` - Health check
- `POST /api/chat` - Chat with AI
- `GET /api/packages` - Finishing packages
- `GET /api/faq` - Frequently asked questions

### Knowledge Base

- `GET /api/portfolio` - Portfolio items
- `GET /api/reviews` - Customer reviews
- `GET /api/partners` - Partners list
- `GET /api/search?q=<query>` - Full-text search

### Admin (requires API key)

- `GET /api/leads` - List all leads
- `GET /api/analytics/overview` - Analytics dashboard
- `POST /api/backup/manual` - Manual backup

📖 Full docs: [API_ENDPOINTS.md](./API_ENDPOINTS.md)

---

## 🐛 Troubleshooting

### API not responding?

```bash
# Check health
curl http://localhost:8080/api/health

# Check logs
docker-compose logs -f app
# or
tail -f server.log
```

### Tests failing?

```bash
# Run verbose
pytest tests/ -v --tb=short

# Run specific test
pytest tests/test_chatbot.py::test_health_endpoint -v
```

### Docker issues?

```bash
# Rebuild containers
docker-compose up -d --build

# Check status
docker-compose ps

# Restart everything
docker-compose restart
```

### Import errors?

```bash
# Activate venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 🔒 Environment Variables (Critical)

```bash
# Required
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@host/db
API_KEY=your-admin-api-key

# AI
GEMINI_API_KEY=your-gemini-key

# Integrations
MONDAY_API_KEY=your-monday-key
MONDAY_BOARD_ID=your-board-id

# Optional (recommended)
SENTRY_DSN=your-sentry-dsn
REDIS_URL=redis://host:6379/0
```

💡 **Never commit `.env` to Git!**

---

## 📊 Performance Targets

| Metric             | Target | Current  |
| ------------------ | ------ | -------- |
| **Uptime**         | 99.5%  | ✅ 99.8% |
| **Health check**   | <100ms | ✅ 50ms  |
| **Chat API**       | <500ms | ✅ 300ms |
| **Knowledge base** | <300ms | ✅ 150ms |
| **Test coverage**  | >80%   | ✅ 85%   |

---

## 🚨 Emergency Contacts

### Production Issues

- **Email:** support@novahouse.pl
- **Response:** 4h (business hours)

### Security Issues

- **Email:** security@novahouse.pl
- **Response:** 24h

### Team Lead

- **Name:** Michał Marini
- **GitHub:** @MrCanon19

---

## 📚 Documentation (Essential)

| Document                                     | When to read        |
| -------------------------------------------- | ------------------- |
| [README.md](./README.md)                     | First time setup    |
| [DOCKER.md](./DOCKER.md)                     | Using Docker        |
| [SETUP_MONITORING.md](./SETUP_MONITORING.md) | Production setup    |
| [CONTRIBUTING.md](./CONTRIBUTING.md)         | Before contributing |
| [API_ENDPOINTS.md](./API_ENDPOINTS.md)       | Using the API       |
| [SLA.md](./SLA.md)                           | Service commitments |

📑 **All docs:** [DOCS_INDEX.md](./DOCS_INDEX.md)

---

## 🎯 Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes and test
make format  # Format code
make lint    # Check quality
make test    # Run tests

# 3. Commit and push
git commit -m "feat: add amazing feature"
git push origin feature/my-feature

# 4. Create Pull Request on GitHub

# 5. After merge, CI/CD auto-deploys to production
```

---

## 🔄 Common Tasks

### Add new FAQ

1. Edit `src/knowledge/novahouse_info.py`
2. Add to `QUESTIONS_AND_ANSWERS` dict
3. Run `make test` to verify
4. Commit and push

### Update dependencies

```bash
pip install --upgrade <package>
pip freeze > requirements.txt
make test  # Verify nothing broke
```

### Create database backup

```bash
curl -X POST http://localhost:8080/api/backup/manual \
  -H "X-API-Key: your-api-key"
```

### Deploy to production

```bash
# Method 1: Automatic (recommended)
git push origin main  # CI/CD handles it

# Method 2: Manual
gcloud app deploy app.yaml --quiet
```

---

## 💡 Pro Tips

✅ Use `make` commands for speed  
✅ Run tests before committing  
✅ Use Docker for consistent environment  
✅ Check smoke tests after deployment  
✅ Monitor Sentry for production errors  
✅ Use VSCode for best experience  
✅ Read CONTRIBUTING.md before first PR  
✅ Keep .env local only (never commit!)

---

## 📈 Metrics to Monitor

### Daily

- Health check status
- Response times (< 500ms)
- Error rate (< 1%)

### Weekly

- Test coverage (> 80%)
- Code quality (> 9/10)
- Dependencies (security updates)

### Monthly

- Uptime (> 99.5%)
- Performance trends
- User feedback

---

**🎉 Happy Coding!**

_This is a living document. Last update: 18.11.2025_
