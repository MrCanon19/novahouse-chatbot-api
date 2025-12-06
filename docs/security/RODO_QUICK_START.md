# 🚀 RODO - Szybki Start

## ✅ Wszystko gotowe!

Implementacja RODO została zakończona. Oto co zostało dodane:

### 📁 Nowe pliki:
1. ✅ `src/static/polityka-prywatnosci.html` - Polityka prywatności
2. ✅ `src/migrations/add_rodo_consent_table.py` - Migracja bazy danych
3. ✅ `RODO_IMPLEMENTATION.md` - Pełna dokumentacja
4. ✅ `RODO_QUICK_START.md` - Ten plik

### 🔧 Zmodyfikowane pliki:
1. ✅ `src/static/chatbot.html` - Dodano modal RODO i funkcje
2. ✅ `src/routes/chatbot.py` - Dodano endpointy RODO
3. ✅ `src/models/chatbot.py` - Dodano model RodoConsent

### 🎯 Co działa:
- ✅ Modal zgody RODO przy pierwszym wejściu
- ✅ Zapisywanie zgód w bazie danych
- ✅ Funkcja "Usuń moje dane"
- ✅ Polityka prywatności
- ✅ Baner informacyjny w chacie

## 🧪 Testowanie lokalne

```bash
# 1. Uruchom aplikację
cd ~/novahouse-chatbot-api
python src/main.py

# 2. Otwórz w przeglądarce
http://localhost:8080/chatbot.html
```

**Sprawdź:**
1. Modal RODO pojawia się przy pierwszym wejściu ✅
2. Checkbox musi być zaznaczony, żeby aktywować przycisk ✅
3. Po akceptacji pojawia się baner w chacie ✅
4. Link "Usuń moje dane" działa ✅
5. Polityka prywatności otwiera się: http://localhost:8080/polityka-prywatnosci.html ✅

## 🚀 Deploy na produkcję

```bash
# Deploy
gcloud app deploy

# Sprawdź logi
gcloud app logs tail -s default
```

## ⚠️ WAŻNE - Do uzupełnienia przez Marcina:

### 1. Adres firmy w plikach:

**Plik: `src/static/chatbot.html` (linia ~390)**
```html
<strong>Administrator danych:</strong> NovaHouse, [DODAJ ADRES], email: m.kubiak@novahouse.pl
```

**Plik: `src/static/polityka-prywatnosci.html` (linia ~50)**
```html
<strong>NovaHouse</strong><br>
[DODAJ PEŁNY ADRES FIRMY]<br>
Email: m.kubiak@novahouse.pl
```

### 2. URL strony głównej:

**Plik: `src/static/chatbot.html` (linia ~450)**
```javascript
window.location.href = 'https://novahouse.pl'; // Sprawdź czy to właściwy URL
```

## 📊 Sprawdzenie zgód w bazie

```python
from src.models.chatbot import RodoConsent
from src.main import app

with app.app_context():
    consents = RodoConsent.query.all()
    print(f"Liczba zgód: {len(consents)}")
    for consent in consents:
        print(f"Session: {consent.session_id}, Data: {consent.consent_date}")
```

## 🎉 Gotowe!

Wszystkie wymagania RODO zostały zaimplementowane:
- ✅ Informacja o bocie AI
- ✅ Zgoda użytkownika
- ✅ Polityka prywatności
- ✅ Prawo do usunięcia danych
- ✅ Zapisywanie zgód

**Pytania?** Kontakt: m.kubiak@novahouse.pl
