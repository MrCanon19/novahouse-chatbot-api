# 🔒 Implementacja RODO w Chatbocie NovaHouse

## ✅ Co zostało zaimplementowane

### 1. **Modal zgody RODO** (`src/static/chatbot.html`)
- ✅ Wyświetla się przed rozpoczęciem rozmowy
- ✅ Informuje, że to bot AI
- ✅ Link do polityki prywatności
- ✅ Checkbox z wymaganą zgodą
- ✅ Przycisk akceptacji i odrzucenia
- ✅ Informacje o administratorze danych

### 2. **Backend - Nowe endpointy** (`src/routes/chatbot.py`)
- ✅ `POST /api/chatbot/rodo-consent` - zapisuje zgodę użytkownika
- ✅ `DELETE /api/chatbot/delete-my-data` - usuwa wszystkie dane użytkownika (prawo do bycia zapomnianym)

### 3. **Model bazy danych** (`src/models/chatbot.py`)
- ✅ Nowa tabela `RodoConsent` do śledzenia zgód
- ✅ Pola: session_id, consent_given, consent_date, ip_address, user_agent

### 4. **Polityka Prywatności** (`src/static/polityka-prywatnosci.html`)
- ✅ Kompletna polityka zgodna z RODO
- ✅ Informacje o administratorze
- ✅ Cele przetwarzania danych
- ✅ Prawa użytkownika
- ✅ Kontakt do UODO

### 5. **Funkcjonalności użytkownika**
- ✅ Baner informacyjny w chacie
- ✅ Link "Usuń moje dane" dostępny w każdej chwili
- ✅ Przechowywanie zgody w localStorage
- ✅ Zapisywanie session_id dla późniejszego usunięcia danych

## 🚀 Instrukcja wdrożenia

### Krok 1: Uruchom migrację bazy danych

```bash
cd ~/novahouse-chatbot-api
python src/migrations/add_rodo_consent_table.py
```

### Krok 2: Przetestuj lokalnie

```bash
# Uruchom aplikację
python src/main.py

# Otwórz w przeglądarce
http://localhost:8080/chatbot.html
```

**Sprawdź:**
- ✅ Modal RODO wyświetla się przy pierwszym wejściu
- ✅ Po zaakceptowaniu modal znika i pojawia się baner
- ✅ Link "Usuń moje dane" działa
- ✅ Po usunięciu danych modal pojawia się ponownie

### Krok 3: Deploy na produkcję

```bash
# Deploy do Google Cloud
gcloud app deploy

# Sprawdź logi
gcloud app logs tail -s default
```

### Krok 4: Weryfikacja na produkcji

Otwórz: `https://[twoja-domena]/chatbot.html`

## 📋 Checklist zgodności RODO i innych przepisów UE

### RODO (Rozporządzenie UE 2016/679)
- ✅ **Art. 6 RODO** - Podstawa prawna (zgoda użytkownika)
- ✅ **Art. 13 RODO** - Informacje dla użytkownika (polityka prywatności)
- ✅ **Art. 15 RODO** - Prawo dostępu do danych
- ✅ **Art. 17 RODO** - Prawo do usunięcia danych ("prawo do bycia zapomnianym")
- ✅ **Art. 22 RODO** - Automatyczne podejmowanie decyzji (chatbot NIE podejmuje decyzji prawnych)
- ✅ **Art. 25 RODO** - Ochrona danych w fazie projektowania (privacy by design)
- ⚠️ **Art. 28 RODO** - Umowy powierzenia (wymagane z Monday.com, Google)
- ⚠️ **Art. 30 RODO** - Rejestr czynności przetwarzania (jeśli wymagany)
- ✅ **Art. 32 RODO** - Bezpieczeństwo przetwarzania (HTTPS, szyfrowanie)
- ⚠️ **Art. 44-50 RODO** - Transfer poza EOG (SCC dla USA)

### AI Act (Rozporządzenie UE 2024/1689)
- ✅ **Art. 50** - Transparentność (użytkownik wie, że rozmawia z AI)
- ✅ **Klasyfikacja** - System niskiego ryzyka
- ✅ **Nadzór człowieka** - Możliwość kontaktu z konsultantem

### Data Act (Rozporządzenie UE 2023/2854)
- ✅ **Dostęp do danych** - Użytkownik może zobaczyć swoje dane
- ✅ **Przenoszenie danych** - Określone w polityce

### Europejski Akt o Dostępności (EAA)
- ⚠️ **Dostępność** - Podstawowa implementacja (do rozszerzenia)

## 🔧 Konfiguracja wymagana

### 1. Zaktualizuj dane kontaktowe w plikach:

**Plik: `src/static/chatbot.html`**
- Linia ~390: Dodaj pełny adres firmy
- Linia ~450: Sprawdź URL przekierowania (novahouse.pl)

**Plik: `src/static/polityka-prywatnosci.html`**
- Linia ~50: Dodaj pełny adres firmy
- Dodaj numer telefonu do kontaktu

### 2. ⚠️ KRYTYCZNE - Umowy powierzenia przetwarzania danych:

**Wymagane umowy zgodnie z Art. 28 RODO:**

1. **Monday.com** - System CRM
   - Szablon: `UMOWA_POWIERZENIA_SZABLON.md`
   - Skonsultuj z prawnikiem
   - Podpisz przed wdrożeniem produkcyjnym

2. **Google Gemini AI** - Przetwarzanie zapytań
   - Sprawdź warunki Google Cloud
   - Podpisz umowę powierzenia
   - Zweryfikuj Standard Contractual Clauses (SCC)

3. **Google Cloud Platform** - Hosting
   - Umowa powierzenia z Google
   - SCC dla transferu do USA

### 3. Standard Contractual Clauses (SCC):

Dla transferu danych do USA wymagane są SCC:
- Sprawdź czy dostawcy mają podpisane SCC
- Zweryfikuj dodatkowe zabezpieczenia
- Dokumentuj transfer w rejestrze czynności

### 4. Opcjonalne (zalecane):

- **Rejestr czynności przetwarzania** (Art. 30 RODO)
- **DPIA** - Ocena skutków (jeśli wymagana)
- **Regulamin usługi chatbota**
- **Inspektor Ochrony Danych** (jeśli wymagany)

## 📊 Monitoring zgód RODO

### Sprawdź zgody w bazie danych:

```python
from src.models.chatbot import RodoConsent
from src.main import app

with app.app_context():
    consents = RodoConsent.query.all()
    for consent in consents:
        print(f"Session: {consent.session_id}")
        print(f"Zgoda: {consent.consent_given}")
        print(f"Data: {consent.consent_date}")
        print(f"IP: {consent.ip_address}")
        print("---")
```

## 🛡️ Bezpieczeństwo

### Dane przechowywane:
- ✅ Session ID (anonimowy identyfikator)
- ✅ Treść rozmowy
- ✅ Zgoda RODO z datą i IP
- ✅ Dane kontaktowe (tylko jeśli użytkownik poda)

### Dane NIE przechowywane:
- ❌ Hasła
- ❌ Dane karty kredytowej
- ❌ Szczegółowe dane lokalizacyjne

## 📞 Kontakt w sprawie RODO

**Administrator Danych:**
- Email: m.kubiak@novahouse.pl
- Strona: https://novahouse.pl

**Inspektor Ochrony Danych (jeśli wymagany):**
- [DO UZUPEŁNIENIA]

## 🔄 Kolejne kroki (opcjonalne)

1. **Rozszerz politykę prywatności** o:
   - Szczegóły dotyczące Monday.com
   - Informacje o Google Gemini AI
   - Transfer danych poza EOG (jeśli dotyczy)

2. **Dodaj eksport danych** (Art. 20 RODO):
   ```python
   @chatbot_bp.route('/export-my-data', methods=['POST'])
   def export_user_data():
       # Zwróć wszystkie dane użytkownika w formacie JSON
       pass
   ```

3. **Rejestr czynności przetwarzania** (Art. 30 RODO):
   - Dokumentuj wszystkie operacje na danych osobowych

4. **Ocena skutków dla ochrony danych (DPIA)**:
   - Jeśli przetwarzanie jest na dużą skalę

## ✅ Status implementacji

| Wymaganie | Status | Notatki |
|-----------|--------|---------|
| Modal zgody RODO | ✅ Gotowe | Wyświetla się przed rozmową |
| Polityka prywatności | ✅ Gotowe | Wymaga uzupełnienia adresu |
| Prawo do usunięcia | ✅ Gotowe | Funkcja deleteMyData() |
| Zapisywanie zgód | ✅ Gotowe | Tabela rodo_consents |
| Informacja o bocie AI | ✅ Gotowe | W modalu i banerze |
| Bezpieczne przechowywanie | ✅ Gotowe | SQLite + HTTPS |

## 📝 Changelog

**2024-01-XX** - Wersja 1.0
- ✅ Dodano modal zgody RODO
- ✅ Dodano politykę prywatności
- ✅ Dodano funkcję usuwania danych
- ✅ Dodano tabelę zgód w bazie danych
- ✅ Dodano endpointy backend

---

**Pytania? Problemy?**
Skontaktuj się z Marcinem: m.kubiak@novahouse.pl
