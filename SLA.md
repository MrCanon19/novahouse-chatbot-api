# 🤝 Porozumienie o Poziomie Usług (SLA)

## 📊 NovaHouse Chatbot API - Service Level Agreement

**Wersja:** 1.0  
**Data obowiązywania:** 18 listopada 2025  
**Dotyczy:** NovaHouse Chatbot API v2.3+

---

## 🎯 Dostępność (Uptime)

### Cel: 99.5% uptime miesięcznie

| Tier            | Uptime | Downtime/miesiąc | Status          |
| --------------- | ------ | ---------------- | --------------- |
| **Production**  | 99.5%  | ~3.6 godz        | ✅ Gwarantowane |
| **Development** | 95.0%  | ~36 godz         | ⚠️ Best effort  |

**Wykluczenia z uptime:**

- Planowane maintenance (z 48h notice)
- Force majeure (awarie GCP datacenter)
- Ataki DDoS > 1M requests/min
- Problemy po stronie klienta

### Monitoring

Sprawdź aktualny status:

```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/api/health
```

**Status page:** https://stats.uptimerobot.com/novahouse _(coming soon)_

---

## ⚡ Wydajność

### Response Time Targets

| Endpoint Type      | Target | P95    | P99    |
| ------------------ | ------ | ------ | ------ |
| **Health check**   | <100ms | <150ms | <200ms |
| **Chat API**       | <500ms | <800ms | <1s    |
| **Knowledge base** | <300ms | <500ms | <700ms |
| **Analytics**      | <1s    | <2s    | <3s    |
| **File upload**    | <2s    | <4s    | <6s    |

**Load capacity:**

- 100 concurrent users (sustained)
- 1000 requests/minute (burst)
- 10MB max upload size

---

## 🔒 Bezpieczeństwo

### Gwarancje

✅ **Encryption:**

- TLS 1.3 for all API calls
- Encrypted data at rest (GCP)
- Secure credential storage

✅ **Backup:**

- Automated daily backups (3AM UTC)
- 30-day retention
- GDPR-compliant export

✅ **Compliance:**

- RODO/GDPR compliant
- SOC 2 Type II (via GCP)
- ISO 27001 (via GCP)

### Incident Response Times

| Severity                | Response | Resolution  |
| ----------------------- | -------- | ----------- |
| **Critical** (API down) | 1h       | 4h          |
| **High** (degraded)     | 4h       | 24h         |
| **Medium** (bug)        | 24h      | 5 dni       |
| **Low** (enhancement)   | 7 dni    | Best effort |

---

## 📞 Support

### Kanały wsparcia

| Kanał                  | Czas odpowiedzi | Dostępność |
| ---------------------- | --------------- | ---------- |
| **Email**              | 4h (business)   | 24/7       |
| **GitHub Issues**      | 24h             | 24/7       |
| **Slack** (Enterprise) | 1h              | 9-17 CET   |
| **Phone** (Critical)   | 30min           | 24/7       |

**Support email:** support@novahouse.pl  
**Emergency hotline:** +48 XXX XXX XXX _(Enterprise only)_

### Eskalacja

1. **L1 Support** - Podstawowe pytania (4h response)
2. **L2 Support** - Techniczne issues (24h response)
3. **L3 Support** - Critical bugs (1h response)
4. **DevOps** - Infrastructure (30min response)

---

## 📊 Raportowanie

### Comiesięczne raporty zawierają:

- ✅ Uptime (actual vs target)
- ✅ Performance metrics (P50/P95/P99)
- ✅ Incident summary
- ✅ Feature releases
- ✅ Capacity planning

**Dostęp:** Automatyczny email pierwszego dnia miesiąca

---

## 💰 SLA Credits (Enterprise)

W przypadku naruszenia SLA:

| Uptime Achieved | Credit                 |
| --------------- | ---------------------- |
| < 99.5%         | 10% miesięcznej opłaty |
| < 99.0%         | 25% miesięcznej opłaty |
| < 95.0%         | 50% miesięcznej opłaty |

**Warunki:**

- Credit request w ciągu 30 dni
- Minimum $100 miesięczna opłata
- Max 100% refund per miesiąc

---

## 🔄 Maintenance Windows

**Planned maintenance:**

- **Częstotliwość:** 1x miesięcznie
- **Dzień:** Niedziela, 2:00-4:00 CET
- **Powiadomienie:** 48h wcześniej (email)
- **Max duration:** 2 godziny

**Emergency maintenance:**

- Security patches: immediate (no notice)
- Critical bugs: 2h notice

---

## 📈 Capacity & Limits

### Rate Limits

| Tier           | Requests/minute | Requests/day |
| -------------- | --------------- | ------------ |
| **Free**       | 60              | 1,000        |
| **Starter**    | 300             | 10,000       |
| **Pro**        | 1,000           | 50,000       |
| **Enterprise** | Custom          | Custom       |

**HTTP Status 429:** Too Many Requests  
**Retry-After header:** Seconds until reset

### Storage Limits

- **Database:** 10GB (Pro), 50GB (Enterprise)
- **Files:** 1GB (Pro), 10GB (Enterprise)
- **Backups:** 30 days retention

---

## 🔧 Deprecation Policy

### Wersjonowanie API

- **Major versions:** Supported for 12 miesięcy
- **Minor versions:** Supported for 6 miesięcy
- **Deprecation notice:** 90 dni przed EOL
- **Security patches:** 6 miesięcy post-EOL

**Current support:**

- v2.3.x ✅ (Current, full support)
- v2.2.x ⚠️ (Critical patches only, EOL 2026-05-18)
- v2.1.x ❌ (EOL, upgrade required)

---

## 📋 Changelog

### v1.0 (2025-11-18)

- Initial SLA document
- 99.5% uptime target
- Response time targets defined
- Support channels established

---

## 📞 Kontakt SLA

**SLA Manager:** Michał Marini  
**Email:** sla@novahouse.pl  
**Phone:** +48 XXX XXX XXX  
**Hours:** Mon-Fri 9:00-17:00 CET

**Review cycle:** Quarterly (Mar, Jun, Sep, Dec)  
**Next review:** 2026-02-01

---

## ⚖️ Prawne

Niniejsze SLA stanowi integralną część umowy o świadczenie usług.  
W przypadku sprzeczności z umową główną, pierwszeństwo ma umowa.

**Last updated:** 18 listopada 2025  
**Version:** 1.0
