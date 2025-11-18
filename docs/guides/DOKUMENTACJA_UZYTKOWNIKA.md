# 📖 NovaHouse Chatbot - Dokumentacja Użytkownika

## 🌐 Linki Produkcyjne

- **Strona główna:** https://glass-core-467907-e9.ey.r.appspot.com
- **Panel Admina:** https://glass-core-467907-e9.ey.r.appspot.com/admin
- **System Kwalifikacji:** https://glass-core-467907-e9.ey.r.appspot.com/qualification
- **API Chatbota:** https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/chat

---

## 👥 DLA HANDLOWCÓW

### Panel Admina
1. Otwórz: https://glass-core-467907-e9.ey.r.appspot.com/admin
2. Zobacz statystyki:
   - Ile leadów w systemie
   - Ile nowych (oczekuje na kontakt)
   - Ile zsynchronizowanych z Monday.com
3. Przeglądaj listę leadów z filtrowaniem
4. Kliknij przycisk odświeżania (prawy dolny róg) dla aktualnych danych

### Praca z Leadami
- **Nowe leady** - pojawią się automatycznie z chatbota
- **Status "Nowy"** - czeka na pierwszy kontakt
- **Monday.com sync** - leady z badge "Sync" są w Monday.com
- Wszystkie dane: imię, email, telefon, wiadomość

---

## 🎯 System Kwalifikacji Klienta

### Jak działa?
1. Klient otwiera: https://glass-core-467907-e9.ey.r.appspot.com/qualification
2. Odpowiada na 7 pytań:
   - Metraż mieszkania
   - Budżet
   - Termin realizacji
   - Rodzaj materiałów
   - Smart home
   - Indywidualny projekt
   - Priorytety
3. System oblicza rekomendację pakietu (Standard/Premium/Luxury)
4. Pokazuje pewność rekomendacji (%)

### Dla kogo który pakiet?
- **Standard:** Budżet <100k, podstawowe materiały, priorytet: cena/czas
- **Premium:** Budżet 100-200k, jakość materiałów, smart home
- **Luxury:** Budżet >200k, materiały luksusowe, indywidualny projekt

---

## 💬 Chatbot

### Podstawowe komendy
Chatbot rozumie po polsku i odpowiada na pytania o:
- Pakiety wykończeniowe
- Czas realizacji (6-12 tygodni)
- Czy cena obejmuje materiały (Tak)
- Gwarancja (2 lata)
- Płatności (etapami: 30% zaliczka)

### Przykłady pytań:
- "Jakie macie pakiety?"
- "Ile kosztuje Premium?"
- "Jak długo trwa wykończenie?"
- "Czy mogę dostosować pakiet?"

---

## 🔗 Monday.com Integracja

### Co jest synchronizowane?
- ✅ Nowe leady automatycznie trafiają do Monday.com
- ✅ Zmiany statusu w systemie → aktualizacja w Monday.com
- ✅ Wszystkie dane kontaktowe

### Tablica Monday.com:
https://novahouse-squad.monday.com/boards/2145240699

---

## 🆘 Wsparcie Techniczne

### W razie problemów:
1. Sprawdź połączenie z internetem
2. Odśwież stronę (Cmd+R / Ctrl+R)
3. Wyczyść cache przeglądarki
4. Kontakt: [email do wsparcia]

### Znane ograniczenia:
- Chatbot działa najlepiej z krótkimi, konkretnymi pytaniami
- Rekomendacje pakietów są automatyczne (mogą wymagać konsultacji)
- Dashboard odświeża się co 30 sekund

---

## 📱 Dostęp Mobilny

Wszystkie funkcje działają na urządzeniach mobilnych:
- ✅ Panel Admina - responsywny
- ✅ System Kwalifikacji - optymalizowany na telefon
- ✅ Chatbot - działa na wszystkich urządzeniach

---

**Aktualizacja:** 17 października 2025  
**Wersja:** 2.0  
**Status:** 🟢 Produkcja
