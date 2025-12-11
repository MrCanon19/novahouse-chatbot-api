# 🧪 Manual Conversation Tests - 20 Scenarios

**Data:** 11 grudnia 2025  
**Cel:** Testowanie chatbota w różnych scenariuszach jako różni klienci

---

## Test 1: Klient z literówkami
**Scenariusz:** Klient pisze z literówkami  
**Wiadomości:**
1. "Cześć, jestem Jan Kowalski"
2. "Mam 200m2 w Warszawie"
3. "Ile kosztuje wykończenie?"
4. "Jakie macie pakiety?"
5. "Dziękuję za informacje"

**Oczekiwane:** Chatbot powinien rozumieć mimo literówek, poprawić metraż (200m²), podać ceny

---

## Test 2: Klient z emotikonami
**Scenariusz:** Klient używa emotikonów  
**Wiadomości:**
1. "Cześć! 😊 Jestem Maria Nowak"
2. "Mam mieszkanie 70m² 🏠"
3. "Ile to będzie kosztować? 💰"
4. "Super! 🎉 Dziękuję"

**Oczekiwane:** Chatbot powinien odpowiedzieć naturalnie, używać emotikonów z umiarem (max 1-2)

---

## Test 3: Klient mieszający języki
**Scenariusz:** Klient miesza polski z angielskim  
**Wiadomości:**
1. "Hi, jestem Piotr"
2. "Mam apartment 100m²"
3. "What packages do you have?"
4. "OK, thanks!"

**Oczekiwane:** Chatbot powinien odpowiadać po polsku, rozumieć mieszane języki

---

## Test 4: Klient zmienia decyzję
**Scenariusz:** Klient zmienia metraż/budżet  
**Wiadomości:**
1. "Mam 200m² i budżet 500k"
2. "A właściwie mam 150m²"
3. "I budżet 300k"
4. "Przelicz proszę"

**Oczekiwane:** Chatbot powinien zaktualizować kontekst, przeliczyć ceny dla nowych danych

---

## Test 5: Klient z konfliktowymi danymi
**Scenariusz:** Klient podaje sprzeczne informacje  
**Wiadomości:**
1. "Mam 200m² w Warszawie"
2. "A właściwie 100m²"
3. "Nie, jednak 200m²"
4. "Które jest poprawne?"

**Oczekiwane:** Chatbot powinien zapytać o potwierdzenie, użyć najnowszych danych

---

## Test 6: Klient bez niektórych danych
**Scenariusz:** Klient nie podaje wszystkich danych  
**Wiadomości:**
1. "Cześć, jestem Anna"
2. "Ile kosztuje wykończenie?"
3. "Nie wiem jaki mam metraż"
4. "Możesz podać orientacyjne ceny?"

**Oczekiwane:** Chatbot powinien podać orientacyjne ceny, zapytać o metraż

---

## Test 7: Klient z bardzo długą wiadomością
**Scenariusz:** Klient pisze bardzo długą wiadomość  
**Wiadomości:**
1. "Cześć, jestem Tomasz i mam mieszkanie w Warszawie o powierzchni 120m² i chciałbym wykończyć je pod klucz. Mam budżet około 200 tysięcy złotych i zastanawiam się nad pakietem Comfort. Czy możecie mi powiedzieć więcej o tym pakiecie? Jakie materiały są wliczone? Jak długo trwa realizacja? Czy macie jakieś realizacje w Warszawie które mogę zobaczyć?"

**Oczekiwane:** Chatbot powinien odpowiedzieć na wszystkie pytania, nie przeciąć wiadomości

---

## Test 8: Klient z bardzo krótkimi odpowiedziami
**Scenariusz:** Klient odpowiada bardzo krótko  
**Wiadomości:**
1. "Cześć"
2. "200m²"
3. "Warszawa"
4. "500k"
5. "OK"

**Oczekiwane:** Chatbot powinien zrozumieć kontekst, zebrać wszystkie dane, podać wycenę

---

## Test 9: Klient z obcojęzycznym imieniem
**Scenariusz:** Klient ma obcojęzyczne imię  
**Wiadomości:**
1. "Cześć, jestem Alex Smith"
2. "Mam 150m² w Gdańsku"
3. "Ile kosztuje Premium?"

**Oczekiwane:** Chatbot powinien NIE odmieniać obcojęzycznego imienia (Alex → Alex, nie Alexie)

---

## Test 10: Klient z polskim imieniem
**Scenariusz:** Klient ma polskie imię  
**Wiadomości:**
1. "Cześć, jestem Marcin Kowalski"
2. "Mam 80m²"
3. "Jakie pakiety macie?"

**Oczekiwane:** Chatbot powinien użyć wołacza w pierwszym powitaniu ("Cześć Marcinie!"), potem naturalnie

---

## Test 11: Klient pyta o szczegóły pakietu
**Scenariusz:** Klient pyta o szczegóły konkretnego pakietu  
**Wiadomości:**
1. "Cześć, jestem Katarzyna"
2. "Mam 90m²"
3. "Czym różni się Premium od Comfort?"
4. "Co zawiera Premium?"
5. "Jak długo trwa Premium?"

**Oczekiwane:** Chatbot powinien podać konkretne różnice, zawartość, czas realizacji

---

## Test 12: Klient pyta o materiały
**Scenariusz:** Klient pyta czy materiały są wliczone  
**Wiadomości:**
1. "Cześć, jestem Paweł"
2. "Mam 110m²"
3. "Czy materiały są w cenie?"
4. "Jakie materiały są wliczone?"
5. "Czy jest rabat na materiały?"

**Oczekiwane:** Chatbot powinien potwierdzić że materiały są wliczone, wymienić przykłady, wspomnieć o rabacie 15%

---

## Test 13: Klient pyta o gwarancję
**Scenariusz:** Klient pyta o gwarancję  
**Wiadomości:**
1. "Cześć, jestem Joanna"
2. "Mam 130m²"
3. "Jaką macie gwarancję?"
4. "Na co dokładnie?"

**Oczekiwane:** Chatbot powinien podać 36 miesięcy (3 lata) gwarancji, wyjaśnić na co

---

## Test 14: Klient pyta o wizualizację
**Scenariusz:** Klient pyta o projekt 3D  
**Wiadomości:**
1. "Cześć, jestem Michał"
2. "Mam 160m²"
3. "Czy macie projekt 3D?"
4. "Czy jest wliczony w pakiet?"

**Oczekiwane:** Chatbot powinien potwierdzić że każdy pakiet zawiera projekt 3D + moodboard

---

## Test 15: Klient pyta o czas realizacji
**Scenariusz:** Klient pyta o czas realizacji  
**Wiadomości:**
1. "Cześć, jestem Agnieszka"
2. "Mam 180m²"
3. "Jak długo trwa wykończenie?"
4. "Dla jakiego pakietu?"

**Oczekiwane:** Chatbot powinien podać czasy dla wszystkich pakietów, w tygodniach i miesiącach

---

## Test 16: Klient chce umówić spotkanie
**Scenariusz:** Klient chce umówić konsultację  
**Wiadomości:**
1. "Cześć, jestem Robert"
2. "Mam 200m² w Warszawie"
3. "Chciałbym umówić spotkanie"
4. "Podaję email: robert@example.com"

**Oczekiwane:** Chatbot powinien zebrać dane, utworzyć lead, podać link do kalendarza

---

## Test 17: Klient z małym budżetem
**Scenariusz:** Klient ma mały budżet  
**Wiadomości:**
1. "Cześć, jestem Ewa"
2. "Mam 60m²"
3. "Mam budżet tylko 50k"
4. "Co mogę za to dostać?"

**Oczekiwane:** Chatbot powinien zarekomendować Express (60m² × 999 zł = ~60k), być empatyczny

---

## Test 18: Klient z dużym budżetem
**Scenariusz:** Klient ma duży budżet  
**Wiadomości:**
1. "Cześć, jestem Wojciech"
2. "Mam 250m²"
3. "Mam budżet 800k"
4. "Co polecacie?"

**Oczekiwane:** Chatbot powinien zarekomendować Premium lub Indywidualny, pokazać że zostaje budżet na dodatki

---

## Test 19: Klient pyta o miasto spoza zasięgu
**Scenariusz:** Klient jest z miasta spoza zasięgu  
**Wiadomości:**
1. "Cześć, jestem Łukasz"
2. "Mam 100m² w Krakowie"
3. "Działacie w Krakowie?"

**Oczekiwane:** Chatbot powinien poinformować że działają w Trójmieście, Warszawie, Wrocławiu, ale być pomocny

---

## Test 20: Klient z kompletnymi danymi od razu
**Scenariusz:** Klient podaje wszystkie dane od razu  
**Wiadomości:**
1. "Cześć, jestem Magdalena Kowalska. Mam mieszkanie 140m² w Gdańsku i budżet 250 tysięcy złotych. Chciałabym wykończyć je pakietem Comfort. Jak długo to trwa i co dokładnie zawiera?"

**Oczekiwane:** Chatbot powinien potwierdzić wszystkie dane, przeliczyć cenę (140m² × 1499 zł = ~210k), podać czas i zawartość

---

## ✅ Checklist wykonania

- [ ] Test 1: Literówki
- [ ] Test 2: Emotikony
- [ ] Test 3: Mieszane języki
- [ ] Test 4: Zmiana decyzji
- [ ] Test 5: Konfliktowe dane
- [ ] Test 6: Brakujące dane
- [ ] Test 7: Długa wiadomość
- [ ] Test 8: Krótkie odpowiedzi
- [ ] Test 9: Obcojęzyczne imię
- [ ] Test 10: Polskie imię
- [ ] Test 11: Szczegóły pakietu
- [ ] Test 12: Materiały
- [ ] Test 13: Gwarancja
- [ ] Test 14: Wizualizacja
- [ ] Test 15: Czas realizacji
- [ ] Test 16: Umówienie spotkania
- [ ] Test 17: Mały budżet
- [ ] Test 18: Duży budżet
- [ ] Test 19: Miasto spoza zasięgu
- [ ] Test 20: Kompletne dane

---

**Status:** ⏳ Do wykonania manualnie przed produkcją

