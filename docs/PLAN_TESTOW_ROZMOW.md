# 📋 PLAN TESTÓW ROZMÓW - 20 SCENARIUSZY

**Status:** ✅ **GOTOWY DO WYKONANIA**  
**Data:** 12 grudnia 2025

---

## 🎯 CEL TESTÓW

Przeprowadzenie 20 testowych rozmów jako różni potencjalni klienci, aby:
- Sprawdzić reakcje chatbota na różne style pisania
- Zweryfikować poprawność ekstrakcji danych
- Przetestować sytuacje nietypowe
- Zidentyfikować potencjalne problemy

---

## 📝 SCENARIUSZE TESTOWE

### Test 1: Klient zainteresowany pakietem Express
**Wiadomości:**
1. "Dzień dobry"
2. "Chcę wycenę na mieszkanie 50m²"
3. "Jaki jest najtańszy pakiet?"
4. "Ile to będzie kosztować?"
5. "Kiedy można zacząć?"

**Oczekiwane:**
- Rozpoznanie metrażu: 50m²
- Rekomendacja pakietu Express
- Podanie ceny (~50k zł)
- Informacja o czasie realizacji (6-8 tyg)

---

### Test 2: Klient z budżetem 200k
**Wiadomości:**
1. "Mam budżet 200 tysięcy złotych"
2. "Co mogę za to dostać?"
3. "Mieszkanie ma 65m²"
4. "Jaki pakiet polecacie?"

**Oczekiwane:**
- Rozpoznanie budżetu: 200000 zł
- Rozpoznanie metrażu: 65m²
- Rekomendacja pakietu Comfort lub Premium

---

### Test 3: Klient z mieszkaniem 50m²
**Wiadomości:**
1. "Mam mieszkanie 50m²"
2. "Chcę wycenę"
3. "Jaki pakiet będzie najlepszy?"
4. "Jestem z Warszawy"

**Oczekiwane:**
- Rozpoznanie metrażu: 50m²
- Rozpoznanie miasta: Warszawa
- Rekomendacja pakietu

---

### Test 4: Klient z Warszawy
**Wiadomości:**
1. "Jestem z Warszawy"
2. "Chcę wykończyć mieszkanie"
3. "Mam 70m²"
4. "Budżet około 150 tysięcy"

**Oczekiwane:**
- Rozpoznanie miasta: Warszawa
- Rozpoznanie metrażu: 70m²
- Rozpoznanie budżetu: 150000 zł

---

### Test 5: Klient z Wrocławia
**Wiadomości:**
1. "Dzień dobry, jestem z Wrocławia"
2. "Mam mieszkanie 60m²"
3. "Chcę pakiet Comfort"
4. "Ile to będzie kosztować?"

**Oczekiwane:**
- Rozpoznanie miasta: Wrocław
- Rozpoznanie metrażu: 60m²
- Rozpoznanie pakietu: Comfort
- Podanie ceny (~90k zł)

---

### Test 6: Klient z Trójmiasta
**Wiadomości:**
1. "Jestem z Gdańska"
2. "Mam mieszkanie 80m²"
3. "Chcę pakiet Premium"
4. "Kiedy można zacząć?"

**Oczekiwane:**
- Rozpoznanie miasta: Gdańsk
- Rozpoznanie metrażu: 80m²
- Rozpoznanie pakietu: Premium
- Informacja o czasie realizacji (10-16 tyg)

---

### Test 7: Klient z małego miasta
**Wiadomości:**
1. "Jestem z Radomska"
2. "Mam mieszkanie 45m²"
3. "Czy działacie w moim mieście?"
4. "Chcę wycenę"

**Oczekiwane:**
- Rozpoznanie miasta: Radomsko
- Rozpoznanie metrażu: 45m²
- Informacja o zasięgu działalności (Trójmiasto, Warszawa, Wrocław)

---

### Test 8: Klient z literówkami
**Wiadomości:**
1. "Dzien dobry"
2. "Mam mieszkanie 55m2"
3. "Jestem z warszawy"
4. "Chce pakiet komfort"

**Oczekiwane:**
- Rozpoznanie mimo literówek
- Rozpoznanie metrażu: 55m²
- Rozpoznanie miasta: Warszawa
- Rozpoznanie pakietu: Comfort

---

### Test 9: Klient używający emotikon
**Wiadomości:**
1. "Dzień dobry! 😊"
2. "Mam mieszkanie 50m²"
3. "Chcę wycenę 😃"
4. "Jestem z Wrocławia 🏠"

**Oczekiwane:**
- Ignorowanie emotikon
- Rozpoznanie metrażu: 50m²
- Rozpoznanie miasta: Wrocław

---

### Test 10: Klient mieszający języki
**Wiadomości:**
1. "Hello, chcę wycenę"
2. "Mam apartment 60m²"
3. "Jestem z Warsaw"
4. "Ile to będzie cost?"

**Oczekiwane:**
- Rozpoznanie mimo mieszania języków
- Rozpoznanie metrażu: 60m²
- Rozpoznanie miasta: Warszawa (z "Warsaw")

---

### Test 11: Klient zmieniający decyzję
**Wiadomości:**
1. "Chcę pakiet Express"
2. "A może jednak Comfort?"
3. "Albo Premium?"
4. "Który będzie najlepszy dla 70m²?"

**Oczekiwane:**
- Rozpoznanie zmiany decyzji
- Rozpoznanie metrażu: 70m²
- Rekomendacja pakietu

---

### Test 12: Klient podający sprzeczne dane
**Wiadomości:**
1. "Mam mieszkanie 50m²"
2. "A właściwie 60m²"
3. "Albo 55m²"
4. "Nie jestem pewien"

**Oczekiwane:**
- Przyjęcie ostatniej podanej wartości: 55m²
- Uspokojenie klienta

---

### Test 13: Klient bez podawania danych
**Wiadomości:**
1. "Dzień dobry"
2. "Chcę wycenę"
3. "Ile to kosztuje?"
4. "Kiedy można zacząć?"

**Oczekiwane:**
- Pytania o brakujące dane (metraż, miasto)
- Nie zakładanie danych których klient nie podał

---

### Test 14: Klient pytający o gwarancję
**Wiadomości:**
1. "Jaka jest gwarancja?"
2. "Na ile lat?"
3. "Co obejmuje?"
4. "Mam mieszkanie 65m²"

**Oczekiwane:**
- Informacja o gwarancji: 36 miesięcy (3 lata)
- Rozpoznanie metrażu: 65m²

---

### Test 15: Klient pytający o czas realizacji
**Wiadomości:**
1. "Ile trwa wykończenie?"
2. "Dla pakietu Comfort"
3. "Mieszkanie 55m²"
4. "Kiedy można zacząć?"

**Oczekiwane:**
- Informacja o czasie: 8-12 tygodni (Comfort)
- Rozpoznanie metrażu: 55m²
- Rozpoznanie pakietu: Comfort

---

### Test 16: Klient pytający o materiały
**Wiadomości:**
1. "Jakie materiały są w pakiecie?"
2. "Czy są wliczone w cenę?"
3. "Mam mieszkanie 60m²"
4. "Pakiet Premium"

**Oczekiwane:**
- Informacja o materiałach wliczonych w cenę
- Rozpoznanie metrażu: 60m²
- Rozpoznanie pakietu: Premium

---

### Test 17: Klient chcący umówić spotkanie
**Wiadomości:**
1. "Chcę umówić spotkanie"
2. "Mam mieszkanie 70m²"
3. "Jestem z Warszawy"
4. "Kiedy możemy się spotkać?"

**Oczekiwane:**
- Rozpoznanie intencji umówienia spotkania
- Rozpoznanie metrażu: 70m²
- Rozpoznanie miasta: Warszawa
- Sugestia Zencal lub kontakt

---

### Test 18: Klient pytający o konkurencję
**Wiadomości:**
1. "Czym różnicie się od konkurencji?"
2. "Dlaczego wybrać was?"
3. "Mam mieszkanie 50m²"

**Oczekiwane:**
- Informacja o przewagach (96% zadowolonych, 94% przed terminem, 36 miesięcy gwarancji)
- Rozpoznanie metrażu: 50m²

---

### Test 19: Klient z negatywnym feedbackiem
**Wiadomości:**
1. "Słyszałem złe opinie"
2. "Czy to prawda?"
3. "Chcę wycenę na 60m²"

**Oczekiwane:**
- Uspokojenie klienta
- Informacja o pozytywnych statystykach
- Rozpoznanie metrażu: 60m²

---

### Test 20: Klient z bardzo długą rozmową
**Wiadomości:** (15 wiadomości)
1. "Dzień dobry"
2. "Mam mieszkanie 55m²"
3. "Jestem z Wrocławia"
4. "Budżet 200 tysięcy"
5. "Chcę pakiet Comfort"
6. "Ile to będzie kosztować?"
7. "Kiedy można zacząć?"
8. "Jaka jest gwarancja?"
9. "Co obejmuje pakiet?"
10. "Czy materiały są wliczone?"
11. "Ile trwa realizacja?"
12. "Czy można zmienić coś w trakcie?"
13. "Jak wygląda proces?"
14. "Czy jest projekt?"
15. "Chcę umówić spotkanie"

**Oczekiwane:**
- Utrzymanie kontekstu przez całą rozmowę
- Rozpoznanie wszystkich danych
- Spójne odpowiedzi
- Sugestia umówienia spotkania na końcu

---

## 📊 WERYFIKACJA

Dla każdego testu sprawdź:
- ✅ Czy chatbot rozpoznał wszystkie dane?
- ✅ Czy odpowiedzi są spójne i profesjonalne?
- ✅ Czy używa poprawnej odmiany imion/miast?
- ✅ Czy nie zakłada danych których klient nie podał?
- ✅ Czy proponuje następne kroki?

---

## 📝 WYNIKI TESTÓW

[Do wypełnienia po przeprowadzeniu testów]

---

**Plik testowy:** `tests/test_conversations.py`  
**Status:** ✅ Gotowy do wykonania

