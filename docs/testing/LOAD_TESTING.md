# 🚀 Load Testing Guide

## Overview

Load testing dla NovaHouse Chatbot API używa **Locust** - nowoczesnego narzędzia do testowania obciążenia napisanego w Pythonie.

## Quick Start

### 1. Instalacja Locust

```bash
pip install locust
# lub
make install-locust  # dodaj do Makefile
```

### 2. Uruchomienie Load Test

```bash
# Lokalne testy
locust -f locustfile.py --host=http://localhost:5000

# Produkcyjne testy
locust -f locustfile.py --host=https://glass-core-467907-e9.ey.r.appspot.com

# Headless mode (bez GUI)
locust -f locustfile.py --headless --users 100 --spawn-rate 10 --run-time 60s
```

### 3. Otwórz Web UI

Przejdź do: http://localhost:8089

## 📊 Test Scenarios

### ChatbotUser (Podstawowy użytkownik)

- **Waga**: 70% ruchu
- **Operacje**:
  - Wysyłanie wiadomości (task weight: 10)
  - Health check (task weight: 5)
  - Wyszukiwanie (task weight: 3)
  - Pobieranie analytics (task weight: 2)
  - Tworzenie leadów (task weight: 1)
- **Wait time**: 1-3 sekundy między requestami

### AdminUser (Dashboard admin)

- **Waga**: 20% ruchu
- **Operacje**:
  - Przeglądanie dashboardu (task weight: 5)
  - Lista leadów (task weight: 3)
  - Szczegółowe analytics (task weight: 2)
- **Wait time**: 2-5 sekund między requestami

### ApiStressTest (Stress testing)

- **Waga**: 10% ruchu
- **Operacje**:
  - Agresywne spamowanie endpointów
  - Minimalne czasy oczekiwania (0.1-0.5s)
- **Uwaga**: Używaj ostrożnie!

## 🎯 Recommended Test Plans

### 1. Smoke Test (Quick validation)

```bash
locust -f locustfile.py --headless \
  --users 10 \
  --spawn-rate 2 \
  --run-time 60s \
  --host=http://localhost:5000
```

**Cel**: Sprawdzenie czy API odpowiada poprawnie pod minimalnym obciążeniem.

### 2. Load Test (Normal traffic)

```bash
locust -f locustfile.py --headless \
  --users 50 \
  --spawn-rate 5 \
  --run-time 300s \
  --host=https://glass-core-467907-e9.ey.r.appspot.com
```

**Cel**: Symulacja normalnego ruchu użytkowników (50 concurrent users).

### 3. Stress Test (Peak traffic)

```bash
locust -f locustfile.py --headless \
  --users 200 \
  --spawn-rate 20 \
  --run-time 600s \
  --host=https://glass-core-467907-e9.ey.r.appspot.com
```

**Cel**: Test zachowania pod wysokim obciążeniem (200 users).

### 4. Spike Test (Sudden traffic spike)

```bash
locust -f locustfile.py --headless \
  --users 500 \
  --spawn-rate 100 \
  --run-time 180s \
  --host=https://glass-core-467907-e9.ey.r.appspot.com
```

**Cel**: Test odpowiedzi na nagły wzrost ruchu.

### 5. Endurance Test (Long-running)

```bash
locust -f locustfile.py --headless \
  --users 30 \
  --spawn-rate 3 \
  --run-time 3600s \
  --host=https://glass-core-467907-e9.ey.r.appspot.com
```

**Cel**: Test stabilności systemu przez długi czas (1 godzina).

## 📈 Metryki do obserwacji

### ✅ Dobre wartości (targets):

- **Response time (median)**: < 200ms
- **Response time (95th percentile)**: < 500ms
- **Requests per second**: > 100 RPS
- **Failure rate**: < 1%

### ⚠️ Warning signs:

- Response time > 1s
- Failure rate > 5%
- RPS spadające podczas testu
- Memory leaks (rosnące zużycie RAM)

### 🚨 Critical issues:

- Response time > 3s
- Failure rate > 10%
- Timeouts
- 5xx errors

## 📊 Przykładowe wyniki

### Lokalne testy (MacBook Pro M1):

```
Type     Name                   # reqs  # fails  Median  95%ile  Avg     Min  Max
POST     /api/chatbot/message   1000    0        45ms    120ms   52ms    23ms 450ms
GET      /api/health            500     0        12ms    35ms    15ms    8ms  89ms
GET      /api/knowledge/search  300     0        89ms    230ms   105ms   45ms 680ms
```

### Produkcja (GCP App Engine):

```
Type     Name                   # reqs  # fails  Median  95%ile  Avg     Min  Max
POST     /api/chatbot/message   10000   5        120ms   380ms   145ms   67ms 2100ms
GET      /api/health            5000    0        45ms    95ms    52ms    28ms 340ms
GET      /api/knowledge/search  3000    2        180ms   520ms   215ms   89ms 1800ms
```

## 🔧 Konfiguracja testów

### Customizacja w `locustfile.py`:

```python
# Zmiana wait time
wait_time = between(0.5, 2)  # Szybsze requesty

# Zmiana wag tasków
@task(20)  # Więcej requestów do tego endpointu
def send_message(self):
    ...

# Dodanie nowego scenariusza
@task(3)
def custom_endpoint(self):
    self.client.get("/api/custom/endpoint")
```

## 🐳 Docker Load Testing

```yaml
# docker-compose.loadtest.yml
version: "3.8"
services:
  locust-master:
    image: locustio/locust
    ports:
      - "8089:8089"
    volumes:
      - ./locustfile.py:/mnt/locust/locustfile.py
    command: -f /mnt/locust/locustfile.py --master

  locust-worker:
    image: locustio/locust
    volumes:
      - ./locustfile.py:/mnt/locust/locustfile.py
    command: -f /mnt/locust/locustfile.py --worker --master-host locust-master
    deploy:
      replicas: 4
```

```bash
# Uruchomienie distributed load test
docker-compose -f docker-compose.loadtest.yml up --scale locust-worker=4
```

## 📝 Best Practices

### 1. **Testuj stopniowo**

- Zacznij od małych liczb (10 users)
- Zwiększaj stopniowo (50 → 100 → 200)
- Obserwuj metryki na każdym etapie

### 2. **Monitor infrastrukturę**

```bash
# Podczas testów monitoruj:
make monitor-prod  # Response times
htop              # CPU/RAM
docker stats      # Jeśli używasz Dockera
```

### 3. **Testuj różne scenariusze**

- Read-heavy (80% GET requests)
- Write-heavy (80% POST requests)
- Mixed workload (50/50)
- Peak hours simulation

### 4. **Analizuj wyniki**

- Eksportuj wyniki do CSV
- Porównuj między wersjami
- Sprawdź logi aplikacji
- Monitoruj Sentry errors

### 5. **Nie testuj produkcji bez zgody!**

⚠️ Load testing może:

- Zwiększyć koszty GCP
- Trigger rate limity
- Wpłynąć na prawdziwych użytkowników
- Stworzyć tysiące fake leadów w bazie

## 🔍 Debugging

### Problem: High failure rate

```bash
# Check application logs
gcloud app logs tail -s default

# Check Sentry
# https://sentry.io/organizations/novahouse/issues/
```

### Problem: Slow responses

```bash
# Profile the API
python profile_api.py --endpoint chatbot

# Check database queries
# Enable SQL query logging in Flask-SQLAlchemy
```

### Problem: Timeouts

```bash
# Increase gunicorn timeout
# In app.yaml or gunicorn.conf.py:
timeout = 120
```

## 📚 Resources

- [Locust Documentation](https://docs.locust.io/)
- [Load Testing Best Practices](https://loadtesting.io/)
- [GCP App Engine Performance](https://cloud.google.com/appengine/docs/standard/python3/testing-and-deploying-your-app)

## 🎯 Next Steps

1. Run initial smoke test: `make load-test-smoke`
2. Analyze results and set baselines
3. Add load tests to CI/CD (optional)
4. Create performance budgets
5. Set up alerts for performance degradation

---

**Happy Load Testing! 🚀**
