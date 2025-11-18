# 📚 Dokumentacja NovaHouse Chatbot

## 🚀 Quick Start

| Dokument                                         | Opis                                         | Czas czytania |
| ------------------------------------------------ | -------------------------------------------- | ------------- |
| **[README.md](./README.md)**                     | Główna dokumentacja projektu                 | 5 min         |
| **[DOCKER.md](./DOCKER.md)**                     | Setup z Docker & Docker Compose              | 3 min         |
| **[SETUP_MONITORING.md](./SETUP_MONITORING.md)** | Konfiguracja Sentry & Redis & GitHub Actions | 7 min         |
| **[CONTRIBUTING.md](./CONTRIBUTING.md)**         | Jak kontrybuować do projektu                 | 10 min        |

---

## 🔧 Setup & Deployment

### Development

- **[README.md](./README.md)** - Quick start (3 opcje: Docker, setup.py, manual)
- **[DOCKER.md](./DOCKER.md)** - Docker Compose development workflow
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Development guidelines & git workflow
- **setup.py** - Automatyczny setup script (venv + deps + hooks)

### Production

- **[INSTRUKCJA_WDROZENIA_GCP.md](./INSTRUKCJA_WDROZENIA_GCP.md)** - Google Cloud Platform deployment
- **[DEPLOY_SECRETS.md](./DEPLOY_SECRETS.md)** - Zarządzanie secrets w produkcji
- **[PRODUKCJA_GOTOWA.md](./PRODUKCJA_GOTOWA.md)** - Production readiness checklist
- **[DEPLOYMENT_SUCCESS_20251114.md](./updates/DEPLOYMENT_SUCCESS_20251114.md)** - Ostatnie wdrożenie

### Monitoring & Maintenance

- **[SETUP_MONITORING.md](./SETUP_MONITORING.md)** - Sentry, Redis, GitHub Actions setup
- **[BACKUP_SYSTEM.md](./BACKUP_SYSTEM.md)** - System backupów i recovery
- **[ROTATE_CREDENTIALS.md](./ROTATE_CREDENTIALS.md)** - Rotacja credentials
- **smoke_tests.py** - Post-deployment validation

---

## 📖 Features & API

### Core Features

- **[README.md](./README.md)** - Lista wszystkich features (v1.0 - v2.3)
- **[API_ENDPOINTS.md](./API_ENDPOINTS.md)** - Kompletna dokumentacja API
- **[LINKI_NOTION.md](./LINKI_NOTION.md)** - Live linki do aplikacji

### Integracje

- **[MONDAY_INTEGRATION.md](./MONDAY_INTEGRATION.md)** - Monday.com CRM integration
- **[BOOKSY_INTEGRATION.md](./BOOKSY_INTEGRATION.md)** - Booksy booking system
- **[ANALYTICS_IMPLEMENTATION.md](./ANALYTICS_IMPLEMENTATION.md)** - Analytics & A/B testing

### Knowledge Base

- **src/knowledge/novahouse_info.py** - 45+ FAQ i 5 pakietów wykończeniowych

---

## 🔒 Security & Compliance

### Bezpieczeństwo

- **[SECURITY.md](./SECURITY.md)** - Security configuration & best practices
- **[SECURITY_POLICY.md](./SECURITY_POLICY.md)** - Vulnerability disclosure policy
- **[API_KEY_SETUP.md](./API_KEY_SETUP.md)** - Secure API key management

### RODO/GDPR

- **[RODO_IMPLEMENTATION.md](./RODO_IMPLEMENTATION.md)** - Pełna implementacja RODO
- **[RODO_QUICK_START.md](./RODO_QUICK_START.md)** - RODO quick reference
- **[RODO_CHATBOT_CHECKLIST.md](./RODO_CHATBOT_CHECKLIST.md)** - RODO compliance checklist
- **[RODO_TEST_RESULTS.md](./RODO_TEST_RESULTS.md)** - RODO testing report
- **[UMOWA_POWIERZENIA_SZABLON.md](./UMOWA_POWIERZENIA_SZABLON.md)** - Data processing agreement

---

## 📊 Status & Updates

### Aktualny Stan

- **[STATUS_CURRENT_NOTION.md](./STATUS_CURRENT_NOTION.md)** - Szczegółowy status projektu
- **[STATUS_CURRENT.md](./STATUS_CURRENT.md)** - Status snapshot
- **[LINKI_NOTION.md](./LINKI_NOTION.md)** - Wydajność i metryki

### Release Notes

- **[updates/RELEASE_NOTES_V2.3.md](./updates/RELEASE_NOTES_V2.3.md)** - v2.3 release notes
- **[updates/RELEASE_NOTES_V2.2.md](./updates/RELEASE_NOTES_V2.2.md)** - v2.2 release notes
- **[CHANGELOG.md](./CHANGELOG.md)** - Chronologiczny changelog

### Implementation Reports

- **[updates/IMPLEMENTATION_COMPLETE_V2.3.md](./updates/IMPLEMENTATION_COMPLETE_V2.3.md)** - v2.3 implementation
- **[updates/IMPLEMENTATION_COMPLETE.md](./updates/IMPLEMENTATION_COMPLETE.md)** - Previous implementations
- **[FINAL_SUMMARY.md](./FINAL_SUMMARY.md)** - Podsumowanie finalne
- **[RUNDY_1_2_3_FINAL_SUMMARY.md](./RUNDY_1_2_3_FINAL_SUMMARY.md)** - Rundy 1-3 summary

---

## ⚡ Performance & Load Testing

### Performance Tools

- **[LOAD_TESTING.md](./LOAD_TESTING.md)** - Complete load testing guide (Locust)
- **[locustfile.py](./locustfile.py)** - Load test scenarios (ChatbotUser, AdminUser, ApiStressTest)
- **[profile_api.py](./profile_api.py)** - Performance profiling tool (cProfile)
- **[benchmark.py](./benchmark.py)** - Performance benchmark script
- **[monitor.sh](./monitor.sh)** - Real-time performance monitoring
- **[.coveragerc](./.coveragerc)** - Coverage.py configuration

### Quick Commands

```bash
make profile              # Profile API endpoints
make load-test           # Run Locust load tests
make load-test-smoke     # Quick smoke test (10 users, 60s)
make coverage-report     # Generate coverage HTML report
```

---

## 📚 API Documentation

### Interactive Documentation

- **[Swagger UI](https://glass-core-467907-e9.ey.r.appspot.com/api-docs)** - Live interactive API docs ⭐
- **[src/docs/openapi.yaml](./src/docs/openapi.yaml)** - OpenAPI 3.0.3 specification
- **[SWAGGER_SETUP.md](./SWAGGER_SETUP.md)** - Swagger UI setup guide
- **[API_ENDPOINTS.md](./API_ENDPOINTS.md)** - Detailed endpoint documentation

### API Features

- **8+ Documented Endpoints** - Complete with examples
- **Try it out** - Test API directly in browser
- **Security Schemas** - API Key authentication
- **Request/Response Examples** - For all endpoints
- **Error Codes** - Documented error responses

### Quick Access

```bash
# Local
http://localhost:5000/api-docs

# Production
https://glass-core-467907-e9.ey.r.appspot.com/api-docs
```

---

## 🧪 Testing & Quality

### Testing

- **[README.md](./README.md#testing)** - Testing overview & commands
- **tests/test_chatbot.py** - 18 automated tests
- **tests/test_knowledge.py** - Knowledge base tests
- **smoke_tests.py** - Quick smoke tests

### Code Quality

- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Code style guidelines
- **[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)** - Community guidelines
- **[POPRAWKI_EKSPERT.md](./POPRAWKI_EKSPERT.md)** - Expert audit report (5.5→9.5/10)
- **[FINAL_AUDIT_COMPLETE.md](./FINAL_AUDIT_COMPLETE.md)** - Security audit results

---

## 🗺️ Roadmap & Development

### Planning

- **[ROADMAP_ROZWOJU - 18.11.25.md](./ROADMAP_ROZWOJU - 18.11.25.md)** - Future development roadmap
- **[README_PHASES_2_3_6_7.md](./README_PHASES_2_3_6_7.md)** - Phase implementation plan
- **[RUNDY_IMPLEMENTATION.md](./RUNDY_IMPLEMENTATION.md)** - Development rounds

### Updates System

- **[AUTO_UPDATE_GUIDE.md](./AUTO_UPDATE_GUIDE.md)** - Automatic update generation
- **generate-update.sh** - Update generator script
- **auto-update-hook.sh** - Git hook for auto-updates

---

## 💼 Enterprise

### SLA & Support

- **[SLA.md](./SLA.md)** - Service Level Agreement (99.5% uptime)
- **[SECURITY_POLICY.md](./SECURITY_POLICY.md)** - Security incident response
- **[DASHBOARD_AUDIT.md](./DASHBOARD_AUDIT.md)** - Dashboard audit results

### Documentation dla Użytkowników

- **[DOKUMENTACJA_UZYTKOWNIKA.md](./DOKUMENTACJA_UZYTKOWNIKA.md)** - User documentation (Polish)
- **[README_QUICK_START.md](./README_QUICK_START.md)** - Quick start guide
- **[README_SUCCESS.md](./README_SUCCESS.md)** - Success stories & metrics

---

## 🔗 External Resources

### Live Services

- **Production:** https://glass-core-467907-e9.ey.r.appspot.com
- **API Docs:** https://glass-core-467907-e9.ey.r.appspot.com/docs
- **GitHub Repo:** https://github.com/MrCanon19/novahouse-chatbot-api

### Tools & Services

- **Sentry:** Error monitoring (setup: [SETUP_MONITORING.md](./SETUP_MONITORING.md))
- **Upstash Redis:** Caching (setup: [REDIS_SETUP.md](./REDIS_SETUP.md))
- **Monday.com:** CRM integration ([MONDAY_INTEGRATION.md](./MONDAY_INTEGRATION.md))
- **Booksy:** Booking system ([BOOKSY_INTEGRATION.md](./BOOKSY_INTEGRATION.md))

---

## 📞 Pomoc & Support

### Gdzie szukać pomocy?

1. **Quick fixes:** [README.md](./README.md) - FAQ i troubleshooting
2. **Setup issues:** [SETUP_MONITORING.md](./SETUP_MONITORING.md) - Troubleshooting section
3. **Docker problems:** [DOCKER.md](./DOCKER.md) - Docker troubleshooting
4. **Security concerns:** [SECURITY_POLICY.md](./SECURITY_POLICY.md) - security@novahouse.pl
5. **Bugs:** [GitHub Issues](https://github.com/MrCanon19/novahouse-chatbot-api/issues)
6. **Features:** [GitHub Discussions](https://github.com/MrCanon19/novahouse-chatbot-api/discussions)

### Kontakt

- **Email:** support@novahouse.pl
- **Team Lead:** Michał Marini (@MrCanon19)
- **Response time:** 4h (business hours)

---

## 🎯 Recommended Reading Order

### Dla nowych użytkowników:

1. **[README.md](./README.md)** - Overview i quick start
2. **[DOCKER.md](./DOCKER.md)** - Uruchomienie lokalnie
3. **[API_ENDPOINTS.md](./API_ENDPOINTS.md)** - Poznaj API
4. **[LINKI_NOTION.md](./LINKI_NOTION.md)** - Zobacz live demo

### Dla developerów:

1. **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Development workflow
2. **[DOCKER.md](./DOCKER.md)** - Local development setup
3. **[SETUP_MONITORING.md](./SETUP_MONITORING.md)** - Production-grade setup
4. **[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)** - Community guidelines

### Dla administratorów:

1. **[INSTRUKCJA_WDROZENIA_GCP.md](./INSTRUKCJA_WDROZENIA_GCP.md)** - Deployment
2. **[BACKUP_SYSTEM.md](./BACKUP_SYSTEM.md)** - Backup strategy
3. **[ROTATE_CREDENTIALS.md](./ROTATE_CREDENTIALS.md)** - Security maintenance
4. **[SLA.md](./SLA.md)** - Service commitments

---

**Last updated:** 18 listopada 2025  
**Total documents:** 50+  
**Version:** 2.3.0 "Production Ready"
