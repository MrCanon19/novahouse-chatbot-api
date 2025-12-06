# Instrukcja Wdrożenia Chatbota NovaHouse na Google Cloud Platform

**Autor:** Manus AI  
**Data:** 11 sierpnia 2025  
**Wersja:** 1.0  
**Projekt:** NovaHouse Chatbot - Wdrożenie Produkcyjne

---

## Spis Treści

1. [Wprowadzenie](#wprowadzenie)
2. [Wymagania Wstępne](#wymagania-wstępne)
3. [Przygotowanie Środowiska Google Cloud Platform](#przygotowanie-środowiska-google-cloud-platform)
4. [Konfiguracja Projektu](#konfiguracja-projektu)
5. [Wdrożenie na App Engine](#wdrożenie-na-app-engine)
6. [Weryfikacja Wdrożenia](#weryfikacja-wdrożenia)
7. [Konfiguracja Domeny Własnej](#konfiguracja-domeny-własnej)
8. [Monitorowanie i Logowanie](#monitorowanie-i-logowanie)
9. [Zarządzanie Kosztami](#zarządzanie-kosztami)
10. [Rozwiązywanie Problemów](#rozwiązywanie-problemów)
11. [Bezpieczeństwo](#bezpieczeństwo)
12. [Backup i Odzyskiwanie](#backup-i-odzyskiwanie)

---

## Wprowadzenie

Niniejsza instrukcja zawiera szczegółowy przewodnik wdrożenia chatbota NovaHouse na platformie Google Cloud Platform (GCP) przy użyciu usługi App Engine. Chatbot został zaprojektowany jako aplikacja Flask z bazą danych SQLite, zoptymalizowana pod kątem stabilności i skalowalności w środowisku chmurowym.

### Architektura Rozwiązania

Chatbot NovaHouse składa się z następujących komponentów:

- **Frontend:** Responsywny interfejs webowy HTML/CSS/JavaScript
- **Backend:** Aplikacja Flask z API REST
- **Baza Danych:** SQLite z modelami dla intencji, encji, konwersacji i leadów
- **AI Engine:** Własny silnik NLU (Natural Language Understanding) do klasyfikacji intencji
- **Hosting:** Google App Engine Standard Environment

### Korzyści z Wdrożenia na GCP

Google Cloud Platform oferuje szereg korzyści dla aplikacji chatbotowych:

- **Automatyczne skalowanie:** App Engine automatycznie dostosowuje zasoby do obciążenia
- **Wysoką dostępność:** 99.95% SLA gwarantuje ciągłość działania
- **Bezpieczeństwo:** Wbudowane mechanizmy ochrony i szyfrowania
- **Integrację:** Łatwa integracja z innymi usługami Google Cloud
- **Koszt-efektywność:** Płatność tylko za rzeczywiście wykorzystane zasoby

---

## Wymagania Wstępne

Przed rozpoczęciem wdrożenia upewnij się, że spełniasz następujące wymagania:

### Konto Google Cloud Platform

1. **Aktywne konto Google Cloud Platform** z włączoną płatnością
2. **Projekt GCP** z unikalną nazwą (np. `novahouse-chatbot-prod`)
3. **Włączone API:** App Engine Admin API, Cloud Build API, Cloud Logging API

### Narzędzia Lokalne

1. **Google Cloud SDK (gcloud CLI)** - najnowsza wersja
2. **Python 3.11** lub nowszy
3. **Git** do zarządzania kodem źródłowym
4. **Edytor tekstu** (VS Code, PyCharm, itp.)

### Uprawnienia

Użytkownik wykonujący wdrożenie musi posiadać następujące role w projekcie GCP:

- `App Engine Admin`
- `Cloud Build Editor`
- `Storage Admin`
- `Logging Admin`

### Budżet i Limity

Zalecane ustawienia budżetu dla środowiska produkcyjnego:

- **Miesięczny budżet:** 400 PLN (zgodnie z wymaganiami NovaHouse)
- **Alerty budżetowe:** 50%, 80%, 90% wykorzystania
- **Limity API:** Domyślne limity App Engine są wystarczające dla większości zastosowań

---


## Przygotowanie Środowiska Google Cloud Platform

### Krok 1: Utworzenie Nowego Projektu

Jeśli nie posiadasz jeszcze dedykowanego projektu dla chatbota, utwórz nowy projekt w Google Cloud Console:

1. **Przejdź do Google Cloud Console:** https://console.cloud.google.com
2. **Kliknij na selektor projektów** w górnej części strony
3. **Wybierz "NEW PROJECT"**
4. **Wprowadź dane projektu:**
   - **Project name:** `NovaHouse Chatbot Production`
   - **Project ID:** `novahouse-chatbot-prod` (musi być globalnie unikalny)
   - **Organization:** Wybierz swoją organizację (jeśli dotyczy)
5. **Kliknij "CREATE"**

### Krok 2: Włączenie Wymaganych API

Po utworzeniu projektu, włącz niezbędne API:

```bash
# Zaloguj się do gcloud CLI
gcloud auth login

# Ustaw aktywny projekt
gcloud config set project novahouse-chatbot-prod

# Włącz wymagane API
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable logging.googleapis.com
gcloud services enable monitoring.googleapis.com
```

### Krok 3: Inicjalizacja App Engine

App Engine wymaga jednorazowej inicjalizacji w projekcie:

```bash
# Inicjalizuj App Engine (wybierz region europe-west3 dla Polski)
gcloud app create --region=europe-west3
```

**Ważne:** Wybór regionu jest nieodwracalny. Dla polskich użytkowników zalecamy:
- `europe-west3` (Frankfurt) - najniższa latencja
- `europe-west1` (Belgia) - alternatywa

### Krok 4: Konfiguracja Uprawnień

Upewnij się, że Twoje konto ma odpowiednie uprawnienia:

```bash
# Sprawdź aktualne uprawnienia
gcloud projects get-iam-policy novahouse-chatbot-prod

# Jeśli potrzebujesz dodać uprawnienia (zastąp YOUR_EMAIL swoim adresem)
gcloud projects add-iam-policy-binding novahouse-chatbot-prod \
    --member="user:YOUR_EMAIL@gmail.com" \
    --role="roles/appengine.appAdmin"
```

### Krok 5: Konfiguracja Budżetu i Alertów

Aby kontrolować koszty, skonfiguruj budżet i alerty:

1. **Przejdź do Billing w Cloud Console**
2. **Wybierz "Budgets & alerts"**
3. **Kliknij "CREATE BUDGET"**
4. **Skonfiguruj budżet:**
   - **Name:** `NovaHouse Chatbot Monthly Budget`
   - **Budget amount:** 400 PLN
   - **Time range:** Monthly
   - **Projects:** Wybierz `novahouse-chatbot-prod`
5. **Ustaw alerty na:** 50%, 80%, 90%
6. **Dodaj adresy email** do powiadomień

### Krok 6: Weryfikacja Konfiguracji

Sprawdź, czy wszystko zostało poprawnie skonfigurowane:

```bash
# Sprawdź status App Engine
gcloud app describe

# Sprawdź włączone API
gcloud services list --enabled

# Sprawdź aktualny projekt
gcloud config get-value project
```

Jeśli wszystkie polecenia wykonują się bez błędów, środowisko GCP jest gotowe do wdrożenia.

---

## Konfiguracja Projektu

### Struktura Projektu

Przed wdrożeniem upewnij się, że struktura projektu jest zgodna z wymaganiami App Engine:

```
novahouse_chatbot_api/
├── app.yaml                 # Konfiguracja App Engine
├── main.py                  # Punkt wejścia dla App Engine
├── requirements.txt         # Zależności Python
├── .gcloudignore           # Pliki do wykluczenia z wdrożenia
├── cloudbuild.yaml         # Konfiguracja Cloud Build (opcjonalne)
├── gunicorn.conf.py        # Konfiguracja Gunicorn
├── src/
│   ├── __init__.py
│   ├── main.py             # Główna aplikacja Flask
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── chatbot.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── chatbot.py
│   │   └── health.py
│   ├── static/
│   │   └── chatbot.html    # Frontend chatbota
│   └── database/
│       └── app.db          # Baza danych SQLite
└── venv/                   # Środowisko wirtualne (wykluczane z wdrożenia)
```

### Weryfikacja Plików Konfiguracyjnych

#### app.yaml

Sprawdź, czy plik `app.yaml` zawiera poprawną konfigurację:

```yaml
runtime: python311

service: default

env_variables:
  FLASK_ENV: production
  SECRET_KEY: "asdf#FGSgvasgf$5$WGT"

automatic_scaling:
  min_instances: 1
  max_instances: 10
  target_cpu_utilization: 0.6

resources:
  cpu: 1
  memory_gb: 0.5
  disk_size_gb: 10

handlers:
- url: /static
  static_dir: src/static

- url: /.*
  script: auto

skip_files:
- ^(.*/)?#.*#$
- ^(.*/)?.*~$
- ^(.*/)?.*\.py[co]$
- ^(.*/)?.*/RCS/.*$
- ^(.*/)?\..*$
- ^(.*/)?venv/.*$
- ^(.*/)?__pycache__/.*$
- ^(.*/)?\.git/.*$
- ^(.*/)?\.gitignore$
- ^(.*/)?README\.md$
- ^(.*/)?\.pytest_cache/.*$
- ^(.*/)?tests/.*$
```

#### requirements.txt

Upewnij się, że wszystkie zależności są zdefiniowane:

```
blinker==1.9.0
click==8.2.1
Flask==3.1.1
flask-cors==6.0.0
Flask-SQLAlchemy==3.1.1
gunicorn==21.2.0
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
SQLAlchemy==2.0.41
typing_extensions==4.14.0
Werkzeug==3.1.3
```

#### main.py (punkt wejścia)

Główny plik dla App Engine:

```python
#!/usr/bin/env python3
"""
Główny plik aplikacji dla Google App Engine
"""

import os
import sys

# Dodanie ścieżki do modułów
sys.path.insert(0, os.path.dirname(__file__))

# Import aplikacji Flask
from src.main import app

# Dla App Engine, aplikacja musi być dostępna jako 'app'
if __name__ == '__main__':
    # Dla lokalnego uruchomienia
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)
```

### Testowanie Lokalne

Przed wdrożeniem na GCP, przetestuj aplikację lokalnie:

```bash
# Przejdź do katalogu projektu
cd novahouse_chatbot_api

# Utwórz środowisko wirtualne (jeśli nie istnieje)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate     # Windows

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom aplikację lokalnie
python main.py
```

Aplikacja powinna być dostępna pod adresem `http://localhost:8080`. Przetestuj podstawowe funkcjonalności:

1. **Health check:** `http://localhost:8080/api/health`
2. **Interfejs chatbota:** `http://localhost:8080/static/chatbot.html`
3. **API chatbota:** POST do `http://localhost:8080/api/chatbot/chat`

---


## Wdrożenie na App Engine

### Metoda 1: Wdrożenie Bezpośrednie (Zalecane)

Najprostszy sposób wdrożenia aplikacji na App Engine:

```bash
# Upewnij się, że jesteś w katalogu projektu
cd novahouse_chatbot_api

# Sprawdź aktualny projekt GCP
gcloud config get-value project

# Jeśli potrzebujesz zmienić projekt
gcloud config set project novahouse-chatbot-prod

# Wdróż aplikację
gcloud app deploy app.yaml --quiet
```

Proces wdrożenia może potrwać 5-10 minut. Po zakończeniu otrzymasz URL aplikacji.

### Metoda 2: Wdrożenie z Cloud Build

Dla bardziej zaawansowanego procesu CI/CD:

```bash
# Wdróż używając Cloud Build
gcloud builds submit --config cloudbuild.yaml .
```

### Monitorowanie Procesu Wdrożenia

Podczas wdrożenia możesz monitorować postęp:

```bash
# Sprawdź status wdrożenia
gcloud app versions list

# Sprawdź logi wdrożenia
gcloud app logs tail -s default
```

### Weryfikacja Wdrożenia

Po zakończeniu wdrożenia, sprawdź czy aplikacja działa poprawnie:

```bash
# Pobierz URL aplikacji
gcloud app browse

# Lub sprawdź URL ręcznie
echo "https://$(gcloud config get-value project).appspot.com"
```

### Testowanie Wdrożonej Aplikacji

1. **Health Check:**
   ```bash
   curl https://novahouse-chatbot-prod.appspot.com/api/health
   ```

2. **Interfejs Chatbota:**
   Otwórz w przeglądarce: `https://novahouse-chatbot-prod.appspot.com/static/chatbot.html`

3. **Test API Chatbota:**
   ```bash
   curl -X POST https://novahouse-chatbot-prod.appspot.com/api/chatbot/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Cześć, chciałbym poznać pakiety wykończeniowe"}'
   ```

### Zarządzanie Wersjami

App Engine automatycznie tworzy nowe wersje przy każdym wdrożeniu:

```bash
# Lista wszystkich wersji
gcloud app versions list

# Przełączanie ruchu między wersjami
gcloud app services set-traffic default --splits=v1=100

# Usuwanie starych wersji
gcloud app versions delete v1 v2 --service=default
```

---

## Weryfikacja Wdrożenia

### Testy Funkcjonalne

Po wdrożeniu wykonaj pełny zestaw testów funkcjonalnych:

#### Test 1: Health Check

```bash
# Test podstawowego health check
curl -i https://novahouse-chatbot-prod.appspot.com/api/health

# Oczekiwana odpowiedź:
# HTTP/2 200
# {
#   "status": "healthy",
#   "database": "connected",
#   "intents_loaded": 17,
#   "entities_loaded": 5,
#   "service": "novahouse-chatbot"
# }
```

#### Test 2: Interfejs Użytkownika

1. Otwórz `https://novahouse-chatbot-prod.appspot.com/static/chatbot.html`
2. Sprawdź czy strona ładuje się poprawnie
3. Przetestuj responsywność na różnych urządzeniach
4. Sprawdź czy wszystkie elementy UI działają

#### Test 3: Funkcjonalność Chatbota

Przetestuj różne scenariusze konwersacji:

```bash
# Test powitania
curl -X POST https://novahouse-chatbot-prod.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Cześć"}'

# Test pytania o pakiety
curl -X POST https://novahouse-chatbot-prod.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Jakie macie pakiety wykończeniowe?"}'

# Test pytania o ceny
curl -X POST https://novahouse-chatbot-prod.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Ile kosztuje pakiet waniliowy?"}'

# Test umówienia spotkania
curl -X POST https://novahouse-chatbot-prod.appspot.com/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Chciałbym umówić spotkanie"}'
```

#### Test 4: Wydajność i Dostępność

```bash
# Test czasu odpowiedzi
time curl https://novahouse-chatbot-prod.appspot.com/api/health

# Test obciążenia (wymaga narzędzia ab - Apache Bench)
ab -n 100 -c 10 https://novahouse-chatbot-prod.appspot.com/api/health
```

### Testy Bezpieczeństwa

#### Test HTTPS

```bash
# Sprawdź czy HTTPS jest wymuszane
curl -I http://novahouse-chatbot-prod.appspot.com/api/health

# Powinno przekierować na HTTPS (301/302)
```

#### Test CORS

```bash
# Test nagłówków CORS
curl -H "Origin: https://example.com" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     https://novahouse-chatbot-prod.appspot.com/api/chatbot/chat
```

### Monitoring i Alerty

Po wdrożeniu skonfiguruj monitoring:

1. **Przejdź do Cloud Monitoring** w GCP Console
2. **Utwórz dashboard** dla aplikacji
3. **Skonfiguruj alerty** dla:
   - Wysokie wykorzystanie CPU (>80%)
   - Duża liczba błędów HTTP (>5%)
   - Długi czas odpowiedzi (>2s)
   - Niedostępność aplikacji

#### Przykładowa konfiguracja alertu:

```yaml
# alert-policy.yaml
displayName: "NovaHouse Chatbot High Error Rate"
conditions:
  - displayName: "HTTP 5xx errors"
    conditionThreshold:
      filter: 'resource.type="gae_app" AND metric.type="appengine.googleapis.com/http/server_response_count"'
      comparison: COMPARISON_GREATER_THAN
      thresholdValue: 10
      duration: 300s
```

---

## Konfiguracja Domeny Własnej

### Dodanie Domeny Niestandardowej

Jeśli chcesz używać własnej domeny zamiast `*.appspot.com`:

1. **Przejdź do App Engine > Settings > Custom domains**
2. **Kliknij "Add a custom domain"**
3. **Wprowadź domenę** (np. `chatbot.novahouse.pl`)
4. **Zweryfikuj własność domeny**
5. **Skonfiguruj rekordy DNS**

### Konfiguracja DNS

Dodaj następujące rekordy DNS w panelu swojego dostawcy domeny:

```
# Dla domeny głównej
chatbot.novahouse.pl.    A    216.239.32.21
chatbot.novahouse.pl.    A    216.239.34.21
chatbot.novahouse.pl.    A    216.239.36.21
chatbot.novahouse.pl.    A    216.239.38.21

# Dla subdomeny www
www.chatbot.novahouse.pl.    CNAME    ghs.googlehosted.com.
```

### SSL/TLS

Google automatycznie zapewnia certyfikaty SSL dla domen niestandardowych:

1. **Certyfikaty są automatycznie generowane** przez Google
2. **Odnowienie jest automatyczne**
3. **Wymuszanie HTTPS** jest domyślnie włączone

### Weryfikacja Domeny

Po konfiguracji DNS (może potrwać do 48 godzin):

```bash
# Sprawdź czy domena działa
curl -I https://chatbot.novahouse.pl/api/health

# Sprawdź certyfikat SSL
openssl s_client -connect chatbot.novahouse.pl:443 -servername chatbot.novahouse.pl
```

---

## Monitorowanie i Logowanie

### Cloud Logging

App Engine automatycznie przesyła logi do Cloud Logging:

```bash
# Przeglądanie logów w czasie rzeczywistym
gcloud app logs tail -s default

# Przeglądanie logów z określonego okresu
gcloud app logs read --since="2025-08-11 10:00:00"

# Filtrowanie logów po poziomie
gcloud app logs read --filter="severity>=ERROR"
```

### Structured Logging

Dla lepszego monitorowania, skonfiguruj structured logging w aplikacji Flask:

```python
import logging
import json
from google.cloud import logging as cloud_logging

# Konfiguracja Cloud Logging
client = cloud_logging.Client()
client.setup_logging()

# Przykład structured log
def log_chatbot_interaction(session_id, intent, response_time):
    logging.info(json.dumps({
        'event': 'chatbot_interaction',
        'session_id': session_id,
        'intent': intent,
        'response_time_ms': response_time,
        'timestamp': datetime.utcnow().isoformat()
    }))
```

### Metryki Niestandardowe

Utwórz niestandardowe metryki dla biznesowych KPI:

```python
from google.cloud import monitoring_v3

def record_conversation_metric(intent, success):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{PROJECT_ID}"

    # Utwórz punkt danych
    point = monitoring_v3.Point({
        "interval": {
            "end_time": {"seconds": int(time.time())}
        },
        "value": {"int64_value": 1}
    })

    # Wyślij metrykę
    client.create_time_series(
        name=project_name,
        time_series=[{
            "metric": {
                "type": "custom.googleapis.com/chatbot/conversations",
                "labels": {
                    "intent": intent,
                    "success": str(success)
                }
            },
            "resource": {
                "type": "gae_app",
                "labels": {"module_id": "default"}
            },
            "points": [point]
        }]
    )
```

### Dashboard Monitoring

Utwórz dashboard w Cloud Monitoring z następującymi wykresami:

1. **Liczba żądań na minutę**
2. **Czas odpowiedzi (percentyle 50, 95, 99)**
3. **Wskaźnik błędów HTTP**
4. **Wykorzystanie pamięci i CPU**
5. **Liczba aktywnych instancji**
6. **Niestandardowe metryki biznesowe**

---


## Zarządzanie Kosztami

### Analiza Kosztów

Regularne monitorowanie kosztów jest kluczowe dla utrzymania budżetu:

```bash
# Sprawdź aktualne koszty
gcloud billing budgets list

# Szczegółowa analiza kosztów
gcloud billing accounts list
```

### Optymalizacja Kosztów

#### Konfiguracja Automatycznego Skalowania

Dostosuj parametry skalowania w `app.yaml`:

```yaml
automatic_scaling:
  min_instances: 0          # Dla oszczędności - instancje mogą być wyłączone
  max_instances: 5          # Ograniczenie maksymalnej liczby instancji
  target_cpu_utilization: 0.8  # Wyższy próg dla mniejszej liczby instancji
  target_throughput_utilization: 0.8
  max_concurrent_requests: 10
```

#### Optymalizacja Zasobów

```yaml
resources:
  cpu: 1
  memory_gb: 0.5           # Minimalna wymagana pamięć
  disk_size_gb: 10         # Tylko niezbędna przestrzeń dyskowa
```

#### Harmonogram Ruchu

Dla aplikacji z przewidywalnym ruchem, rozważ konfigurację harmonogramu:

```yaml
# Przykład dla aplikacji biznesowej (8:00-18:00)
automatic_scaling:
  min_instances: 1         # W godzinach pracy
  max_instances: 5
  # Poza godzinami pracy min_instances może być 0
```

### Monitoring Budżetu

Skonfiguruj zaawansowane alerty budżetowe:

1. **Alert przy 25% budżetu** - informacyjny
2. **Alert przy 50% budżetu** - ostrzeżenie
3. **Alert przy 75% budżetu** - pilne
4. **Alert przy 90% budżetu** - krytyczne + automatyczne działania

#### Automatyczne Działania przy Przekroczeniu Budżetu

```bash
# Utwórz Cloud Function do automatycznego wyłączania aplikacji
gcloud functions deploy budget-enforcer \
  --runtime python39 \
  --trigger-topic budget-alerts \
  --entry-point enforce_budget
```

---

## Rozwiązywanie Problemów

### Najczęstsze Problemy i Rozwiązania

#### Problem 1: Błąd 502 Bad Gateway

**Przyczyny:**
- Aplikacja nie uruchamia się poprawnie
- Błąd w kodzie aplikacji
- Przekroczenie limitu czasu uruchomienia

**Rozwiązanie:**
```bash
# Sprawdź logi aplikacji
gcloud app logs tail -s default

# Sprawdź szczegóły wersji
gcloud app versions describe VERSION_ID --service=default

# Przetestuj aplikację lokalnie
python main.py
```

#### Problem 2: Wysokie Wykorzystanie Pamięci

**Przyczyny:**
- Wycieki pamięci w aplikacji
- Zbyt mała alokacja pamięci
- Nieoptymalne zapytania do bazy danych

**Rozwiązanie:**
```yaml
# Zwiększ alokację pamięci w app.yaml
resources:
  memory_gb: 1.0  # Zwiększ z 0.5 do 1.0 GB
```

```python
# Optymalizacja kodu - zamykanie połączeń DB
@app.teardown_appcontext
def close_db(error):
    db.session.close()
```

#### Problem 3: Długi Czas Odpowiedzi

**Przyczyny:**
- Nieoptymalne zapytania do bazy danych
- Brak indeksów w bazie danych
- Cold start instancji

**Rozwiązanie:**
```yaml
# Utrzymuj minimum 1 instancję aktywną
automatic_scaling:
  min_instances: 1
```

```python
# Dodaj indeksy do bazy danych
class Conversation(db.Model):
    session_id = db.Column(db.String(100), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
```

#### Problem 4: Błędy CORS

**Przyczyny:**
- Niepoprawna konfiguracja CORS
- Brak nagłówków CORS w odpowiedziach

**Rozwiązanie:**
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://yourdomain.com', 'https://novahouse.pl'])
```

### Debugowanie w Środowisku Produkcyjnym

#### Włączenie Szczegółowych Logów

```python
import logging
import os

if os.environ.get('FLASK_ENV') == 'production':
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.DEBUG)
```

#### Monitoring Błędów

```python
import traceback
from google.cloud import error_reporting

error_client = error_reporting.Client()

@app.errorhandler(500)
def handle_500(e):
    error_client.report_exception()
    return jsonify({'error': 'Internal server error'}), 500
```

### Procedury Awaryjne

#### Rollback do Poprzedniej Wersji

```bash
# Lista wersji
gcloud app versions list

# Przełącz ruch na poprzednią wersję
gcloud app services set-traffic default --splits=PREVIOUS_VERSION=100

# Zatrzymaj problematyczną wersję
gcloud app versions stop CURRENT_VERSION
```

#### Tryb Maintenance

```python
# Dodaj endpoint maintenance w aplikacji
@app.route('/maintenance')
def maintenance_mode():
    return jsonify({
        'status': 'maintenance',
        'message': 'Aplikacja jest tymczasowo niedostępna z powodu konserwacji'
    }), 503
```

---

## Bezpieczeństwo

### Konfiguracja Bezpieczeństwa App Engine

#### Ograniczenie Dostępu

```yaml
# W app.yaml - ograniczenie dostępu do endpointów administracyjnych
handlers:
- url: /admin/.*
  script: auto
  login: admin

- url: /api/admin/.*
  script: auto
  login: required
```

#### Konfiguracja Firewall

```bash
# Utwórz reguły firewall
gcloud app firewall-rules create 1000 \
  --source-range="0.0.0.0/0" \
  --action=allow \
  --description="Allow all traffic"

# Zablokuj określone IP (przykład)
gcloud app firewall-rules create 2000 \
  --source-range="192.168.1.0/24" \
  --action=deny \
  --description="Block internal network"
```

### Zabezpieczenie API

#### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/chatbot/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # Kod endpointu
    pass
```

#### Walidacja Danych Wejściowych

```python
from marshmallow import Schema, fields, validate

class ChatMessageSchema(Schema):
    message = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    session_id = fields.Str(validate=validate.Length(max=100))

@app.route('/api/chatbot/chat', methods=['POST'])
def chat():
    schema = ChatMessageSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
```

#### Sanityzacja Danych

```python
import bleach

def sanitize_user_input(text):
    # Usuń potencjalnie niebezpieczne znaki
    return bleach.clean(text, tags=[], attributes={}, strip=True)

@app.route('/api/chatbot/chat', methods=['POST'])
def chat():
    message = sanitize_user_input(request.json.get('message', ''))
    # Dalsze przetwarzanie...
```

### Zarządzanie Sekretami

#### Google Secret Manager

```bash
# Utwórz sekret
gcloud secrets create chatbot-secret-key --data-file=secret.txt

# Nadaj uprawnienia App Engine
gcloud secrets add-iam-policy-binding chatbot-secret-key \
  --member="serviceAccount:novahouse-chatbot-prod@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

```python
from google.cloud import secretmanager

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Użycie w aplikacji
app.config['SECRET_KEY'] = get_secret('chatbot-secret-key')
```

### Audyt Bezpieczeństwa

#### Regularne Przeglądy

1. **Miesięczny przegląd logów dostępu**
2. **Kwartalny audyt uprawnień**
3. **Półroczna aktualizacja zależności**
4. **Roczny penetration testing**

#### Monitoring Bezpieczeństwa

```bash
# Włącz Cloud Security Command Center
gcloud services enable securitycenter.googleapis.com

# Skonfiguruj alerty bezpieczeństwa
gcloud alpha security-center notifications create chatbot-security-alerts \
  --organization=ORGANIZATION_ID \
  --pubsub-topic=projects/PROJECT_ID/topics/security-alerts
```

---

## Backup i Odzyskiwanie

### Strategia Backup

#### Backup Bazy Danych

```python
import sqlite3
import os
from google.cloud import storage
from datetime import datetime

def backup_database():
    # Utwórz kopię bazy danych
    backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

    # Skopiuj bazę danych
    source_db = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
    backup_path = f"/tmp/{backup_filename}"

    # Wykonaj backup
    with sqlite3.connect(source_db) as source:
        with sqlite3.connect(backup_path) as backup:
            source.backup(backup)

    # Prześlij do Cloud Storage
    client = storage.Client()
    bucket = client.bucket('novahouse-chatbot-backups')
    blob = bucket.blob(f"database/{backup_filename}")
    blob.upload_from_filename(backup_path)

    # Usuń lokalny plik tymczasowy
    os.remove(backup_path)

    return backup_filename

# Automatyczny backup (uruchamiany przez Cloud Scheduler)
@app.route('/admin/backup', methods=['POST'])
def create_backup():
    try:
        filename = backup_database()
        return jsonify({'status': 'success', 'backup_file': filename})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
```

#### Konfiguracja Cloud Scheduler

```bash
# Utwórz zadanie automatycznego backup
gcloud scheduler jobs create http chatbot-daily-backup \
  --schedule="0 2 * * *" \
  --uri="https://novahouse-chatbot-prod.appspot.com/admin/backup" \
  --http-method=POST \
  --headers="Content-Type=application/json" \
  --time-zone="Europe/Warsaw"
```

### Procedura Odzyskiwania

#### Odzyskiwanie z Backup

```python
def restore_database(backup_filename):
    # Pobierz backup z Cloud Storage
    client = storage.Client()
    bucket = client.bucket('novahouse-chatbot-backups')
    blob = bucket.blob(f"database/{backup_filename}")

    # Pobierz do pliku tymczasowego
    backup_path = f"/tmp/{backup_filename}"
    blob.download_to_filename(backup_path)

    # Zastąp aktualną bazę danych
    current_db = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
    os.replace(backup_path, current_db)

    return True

@app.route('/admin/restore', methods=['POST'])
def restore_backup():
    backup_filename = request.json.get('backup_filename')
    try:
        restore_database(backup_filename)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
```

### Plan Ciągłości Działania

#### RTO i RPO

- **Recovery Time Objective (RTO):** 30 minut
- **Recovery Point Objective (RPO):** 24 godziny

#### Procedura Awaryjnego Przywracania

1. **Identyfikacja problemu** (5 minut)
2. **Rollback do poprzedniej wersji** (5 minut)
3. **Przywrócenie z backup** (15 minut)
4. **Weryfikacja funkcjonalności** (5 minut)

#### Kontakty Awaryjne

```yaml
# contacts.yaml
emergency_contacts:
  - name: "Administrator Systemu"
    phone: "+48 123 456 789"
    email: "admin@novahouse.pl"
  - name: "Zespół Deweloperski"
    phone: "+48 987 654 321"
    email: "dev@novahouse.pl"
  - name: "Google Cloud Support"
    phone: "+1 855 836 3987"
    url: "https://cloud.google.com/support"
```

---

## Podsumowanie

Niniejsza instrukcja zawiera kompletny przewodnik wdrożenia chatbota NovaHouse na platformie Google Cloud Platform. Kluczowe punkty do zapamiętania:

### Checklist Wdrożenia

- [ ] Utworzenie i konfiguracja projektu GCP
- [ ] Włączenie wymaganych API
- [ ] Inicjalizacja App Engine
- [ ] Konfiguracja budżetu i alertów
- [ ] Przygotowanie plików konfiguracyjnych
- [ ] Testowanie lokalne aplikacji
- [ ] Wdrożenie na App Engine
- [ ] Weryfikacja funkcjonalności
- [ ] Konfiguracja monitoringu
- [ ] Ustawienie domeny niestandardowej (opcjonalne)
- [ ] Konfiguracja backup i procedur awaryjnych

### Najważniejsze Zalecenia

1. **Zawsze testuj lokalnie** przed wdrożeniem na produkcję
2. **Monitoruj koszty** regularnie i ustaw odpowiednie alerty
3. **Wykonuj regularne backup** bazy danych
4. **Aktualizuj zależności** zgodnie z harmonogramem bezpieczeństwa
5. **Dokumentuj wszystkie zmiany** w systemie

### Wsparcie Techniczne

W przypadku problemów z wdrożeniem lub działaniem aplikacji:

1. **Sprawdź logi** w Cloud Logging
2. **Skonsultuj się z dokumentacją** Google Cloud Platform
3. **Skontaktuj się z zespołem deweloperskim** NovaHouse
4. **Rozważ wsparcie Google Cloud** dla krytycznych problemów

Chatbot NovaHouse jest teraz gotowy do pracy w środowisku produkcyjnym na Google Cloud Platform, zapewniając wysoką dostępność, skalowalność i bezpieczeństwo dla Twoich klientów.

---

**Koniec instrukcji wdrożenia**

*Dokument został wygenerowany przez Manus AI w dniu 11 sierpnia 2025 roku.*
