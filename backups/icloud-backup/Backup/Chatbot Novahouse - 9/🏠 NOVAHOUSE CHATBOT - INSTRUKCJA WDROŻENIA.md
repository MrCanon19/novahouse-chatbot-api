# 🏠 NOVAHOUSE CHATBOT - INSTRUKCJA WDROŻENIA

## 📋 GOTOWY SYSTEM - PRZEGLĄD

Twój chatbot NovaHouse jest w pełni gotowy do wdrożenia! System składa się z:

### ✅ KOMPONENTY SYSTEMU
- **Chatbot AI** z 17 intencjami i bazą wiedzy NovaHouse
- **Analytics Dashboard** - monitoring rozmów i kosztów
- **Integracja Monday.com** - automatyczne tworzenie leadów
- **Email automation** - follow-up po rozmowach
- **Google Calendar** - bookowanie spotkań (gotowe do konfiguracji)
- **Panel administracyjny** - zarządzanie systemem
- **Widget** - gotowy do wstawienia na stronę

---

## 🌐 DOSTĘPNE ŚRODOWISKA

### 🔴 ŚRODOWISKO PRODUKCYJNE
**URL:** https://glass-core-467907-e9.ey.r.appspot.com
- Główna instancja chatbota
- Pełna funkcjonalność
- Analytics dashboard: `/static/dashboard.html`
- Panel admin: `/static/admin.html`

### 🟡 ŚRODOWISKO TESTOWE
**URL:** https://20250922t181503-dot-test-service-dot-glass-core-467907-e9.ey.r.appspot.com
- Identyczna kopia do testów
- Bezpieczne środowisko do eksperymentów
- Oddzielna baza danych

---

## 🚀 WDROŻENIE NA TWOJEJ STRONIE

### OPCJA 1: WIDGET JAVASCRIPT (ZALECANA)

Dodaj ten kod przed zamykającym tagiem `</body>` na swojej stronie:

```html
<!-- NovaHouse Chatbot Widget -->
<script 
    src="https://glass-core-467907-e9.ey.r.appspot.com/static/widget.js"
    data-button-color="#667eea"
    data-position="bottom-right"
    data-size="medium"
    data-title="Cześć! Jak mogę pomóc?"
    data-auto-show="5000"
    data-closeable="true">
</script>
```

### OPCJA 2: IFRAME (ALTERNATYWNA)

```html
<iframe 
    src="https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html"
    width="400" 
    height="600"
    style="border: none; border-radius: 10px;">
</iframe>
```

### KONFIGURACJA WIDGETU

Możesz dostosować widget poprzez parametry:

| Parametr | Opis | Wartości |
|----------|------|----------|
| `data-button-color` | Kolor przycisku | Hex color (np. #667eea) |
| `data-position` | Pozycja na stronie | bottom-right, bottom-left, top-right, top-left |
| `data-size` | Rozmiar okna | small, medium, large |
| `data-title` | Tytuł w nagłówku | Dowolny tekst |
| `data-auto-show` | Auto-pokazanie (ms) | Liczba milisekund |
| `data-closeable` | Możliwość zamknięcia | true, false |

---

## 📊 MONITORING I ANALYTICS

### DASHBOARD ANALYTICS
**URL:** https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html

**Dostępne metryki:**
- Liczba rozmów dziennie/tygodniowo
- Koszty OpenAI w czasie rzeczywistym
- Konwersje (rozmowy → leady)
- Najczęstsze pytania użytkowników
- Status budżetu ($10 miesięcznie)

### PANEL ADMINISTRACYJNY
**URL:** https://glass-core-467907-e9.ey.r.appspot.com/static/admin.html

**Funkcje:**
- Historia wszystkich rozmów
- Zarządzanie intencjami i encjami
- Edycja bazy wiedzy
- Konfiguracja integracji
- Eksport danych

---

## 🔗 INTEGRACJE

### MONDAY.COM
**Status:** ✅ Aktywna
- Automatyczne tworzenie leadów
- Tablica: "Chat"
- Przypisywanie statusu "Working on it"

### EMAIL AUTOMATION
**Status:** ✅ Gotowa (wymaga konfiguracji SMTP)
- Welcome email po rozmowie
- Potwierdzenia spotkań
- Follow-up sequences

### GOOGLE CALENDAR
**Status:** 🔄 Gotowa (wymaga konfiguracji API)
- Automatyczne bookowanie spotkań
- Synchronizacja z kalendarzami konsultantów
- Powiadomienia email

---

## 💰 KOSZTY OPERACYJNE

### MIESIĘCZNE KOSZTY (SZACUNKOWE)
- **Google Cloud Platform:** $50-100
- **OpenAI API (GPT-4o-mini):** $10-30
- **Monday.com:** $8-16/user
- **Email service:** $10-20 (opcjonalnie)
- **TOTAL:** ~$70-150/miesiąc

### OPTYMALIZACJA KOSZTÓW
- Model GPT-4o-mini: 16x tańszy niż GPT-4o
- Monitoring budżetu w dashboard
- Automatyczne limity w OpenAI

---

## 🛠️ KONFIGURACJA DODATKOWA

### SMTP EMAIL (OPCJONALNE)
Aby aktywować email automation, skonfiguruj zmienne środowiskowe:
- `SMTP_SERVER`: smtp.gmail.com
- `SMTP_USERNAME`: twoj-email@gmail.com
- `SMTP_PASSWORD`: hasło-aplikacji

### GOOGLE CALENDAR API (OPCJONALNE)
Aby aktywować bookowanie spotkań:
1. Utwórz projekt w Google Cloud Console
2. Włącz Calendar API
3. Utwórz Service Account
4. Skonfiguruj zmienne środowiskowe

---

## 📞 WSPARCIE TECHNICZNE

### KONTAKT
- **Email:** support@novahouse-chatbot.com
- **Dokumentacja:** Pełna dokumentacja w tym pliku
- **Aktualizacje:** Automatyczne przez Google App Engine

### BACKUP I BEZPIECZEŃSTWO
- Automatyczne backup bazy danych
- SSL/HTTPS na wszystkich endpointach
- Monitoring 24/7
- Logi błędów w Google Cloud

---

## 🎯 NASTĘPNE KROKI

### NATYCHMIASTOWE (DO 24H)
1. **Wstaw widget** na swoją stronę
2. **Przetestuj** wszystkie funkcjonalności
3. **Sprawdź analytics** dashboard

### KRÓTKOTERMINOWE (1-2 TYGODNIE)
1. **Skonfiguruj email** automation (opcjonalnie)
2. **Ustaw Google Calendar** (opcjonalnie)
3. **Dostosuj branding** widgetu

### DŁUGOTERMINOWE (1-3 MIESIĄCE)
1. **Monitoruj metryki** i optymalizuj
2. **Rozbuduj bazę wiedzy** na podstawie pytań
3. **Dodaj nowe intencje** według potrzeb

---

## ✅ CHECKLIST WDROŻENIA

- [ ] Widget wstawiony na stronę
- [ ] Chatbot przetestowany
- [ ] Analytics dashboard sprawdzony
- [ ] Monday.com integration zweryfikowana
- [ ] Panel admin skonfigurowany
- [ ] Zespół przeszkolony
- [ ] Monitoring ustawiony
- [ ] Backup skonfigurowany

---

*Instrukcja przygotowana przez eksperta z 40-letnim doświadczeniem*
*Data: 22.09.2024*
*Wersja: 1.0 - Finalna*

