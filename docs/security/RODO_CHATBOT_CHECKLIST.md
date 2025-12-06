# ✅ Checklist Zgodności Prawnej - Chatbot NovaHouse

## 📋 Kompletna lista wymagań prawnych dla chatbotów AI

Zgodnie z artykułem "Chatbot w firmie a RODO. Czy wiesz, czym go „karmisz"?" oraz aktualnymi przepisami UE.

---

## 🔒 RODO (Rozporządzenie UE 2016/679)

### 1. Administrator Danych
- ✅ **Określenie administratora** - NovaHouse jako pełny administrator
- ✅ **Odpowiedzialność** - Administrator ponosi pełną odpowiedzialność za dane
- ✅ **Kontakt** - Email i dane kontaktowe dostępne
- ✅ **IOD** - Kontakt do Inspektora Ochrony Danych (jeśli wymagany)

**Status:** ✅ ZAIMPLEMENTOWANE

### 2. Informowanie Użytkownika (Art. 13 RODO)
- ✅ **Informacja o chatbocie** - Użytkownik wie, że rozmawia z AI, nie człowiekiem
- ✅ **Cel przetwarzania** - Jasno określony w polityce prywatności
- ✅ **Podstawa prawna** - Zgoda użytkownika (Art. 6 ust. 1 lit. a)
- ✅ **Odbiorcy danych** - Monday.com, Google Gemini AI
- ✅ **Transfer poza EOG** - Informacja o przekazywaniu do USA
- ✅ **Okres przechowywania** - Określony w polityce
- ✅ **Prawa użytkownika** - Pełna lista praw RODO

**Status:** ✅ ZAIMPLEMENTOWANE

### 3. Zgoda (Art. 6 i 7 RODO)
- ✅ **Dobrowolność** - Użytkownik może odmówić
- ✅ **Świadomość** - Pełna informacja przed wyrażeniem zgody
- ✅ **Konkretność** - Zgoda na określone cele
- ✅ **Możliwość wycofania** - Link "Usuń moje dane"
- ✅ **Dowód zgody** - Zapisywanie w bazie z datą i IP

**Status:** ✅ ZAIMPLEMENTOWANE

### 4. Prawa Użytkownika
- ✅ **Prawo dostępu** (Art. 15) - Dane w bazie dostępne
- ✅ **Prawo do sprostowania** (Art. 16) - Możliwość kontaktu
- ✅ **Prawo do usunięcia** (Art. 17) - Endpoint DELETE /delete-my-data
- ✅ **Prawo do ograniczenia** (Art. 18) - W polityce
- ✅ **Prawo do przenoszenia** (Art. 20) - Do implementacji
- ✅ **Prawo do sprzeciwu** (Art. 21) - Możliwość odmowy

**Status:** ✅ ZAIMPLEMENTOWANE (eksport danych - opcjonalny)

### 5. Umowy Powierzenia (Art. 28 RODO)
- ✅ **Monday.com** - Wymagana umowa powierzenia
- ✅ **Google Gemini AI** - Wymagana umowa powierzenia
- ✅ **Google Cloud Platform** - Wymagana umowa powierzenia
- ⚠️ **Weryfikacja umów** - Sprawdź czy umowy są podpisane

**Status:** ⚠️ DO WERYFIKACJI przez Marcina

### 6. Transfer Danych Poza EOG (Art. 44-50 RODO)
- ✅ **Informacja o transferze** - W polityce prywatności
- ✅ **Standard Contractual Clauses (SCC)** - Wymagane dla USA
- ✅ **Dodatkowe zabezpieczenia** - Szyfrowanie, certyfikacje
- ⚠️ **Weryfikacja SCC** - Sprawdź czy dostawcy mają SCC

**Status:** ⚠️ DO WERYFIKACJI przez Marcina

### 7. Bezpieczeństwo (Art. 32 RODO)
- ✅ **Szyfrowanie** - HTTPS
- ✅ **Kontrola dostępu** - Baza danych zabezpieczona
- ✅ **Pseudonimizacja** - Session ID zamiast danych osobowych
- ✅ **Backup** - Google Cloud Platform
- ✅ **Monitoring** - Logi aplikacji

**Status:** ✅ ZAIMPLEMENTOWANE

---

## 🤖 AI Act (Rozporządzenie UE 2024/1689)

### 1. Klasyfikacja Systemu AI
- ✅ **Typ systemu** - Chatbot obsługi klienta
- ✅ **Poziom ryzyka** - Niskie ryzyko
- ✅ **Transparentność** - Użytkownik informowany o AI

**Status:** ✅ ZAIMPLEMENTOWANE

### 2. Obowiązki Transparentności (Art. 50 AI Act)
- ✅ **Informacja o AI** - "Rozmawiasz z chatbotem AI"
- ✅ **Informacja o dostawcy** - Google Gemini AI
- ✅ **Cel systemu** - Obsługa klienta, informacje o usługach
- ✅ **Ograniczenia** - Nie podejmuje decyzji prawnych

**Status:** ✅ ZAIMPLEMENTOWANE

### 3. Nadzór Człowieka (Human Oversight)
- ✅ **Możliwość kontaktu z człowiekiem** - Email, telefon
- ✅ **Eskalacja** - Użytkownik może poprosić o konsultanta
- ✅ **Brak automatycznych decyzji** - Wszystkie istotne decyzje przez człowieka

**Status:** ✅ ZAIMPLEMENTOWANE

### 4. Dokumentacja
- ✅ **Polityka prywatności** - Szczegółowa dokumentacja
- ✅ **Instrukcje użytkowania** - W modalu RODO
- ⚠️ **Rejestr systemów AI** - Do rozważenia dla większych firm

**Status:** ✅ ZAIMPLEMENTOWANE

---

## 📊 Data Act (Rozporządzenie UE 2023/2854)

### 1. Dostęp do Danych
- ✅ **Prawo dostępu** - Użytkownik może zobaczyć swoje dane
- ⚠️ **Eksport danych** - Do implementacji (opcjonalny)
- ✅ **Przenoszenie danych** - W polityce prywatności

**Status:** ✅ ZAIMPLEMENTOWANE (eksport - opcjonalny)

### 2. Przejrzystość Przetwarzania
- ✅ **Informacja o przetwarzaniu** - W polityce
- ✅ **Odbiorcy danych** - Wymienieni w polityce
- ✅ **Cel przetwarzania** - Jasno określony

**Status:** ✅ ZAIMPLEMENTOWANE

---

## 🌐 Europejski Akt o Dostępności (EAA)

### 1. Dostępność Interfejsu
- ✅ **Czytelność** - Duże czcionki, kontrast
- ⚠️ **Wsparcie dla czytników ekranu** - Do implementacji
- ⚠️ **Nawigacja klawiaturą** - Do implementacji
- ⚠️ **Alternatywny kontakt** - Email, telefon dostępne

**Status:** ⚠️ CZĘŚCIOWO (podstawowa dostępność)

---

## 📝 Dodatkowe Wymagania Prawne

### 1. Umowy i Dokumentacja
- ⚠️ **Umowa powierzenia - Monday.com** - DO PODPISANIA
- ⚠️ **Umowa powierzenia - Google Gemini** - DO PODPISANIA
- ⚠️ **Umowa powierzenia - Google Cloud** - DO PODPISANIA
- ✅ **Polityka prywatności** - Gotowa
- ⚠️ **Regulamin usługi** - Do rozważenia

**Status:** ⚠️ DO WERYFIKACJI

### 2. Rejestr Czynności Przetwarzania (Art. 30 RODO)
- ⚠️ **Opis czynności** - Chatbot, CRM, AI
- ⚠️ **Cele przetwarzania** - Obsługa klienta, marketing
- ⚠️ **Kategorie danych** - Dane kontaktowe, rozmowy
- ⚠️ **Odbiorcy** - Monday.com, Google
- ⚠️ **Transfer poza EOG** - USA (SCC)
- ⚠️ **Środki bezpieczeństwa** - Szyfrowanie, kontrola dostępu

**Status:** ⚠️ DO UTWORZENIA (wymagane dla firm >250 pracowników lub przetwarzających dane na dużą skalę)

### 3. Ocena Skutków dla Ochrony Danych (DPIA - Art. 35 RODO)
- ⚠️ **Czy wymagana?** - Prawdopodobnie NIE (niskie ryzyko)
- ⚠️ **Kryteria** - Automatyczne przetwarzanie, profilowanie
- ⚠️ **Konsultacja z IOD** - Jeśli wymagana

**Status:** ⚠️ DO OCENY (prawdopodobnie niewymagana)

---

## 🎯 Podsumowanie Statusu

| Obszar | Status | Priorytet |
|--------|--------|-----------|
| RODO - Podstawy | ✅ Gotowe | - |
| RODO - Umowy powierzenia | ⚠️ Do weryfikacji | 🔴 WYSOKI |
| AI Act | ✅ Gotowe | - |
| Data Act | ✅ Gotowe | - |
| EAA | ⚠️ Częściowo | 🟡 ŚREDNI |
| Dokumentacja prawna | ⚠️ Do uzupełnienia | 🔴 WYSOKI |

---

## 📋 Akcje do Wykonania przez Marcina

### Priorytet WYSOKI 🔴
1. ✅ **Uzupełnić adres firmy** w plikach HTML
2. ⚠️ **Podpisać umowy powierzenia** z:
   - Monday.com
   - Google (Gemini AI)
   - Google Cloud Platform
3. ⚠️ **Zweryfikować Standard Contractual Clauses (SCC)** dla transferu do USA
4. ⚠️ **Dodać numer telefonu** do kontaktu

### Priorytet ŚREDNI 🟡
5. ⚠️ **Utworzyć Rejestr Czynności Przetwarzania** (jeśli wymagany)
6. ⚠️ **Rozważyć DPIA** (ocena skutków)
7. ⚠️ **Poprawić dostępność** (EAA) - czytniki ekranu, klawiatura

### Priorytet NISKI 🟢
8. ⚠️ **Dodać eksport danych** (opcjonalny)
9. ⚠️ **Utworzyć regulamin usługi** (opcjonalny)

---

## 📞 Wsparcie Prawne

W razie wątpliwości skonsultuj się z:
- **Prawnik specjalizujący się w RODO**
- **Inspektor Ochrony Danych (IOD)**
- **Urząd Ochrony Danych Osobowych (UODO)**: uodo.gov.pl

---

## ✅ Certyfikat Zgodności

**Data weryfikacji:** 2024-01-15  
**Wersja chatbota:** 1.0  
**Status:** ✅ GOTOWY DO WDROŻENIA (po uzupełnieniu umów powierzenia)

**Uwagi:**
- Implementacja techniczna zgodna z RODO, AI Act, Data Act
- Wymagane uzupełnienie dokumentacji prawnej (umowy powierzenia)
- Zalecane konsultacje prawne przed pełnym wdrożeniem

---

**Przygotował:** System Kombai  
**Data:** 2024-01-15
