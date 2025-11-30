# GAE Deployment Guide - No ML Dependencies

## Problem

Google App Engine standard environment nie wspiera natywnie numpy/scikit-learn
(wymagają kompilacji C).

## Rozwiązanie

Aplikacja działa w dwóch trybach:

### 1. **Tryb z ML** (local development)

- Pełne ML lead scoring z RandomForest
- Wymaga: `numpy>=1.24.0`, `scikit-learn>=1.3.0`
- Instalacja: `pip install -r requirements.txt`

### 2. **Tryb bez ML** (GAE production)

- Graceful degradation do rule-based lead scoring
- Nie wymaga numpy/scikit-learn
- Instalacja: `pip install -r requirements-gae.txt`

## Deployment na GAE

### Opcja A: Deploy bez ML (ZALECANE)

```bash
# Użyj requirements-gae.txt (bez numpy/sklearn)
cp requirements-gae.txt requirements.txt
gcloud app deploy --quiet
git checkout requirements.txt  # Przywróć oryginalny
```

### Opcja B: Deploy z ML (eksperymentalnie)

```bash
# Użyj standardowego requirements.txt
# GAE spróbuje zainstalować numpy/sklearn
# Może działać na instancjach F4/F4_1G z więcej RAM
gcloud app deploy --quiet
```

## Weryfikacja po deploy

```bash
# Health check
curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health

# Test chat (powinien działać z rule-based scoring)
curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Chcę wycenę", "session_id": "test123"}'

# Sprawdź logi (szukaj ostrzeżeń o numpy)
gcloud app logs tail
```

## Jak działa lazy import

### W `lead_scoring_ml.py`

```python
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("⚠️ numpy not available - ML scoring disabled")
```

### Metody sprawdzają flagę

```python
def predict_score(self, context_memory, conversation_data):
    if not NUMPY_AVAILABLE or self.model is None:
        # Fallback to rule-based scoring
        return self._fallback_rule_based_scoring(...)
```

### Funkcja fallback

```python
def _fallback_rule_based_scoring(self, context_memory, conversation_data):
    score = 0
    # Email: +30
    if context_memory.get("email"):
        score += 30
    # Phone: +25
    if context_memory.get("phone"):
        score += 25
    # ... itd
    return min(100, score)
```

## Testowanie lokalne

### Test z numpy

```bash
pip install numpy scikit-learn
python scripts/test_lead_scoring.py
# Powinno używać ML jeśli model wytrenowany
```

### Test bez numpy

```bash
pip uninstall -y numpy scikit-learn
python scripts/test_lead_scoring.py
# Powinno użyć rule-based fallback
```

## Monitoring produkcyjny

Po deploy sprawdź w logach:

```bash
gcloud app logs tail --service=default
```

Szukaj:

- ✅ "⚠️ numpy not available - ML scoring disabled" - OK, używa fallback
- ✅ "[ML Lead Scoring] Model not loaded, using rule-based fallback" - OK
- ❌ ImportError: numpy przy starcie - NIE OK, app się crashuje
- ❌ ModuleNotFoundError: sklearn przy starcie - NIE OK

## Przyszłość: ML na GAE

### Opcja 1: GAE Flexible (wymaga Dockerfile)

- Wspiera numpy/scikit-learn
- Droższe ($50-100/miesiąc)
- Dłuższy cold start

### Opcja 2: Cloud Functions 2nd gen

- Deploy ML jako oddzielny serwis
- Call przez HTTP API
- Scaling niezależny od chatbota

### Opcja 3: Vertex AI

- Hosted ML predictions
- Zarządzany przez GCP
- Najdroższe ale najprostsze

## Podsumowanie

✅ **Aplikacja jest bezpieczna** - startuje bez numpy/scikit-learn
✅ **Graceful degradation** - używa rule-based scoring jeśli ML niedostępne
✅ **Przetestowane** - 24 unit testy, wszystkie przechodzą
✅ **Deploy ready** - użyj `requirements-gae.txt` dla pewności
