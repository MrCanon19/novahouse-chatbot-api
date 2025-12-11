# 🐳 Docker Quick Start

## Szybkie uruchomienie z Docker Compose

### 1️⃣ Podstawowy setup (30 sekund)

```bash
# Sklonuj repo
git clone https://github.com/MrCanon19/chatbot-api.git
cd chatbot-api

# Skopiuj przykładowy config
cp .env.example .env

# Edytuj .env (uzupełnij API keys)
nano .env

# Uruchom wszystko (PostgreSQL + Redis + API)
docker-compose up -d
```

### 2️⃣ Sprawdź status

```bash
# Status kontenerów
docker-compose ps

# Logi aplikacji
docker-compose logs -f app

# Health check
curl http://localhost:8080/api/health
```

### 3️⃣ Zatrzymanie

```bash
# Stop wszystkich kontenerów
docker-compose down

# Stop + usuń volumes (czyści bazę!)
docker-compose down -v
```

---

## 🔧 Szczegółowe komendy

### Development workflow

```bash
# Rebuild po zmianach w kodzie
docker-compose up -d --build

# Wejdź do kontenera
docker-compose exec app bash

# Uruchom testy
docker-compose exec app pytest tests/

# Sprawdź logi konkretnego serwisu
docker-compose logs -f postgres
docker-compose logs -f redis
docker-compose logs -f app
```

### Database operations

```bash
# Backup bazy danych
docker-compose exec postgres pg_dump -U chatbot_user chatbot > backup.sql

# Restore z backupu
docker-compose exec -T postgres psql -U chatbot_user chatbot < backup.sql

# Połącz się z bazą
docker-compose exec postgres psql -U chatbot_user chatbot
```

### Redis operations

```bash
# Redis CLI
docker-compose exec redis redis-cli

# Check Redis keys
docker-compose exec redis redis-cli KEYS '*'

# Flush cache
docker-compose exec redis redis-cli FLUSHALL
```

---

## 🚀 Production Deployment

### Option 1: Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Create secrets
echo "prod-secret-key" | docker secret create secret_key -
echo "postgresql://..." | docker secret create database_url -

# Deploy stack
docker stack deploy -c docker-compose.yml novahouse
```

### Option 2: Kubernetes

```bash
# Build i push image
docker build -t novahouse-chatbot:2.3.0 .
docker tag novahouse-chatbot:2.3.0 gcr.io/glass-core-467907-e9/novahouse-chatbot:2.3.0
docker push gcr.io/glass-core-467907-e9/novahouse-chatbot:2.3.0

# Apply k8s manifests (create these first)
kubectl apply -f k8s/
```

### Option 3: Google Cloud Run

```bash
# Build z Cloud Build
gcloud builds submit --tag gcr.io/glass-core-467907-e9/novahouse-chatbot

# Deploy do Cloud Run
gcloud run deploy novahouse-chatbot \
  --image gcr.io/glass-core-467907-e9/novahouse-chatbot \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars "FLASK_ENV=production"
```

---

## 🔒 Security Best Practices

### 1. Nigdy nie commituj secrets

```bash
# .env jest w .gitignore
# docker-compose.yml zawiera tylko placeholders
# Użyj Docker Secrets lub Kubernetes Secrets w produkcji
```

### 2. Use non-root user

```dockerfile
# Już skonfigurowane w Dockerfile
USER appuser
```

### 3. Skanuj vulnerabilities

```bash
# Skanuj image przed deployem
docker scan novahouse-chatbot:2.3.0

# Lub użyj Trivy
trivy image novahouse-chatbot:2.3.0
```

### 4. Multi-stage builds (opcjonalne)

```dockerfile
# Dockerfile.prod - mniejszy image
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["gunicorn", "--config", "gunicorn.conf.py", "main:app"]
```

---

## 📊 Monitoring w Docker

### Docker stats

```bash
# Real-time stats
docker stats novahouse-api

# Export metrics
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Health checks

```bash
# Manual health check
docker inspect --format='{{json .State.Health}}' novahouse-api | jq

# Auto restart on unhealthy
# (już skonfigurowane w docker-compose.yml)
```

### Integrate with Prometheus

```yaml
# docker-compose.yml - add cadvisor
cadvisor:
  image: gcr.io/cadvisor/cadvisor:latest
  ports:
    - "8081:8080"
  volumes:
    - /:/rootfs:ro
    - /var/run:/var/run:ro
    - /sys:/sys:ro
    - /var/lib/docker/:/var/lib/docker:ro
```

---

## 🐛 Troubleshooting

### Port już zajęty

```bash
# Sprawdź co używa portu 8080
lsof -i :8080

# Zmień port w docker-compose.yml
ports:
  - "8081:8080"  # Host:Container
```

### Brak połączenia z bazą

```bash
# Sprawdź czy postgres działa
docker-compose ps postgres

# Sprawdź logi
docker-compose logs postgres

# Restart postgres
docker-compose restart postgres
```

### Out of memory

```bash
# Dodaj limity w docker-compose.yml
deploy:
  resources:
    limits:
      memory: 1G
    reservations:
      memory: 512M
```

### Wolny build

```bash
# Use BuildKit (szybszy)
DOCKER_BUILDKIT=1 docker-compose build

# Cache layers
docker-compose build --no-cache  # tylko gdy potrzeba rebuild
```

---

## 📚 Dodatkowe zasoby

- **Dockerfile:** Definicja image aplikacji
- **docker-compose.yml:** Orchestration (app + db + redis)
- **.dockerignore:** Co pominąć podczas build
- **SETUP_MONITORING.md:** Sentry i Redis setup
- **CONTRIBUTING.md:** Development guidelines

---

## 🎯 Co dalej?

1. ✅ Uruchom lokalnie z `docker-compose up -d`
2. ✅ Przetestuj API endpoints
3. ✅ Sprawdź monitoring (logi, health checks)
4. ✅ Deploy na produkcję (GCP, AWS, Azure)
5. ✅ Setup CI/CD (GitHub Actions już gotowe)

**Happy Dockering! 🐳**
