# 📊 Monitorowanie Logów Aplikacji

## 🛠️ Narzędzia

### 1. `scripts/monitor_logs.py` - Monitor logów w czasie rzeczywistym

#### Podstawowe użycie:

```bash
# Pokaż ostatnie 50 logów
python3 scripts/monitor_logs.py

# Pokaż tylko błędy
python3 scripts/monitor_logs.py --errors

# Śledź logi w czasie rzeczywistym (tail -f)
python3 scripts/monitor_logs.py --tail

# Śledź tylko błędy w czasie rzeczywistym
python3 scripts/monitor_logs.py --tail --errors

# Pokaż podsumowanie błędów
python3 scripts/monitor_logs.py --summary

# Pokaż logi z minimalną severity
python3 scripts/monitor_logs.py --severity WARNING

# Pokaż więcej logów
python3 scripts/monitor_logs.py --limit 100
```

#### Przykłady:

```bash
# Monitoruj wszystkie logi w czasie rzeczywistym
python3 scripts/monitor_logs.py --tail

# Monitoruj tylko błędy
python3 scripts/monitor_logs.py --tail --errors

# Sprawdź ostatnie błędy
python3 scripts/monitor_logs.py --errors --limit 20

# Podsumowanie błędów
python3 scripts/monitor_logs.py --summary
```

### 2. `scripts/enhanced_logger.py` - Ulepszony logger

Ulepszony logger z dodatkowymi funkcjami:
- Logowanie z kontekstem
- Timing funkcji
- Stack trace dla błędów
- Decoratory do automatycznego logowania

#### Użycie w kodzie:

```python
from scripts.enhanced_logger import get_logger, log_function_execution

logger = get_logger("my_module")

# Podstawowe logowanie z kontekstem
logger.info("User logged in", user_id=123, session_id="abc")
logger.error("API call failed", url="/api/chat", status_code=500)

# Logowanie funkcji z timingiem
@log_function_execution(logger)
def my_function(x, y):
    return x + y
```

## 🔍 Diagnostyka Błędów

### Krok 1: Sprawdź podsumowanie błędów

```bash
python3 scripts/monitor_logs.py --summary
```

To pokaże:
- Liczbę błędów
- Typy błędów
- Ostatnie wystąpienia

### Krok 2: Monitoruj logi w czasie rzeczywistym

```bash
python3 scripts/monitor_logs.py --tail --errors
```

To pozwoli zobaczyć błędy natychmiast po ich wystąpieniu.

### Krok 3: Sprawdź szczegóły konkretnego błędu

```bash
# Pokaż ostatnie 100 logów z błędami
python3 scripts/monitor_logs.py --errors --limit 100
```

## 📋 Najczęstsze Problemy i Rozwiązania

### Problem: Błąd 502 Bad Gateway

```bash
# Sprawdź błędy startowe
python3 scripts/monitor_logs.py --errors --limit 50

# Szukaj "Worker failed to boot" lub "IndentationError"
python3 scripts/monitor_logs.py --errors | grep -i "worker\|indentation\|syntax"
```

### Problem: Błąd bazy danych

```bash
# Szukaj błędów SQL
python3 scripts/monitor_logs.py --errors | grep -i "sql\|database\|connection"
```

### Problem: Błąd API

```bash
# Szukaj błędów API
python3 scripts/monitor_logs.py --errors | grep -i "api\|openai\|monday"
```

## 🎨 Kolory w Logach

- 🔴 **ERROR** - Błędy (czerwony)
- 🟡 **WARNING** - Ostrzeżenia (żółty)
- 🟢 **INFO** - Informacje (zielony)
- 🔵 **DEBUG** - Debug (niebieski)

## 📊 Integracja z GCP

Narzędzie automatycznie używa:
- Projekt: `glass-core-467907-e9`
- Serwis: `default`
- Format: JSON

Możesz zmienić projekt w skrypcie lub przez zmienną środowiskową.

## 🔧 Zaawansowane

### Filtrowanie po czasie

```bash
# Użyj gcloud bezpośrednio dla zaawansowanego filtrowania
gcloud logging read \
  "resource.type=gae_app AND severity>=ERROR AND timestamp>=\"2025-12-12T00:00:00Z\"" \
  --limit 50 \
  --format json \
  --project glass-core-467907-e9
```

### Eksport logów do pliku

```bash
python3 scripts/monitor_logs.py --errors --limit 100 > errors.log
```

### Monitorowanie w tle

```bash
# Uruchom w tle i zapisz do pliku
nohup python3 scripts/monitor_logs.py --tail --errors > monitor.log 2>&1 &
```

## 📝 Notatki

- Logi są w czasie UTC
- Format timestamp: `YYYY-MM-DD HH:MM:SS`
- Severity levels: DEBUG < INFO < WARNING < ERROR < CRITICAL

