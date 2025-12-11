# 🤖 Porównanie Modeli LLM - Nova House Chatbot

**Data:** 11 grudnia 2025  
**Cel:** Wybór najlepszego modelu dla chatbota Nova House

---

## 📊 Dostępne Modele

### 1. gpt-4o-mini (Obecny)
- **Jakość:** ⭐⭐⭐ (Dobra)
- **Szybkość:** ⭐⭐⭐⭐⭐ (Bardzo szybka)
- **Koszt:** ⭐⭐⭐⭐⭐ (Najtańszy)
- **Polski język:** ⭐⭐⭐ (Dobry)
- **Cena:** ~$0.15 / 1M input tokens, ~$0.60 / 1M output tokens

**Zalety:**
- Najtańszy model GPT-4
- Szybki czas odpowiedzi
- Wystarczający dla większości rozmów

**Wady:**
- Może mieć gorszą jakość dla złożonych pytań
- Ograniczona kreatywność

---

### 2. gpt-4o (Rekomendowany dla lepszej jakości)
- **Jakość:** ⭐⭐⭐⭐⭐ (Najlepsza)
- **Szybkość:** ⭐⭐⭐⭐ (Szybka)
- **Koszt:** ⭐⭐⭐ (Średni)
- **Polski język:** ⭐⭐⭐⭐⭐ (Doskonały)
- **Cena:** ~$2.50 / 1M input tokens, ~$10.00 / 1M output tokens

**Zalety:**
- Najlepsza jakość odpowiedzi
- Doskonałe zrozumienie polskiego
- Lepsza kreatywność i kontekst

**Wady:**
- Droższy (~16x droższy niż gpt-4o-mini)
- Wolniejszy niż mini

---

### 3. gpt-3.5-turbo (Nie rekomendowany)
- **Jakość:** ⭐⭐ (Słaba dla polskiego)
- **Szybkość:** ⭐⭐⭐⭐⭐ (Bardzo szybka)
- **Koszt:** ⭐⭐⭐⭐⭐ (Najtańszy)
- **Polski język:** ⭐⭐ (Słaby)
- **Cena:** ~$0.50 / 1M input tokens, ~$1.50 / 1M output tokens

**Zalety:**
- Najtańszy
- Bardzo szybki

**Wady:**
- Słaba jakość dla polskiego języka
- Ograniczone zrozumienie kontekstu
- Nie rekomendowany dla produkcji

---

## 💰 Analiza Kosztów

### Szacunkowe użycie (miesięcznie):
- **Liczba rozmów:** 1000
- **Średnia długość rozmowy:** 10 wiadomości
- **Średnia długość wiadomości:** 50 tokenów (input), 100 tokenów (output)
- **Total tokens:** ~500k input, ~1M output

### Koszty miesięczne:

| Model | Input | Output | RAZEM |
|-------|-------|--------|-------|
| **gpt-4o-mini** | $0.075 | $0.60 | **~$0.68** |
| **gpt-4o** | $1.25 | $10.00 | **~$11.25** |
| **gpt-3.5-turbo** | $0.25 | $1.50 | **~$1.75** |

---

## 🎯 Rekomendacja

### Obecny wybór: **gpt-4o-mini** ✅

**Uzasadnienie:**
1. Dobry balans jakości/kosztu
2. Wystarczający dla większości rozmów
3. Szybki czas odpowiedzi
4. Niski koszt operacyjny

### Rozważ upgrade do **gpt-4o** jeśli:
1. Jakość odpowiedzi jest niewystarczająca
2. Klienci skarżą się na odpowiedzi
3. Budżet pozwala na wyższe koszty
4. Potrzebna lepsza kreatywność

### Strategia hybrydowa (opcjonalnie):
- **gpt-4o-mini** dla standardowych rozmów (90%)
- **gpt-4o** dla kluczowych rozmów (10%) - wysokie lead score, duży budżet

---

## 📈 Metryki do Monitorowania

1. **Jakość odpowiedzi:**
   - User satisfaction rating
   - Conversion rate (rozmowa → lead)
   - Czas do konwersji

2. **Koszty:**
   - Tokens użyte (input/output)
   - Koszt na rozmowę
   - Koszt miesięczny

3. **Wydajność:**
   - Czas odpowiedzi (latency)
   - Error rate
   - Timeout rate

---

## ✅ Aktualizacja Konfiguracji

### Obecna konfiguracja:
```bash
GPT_MODEL=gpt-4o-mini
```

### Aby zmienić na gpt-4o:
```bash
GPT_MODEL=gpt-4o
```

### Aby użyć strategii hybrydowej:
- Dodać logikę wyboru modelu w `GptStrategy` na podstawie lead score lub kontekstu

---

## 📝 Podsumowanie

| Kryterium | gpt-4o-mini | gpt-4o | gpt-3.5-turbo |
|-----------|-------------|--------|---------------|
| **Jakość** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Koszt** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Szybkość** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Polski** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Rekomendacja** | ✅ **OBECNY** | ⭐ Rozważyć | ❌ Nie |

**Finalna rekomendacja:** Pozostać przy **gpt-4o-mini**, monitorować jakość, rozważyć upgrade jeśli potrzeba.

---

**Ostatnia aktualizacja:** 11 grudnia 2025

