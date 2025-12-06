# Plan Implementacji - 3 Rundy

## 🏁 RUNDA 1: PODSTAWY ✅ (GOTOWA)

### Co zrobiono:
- ✅ Zaktualizowana baza wiedzy - godziny pracy, kontakt
- ✅ Rozszerzone FAQ z 5 do 10 pytań
- ✅ Ulepszony system promptów chatbota (bardziej friendly, precyzyjny)
- ✅ Lepsze rozpoznawanie pytań klientów
- ✅ Ulepszone domyślne odpowiedzi
- ✅ Testy przechodzą

### Commit: `536dc27`

---

## 🔌 RUNDA 2: INTEGRACJE (Monday.com + Kwalifikacja)

### Co trzeba zrobić:

#### 1. **Konfiguracja Monday.com**
- [ ] Sprawdzić czy `MONDAY_API_KEY` i `MONDAY_BOARD_ID` są ustawione w zmiennych środowiskowych
- [ ] Potwierdzić że leady z formularza kwalifikacji trafiają do Monday
- [ ] Dodać mapowanie pól: metraż, budżet, priorytet → kolumny w Monday
- [ ] Dodać możliwość ustawienia statusu lead-a na podstawie pakietu (Standard/Premium/Luxury)

#### 2. **Ulepszone dane kwalifikacji**
- [ ] Przechwycić odpowiedzi z formularza kwalifikacji
- [ ] Dodać pytanie o lokalizację (warszawa/inne?)
- [ ] Dodać pytanie o styl wnętrz (minimalistyczny, nowoczesny, klasyczny, Industrial)
- [ ] Zapisywać preferencje stylowe razem z lead-em

#### 3. **Integracja Booksy (rezerwacje)**
- [ ] Sprawdzić czy API Booksy jest dostępne
- [ ] Dodać endpointy do rezerwacji konsultacji
- [ ] Dodać możliwość zarezerwowania spotkania z ekspertem

#### 4. **Ulepszone prompty - bot zachęca do dalszych akcji**
- [ ] Po udzieleniu odpowiedzi - zaproponować rezerwację
- [ ] Po udzieleniu odpowiedzi - zaproponować otrzymanie wyceny
- [ ] Po udzieleniu odpowiedzi - zaproponować rozmowę z ekspertem

---

## 📊 RUNDA 3: ADVANCED (Dashboards + Analytics + Fine-tuning)

### Co trzeba zrobić:

#### 1. **Analytics Dashboard**
- [ ] Sprawdzić działające endpointy: `/api/analytics/overview`, `/api/analytics/conversations`, `/api/analytics/leads`
- [ ] Poprawić linki które nie działają
- [ ] Dodać sekcję dla konwersji: ile osób → ile leadów → ile sfinalizowanych
- [ ] Dodać metryki dotyczące pakietów (ile osób wybrało Standard/Premium/Luxury)

#### 2. **Admin Dashboard**
- [ ] Przejrzeć `admin-dashboard.html`
- [ ] Dodać sekcję do zarządzania rezerwacjami
- [ ] Dodać sekcję do przeglądania wszystkich leadów
- [ ] Dodać możliwość masowych operacji (zmiana statusu, export)

#### 3. **Fine-tuning chatbota**
- [ ] Dodać możliwość zapisania prefernecji użytkownika w sesji
- [ ] Zapamiętywanie poprzednich rozmów w tej samej sesji
- [ ] Lepsze dopasowanie rekomendacji na podstawie historii
- [ ] A/B testing różnych promptów (metric: conversion rate)

#### 4. **Integracja z Booksy rezerwacje**
- [ ] Endpoint do dostępnych terminów
- [ ] Endpoint do rezerwacji terminu
- [ ] Potwierdzenie rezerwacji na email

---

## 📋 Zmienne Środowiskowe (do skonfigurowania)

```bash
# Monday.com
MONDAY_API_KEY=<your_api_key>
MONDAY_BOARD_ID=<your_board_id>

# Booksy (jeśli dostępne)
BOOKSY_API_KEY=<your_api_key>
BOOKSY_BUSINESS_ID=<your_business_id>

# Analytics
ANALYTICS_ENABLED=true

# Gemini
GEMINI_API_KEY=<your_api_key>
```

---

## 🎯 Priorytety

### MUSI (High Priority):
1. Pewna konfiguracja Monday.com z leadami i danymi kwalifikacji
2. Integracja z Booksy - rezerwacje konsultacji
3. Analytics dashboard - metryki konwersji

### POWINNA (Medium Priority):
1. Admin dashboard - pełna zarządzanie leadami
2. Fine-tuning chatbota - lepsze prompty
3. Zapamiętywanie preferencji użytkownika

### MOGŁA BY (Low Priority):
1. A/B testing promptów
2. Zaawansowana analityka
3. Integracja z innymi narzędziami (Slack, email itd.)

---

## ✅ Checklist przed uruchomieniem produkcji

- [ ] Wszystkie zmienne środowiskowe skonfigurowane
- [ ] Monday.com testował i działał
- [ ] Booksy testuje i działał
- [ ] Dashboard pokazuje prawidłowe dane
- [ ] Chatbot udzielał rozsądnych odpowiedzi
- [ ] Leady poprawnie zapisują się do systemu
- [ ] RODO endpoints działają poprawnie
- [ ] Testy przechodzą
- [ ] Baza danych backupowana
- [ ] Logi zapisywane i monitorowane

---

## 📞 Kontakt / FAQ

**Q: Gdzie dodać zmienne środowiskowe?**
A: W pliku `.env` w katalogu głównym projektu. Przykład w `README.md`.

**Q: Jak przetestować integrację z Monday?**
A: Sprawdź `src/integrations/monday_client.py` - jest tam metoda `test_connection()`.

**Q: Gdzie są endpointy analityki?**
A: W `src/routes/analytics.py` - dostępne pod `/api/analytics/*`.
