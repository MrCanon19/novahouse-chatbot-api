# A/B Testing i Competitive Intelligence - Dokumentacja

## Data: 19.12.2024

## Nowe Funkcje - Expert Features (C i E)

### 1. A/B Testing Follow-up Questions (C)

#### Cel
Automatyczne testowanie różnych wariantów pytań follow-up w celu optymalizacji konwersji leadów.

#### Jak działa?
- System losowo wybiera wariant A lub B pytania follow-up (50/50)
- Śledzi ile razy każdy wariant został pokazany (impressions)
- Śledzi ile razy użytkownicy odpowiedzieli na pytanie (responses)
- Oblicza conversion rate dla każdego wariantu
- Po 100+ pokazaniach automatycznie określa zwycięzcę (>10% różnica)

#### Modele Bazy Danych

**FollowUpTest**
- `question_type` - typ pytania (np. "package_to_sqm")
- `variant_a` - treść pytania wariant A
- `variant_b` - treść pytania wariant B
- `variant_a_shown` - ile razy pokazano A
- `variant_b_shown` - ile razy pokazano B
- `variant_a_responses` - ile odpowiedzi na A
- `variant_b_responses` - ile odpowiedzi na B
- `is_active` - czy test jest aktywny

**ChatConversation** (nowa kolumna)
- `followup_variant` - który wariant został pokazany ("A" lub "B")

#### Domyślne Testy A/B

1. **package_to_sqm** - Po zainteresowaniu pakietem → pytanie o metraż
   - A: "💡 A jaki jest mniej więcej metraż Twojego mieszkania? To pomoże mi lepiej dopasować ofertę."
   - B: "📐 Ile metrów kwadratowych ma Twoje mieszkanie? Na tej podstawie przygotuję dokładną wycenę."

2. **sqm_to_location** - Po podaniu metrażu → pytanie o lokalizację
   - A: "📍 W jakim mieście szukasz wykonawcy? Mamy zespoły w całej Polsce."
   - B: "🗺️ Gdzie znajduje się Twoje mieszkanie? Sprawdzę dostępność naszych ekip w Twojej okolicy."

3. **price_to_budget** - Po pytaniu o cenę → pytanie o budżet
   - A: "💰 Masz już określony budżet? Mogę pokazać opcje finansowania i rozłożenia płatności."
   - B: "💵 Jaki budżet planujesz przeznaczyć na wykończenie? Dopasuję najlepszą opcję dla Ciebie."

#### API Endpointy

**GET /api/chatbot/ab-tests/results**
- Wymagane: `X-ADMIN-API-KEY` header
- Zwraca: wszystkie testy A/B z statystykami
- Response:
```json
{
  "tests": [
    {
      "id": 1,
      "question_type": "package_to_sqm",
      "variant_a": "...",
      "variant_b": "...",
      "stats": {
        "variant_a": {
          "shown": 150,
          "responses": 89,
          "conversion_rate": 59.33
        },
        "variant_b": {
          "shown": 145,
          "responses": 102,
          "conversion_rate": 70.34
        }
      },
      "winner": "B",
      "significance": "statistically significant"
    }
  ]
}
```

**POST /api/chatbot/ab-tests/create**
- Wymagane: `X-ADMIN-API-KEY` header
- Body:
```json
{
  "question_type": "custom_test",
  "variant_a": "Pytanie wariant A",
  "variant_b": "Pytanie wariant B",
  "is_active": true
}
```

#### Funkcje

**get_ab_test_variant(conversation, question_type)**
- Wybiera losowo wariant A lub B
- Zwiększa licznik impressions
- Zapisuje wariant w conversation.followup_variant
- Zwraca: (variant, question_text)

**track_ab_test_response(conversation)**
- Śledzi że użytkownik odpowiedział
- Zwiększa licznik responses dla danego wariantu
- Czyści conversation.followup_variant

**generate_follow_up_question()** - zmodyfikowana
- Przed zwróceniem domyślnego pytania sprawdza czy jest aktywny test A/B
- Jeśli tak, używa `get_ab_test_variant()`

---

### 2. Competitive Intelligence (E)

#### Cel
Automatyczne wykrywanie i śledzenie sygnałów konkurencyjnych w rozmowach z użytkownikami.

#### Co wykrywa?

**Typy Sygnałów:**
- `competitor_mention` - wymienienie konkurenta z nazwy
- `price_comparison` - porównanie cen
- `feature_comparison` - porównanie funkcji/jakości
- `loss_to_competitor` - użytkownik wybrał konkurencję

**Wykrywane Konkurenty:**
- remonteo
- remonty
- fixly
- renovate
- home staging
- "konkurencja"
- "inna firma"
- "inne firmy"

**Słowa Kluczowe:**

*Porównanie cen:*
- tańsze, droższe, taniej, droższ
- porówna, comparison

*Porównanie jakości:*
- lepsz, gorsz, jakość, quality
- różnica, difference
- dlaczego wy

*Przegrany lead:*
- wybrałem, wybraliśmy
- zdecydował, zamówił
- umówiłem się z

#### Modele Bazy Danych

**CompetitiveIntel**
- `session_id` - ID sesji użytkownika
- `intel_type` - typ sygnału (competitor_mention, price_comparison, etc.)
- `competitor_name` - nazwa konkurenta (jeśli wykryta)
- `user_message` - oryginalna wiadomość użytkownika
- `context` - JSON z kontekstem rozmowy
- `sentiment` - sentyment (positive, negative, neutral)
- `priority` - priorytet (high, medium, low)
- `created_at` - data/czas wykrycia

#### Analiza Sentymentu

**Positive:**
- lepsze, lepiej, bardziej, ciekaw, interested

**Negative:**
- gorsze, gorzej, droż, wolniej, dłuż

**Neutral:**
- wszystko inne

#### Priorytety

**High:**
- Przegrany lead (loss_to_competitor)
- Wymienienie konkurenta + porównanie cen

**Medium:**
- Wymienienie konkurenta (bez ceny)
- Porównanie cen (bez nazwy)
- Porównanie funkcji

#### API Endpointy

**GET /api/chatbot/competitive-intelligence?days=30**
- Wymagane: `X-ADMIN-API-KEY` header
- Query params: `days` (domyślnie 30)
- Response:
```json
{
  "summary": {
    "total_mentions": 15,
    "date_range_days": 30,
    "competitor_mentions": {
      "remonteo": 5,
      "fixly": 3,
      "konkurencja": 7
    },
    "intel_types": {
      "competitor_mention": 8,
      "price_comparison": 5,
      "loss_to_competitor": 2
    },
    "sentiment_distribution": {
      "positive": 3,
      "negative": 8,
      "neutral": 4
    },
    "priority_distribution": {
      "high": 7,
      "medium": 6,
      "low": 2
    }
  },
  "recent_high_priority": [...]
}
```

#### Funkcje

**detect_competitive_intelligence(user_message, session_id, context_memory)**
- Wykrywa sygnały konkurencyjne w wiadomości użytkownika
- Określa typ, konkurenta, sentyment, priorytet
- Zapisuje do bazy CompetitiveIntel
- Wywoływana automatycznie w każdej wiadomości

#### Integracja z Monday.com

Leady w Monday.com mają teraz nowe kolumny:
- `lead_score` (Number) - wynik 0-100
- `competitor_mentioned` (Text) - nazwa konkurenta jeśli wykryto
- `next_action` (Text) - rekomendowana akcja

Przy tworzeniu leada system automatycznie:
1. Sprawdza czy były sygnały konkurencyjne w tej sesji
2. Jeśli tak, dodaje nazwę konkurenta do Monday
3. Pozwala zespołowi sprzedaży priorytetyzować leady gdzie jest konkurencja

---

## Migracja Bazy Danych

### Uruchomienie

```bash
cd /Users/michalmarini/Projects/manus/novahouse-chatbot-api
python migrations/add_ab_testing_and_competitive_intel.py
```

### Co robi?

1. Tworzy tabelę `followup_tests`
2. Tworzy tabelę `competitive_intel`
3. Dodaje kolumnę `followup_variant` do `chat_conversations`
4. Dodaje 3 domyślne testy A/B

---

## Weryfikacja Monday.com Board

### Wymagane Kolumny

Board `2145240699` powinien mieć:

**Istniejące:**
- `email` (Email type)
- `phone` (Phone type)
- `text` (Text type) - wiadomość
- `package` (Dropdown) - pakiet
- `confidence` (Number) - zaufanie
- `property_type` (Dropdown) - typ nieruchomości
- `budget` (Text/Currency)
- `interior_style` (Dropdown) - styl
- `status` (Status: New Lead, Contacted, Qualified, Done, Stuck)

**Nowe (do dodania w Monday.com):**
- `lead_score` (Number) - wynik 0-100
- `competitor_mentioned` (Text) - nazwa konkurenta
- `next_action` (Text) - rekomendowana akcja

### Test Połączenia

```bash
curl -X POST https://YOUR-APP.appspot.com/api/chatbot/test-monday \
  -H "X-ADMIN-API-KEY: your-admin-key"
```

---

## Użycie

### 1. Włączanie/Wyłączanie Testów A/B

Testy można aktywować/deaktywować bezpośrednio w bazie:
```sql
UPDATE followup_tests SET is_active = false WHERE question_type = 'package_to_sqm';
```

### 2. Monitorowanie Wyników

Dashboard w przeglądarce lub API:
```bash
curl https://YOUR-APP.appspot.com/api/chatbot/ab-tests/results \
  -H "X-ADMIN-API-KEY: your-key"
```

### 3. Przeglądanie Competitive Intel

```bash
curl "https://YOUR-APP.appspot.com/api/chatbot/competitive-intelligence?days=7" \
  -H "X-ADMIN-API-KEY: your-key"
```

---

## Wdrożenie na Produkcję

### 1. Uruchom migrację
```bash
gcloud app deploy --stop-previous-version
```

### 2. Po wdrożeniu, SSH do GAE i uruchom migrację
```bash
gcloud app ssh
cd /app
python migrations/add_ab_testing_and_competitive_intel.py
```

### 3. Dodaj kolumny w Monday.com
- Otwórz board 2145240699
- Dodaj kolumnę "Lead Score" (Number)
- Dodaj kolumnę "Competitor Mentioned" (Text)
- Dodaj kolumnę "Next Action" (Text lub Long Text)

### 4. Testuj
- Rozpocznij rozmowę z chatem
- Wymień konkurencję: "Remonteo mi powiedział że jest taniej"
- Sprawdź czy zapisało się w `/competitive-intelligence`
- Sprawdź czy lead w Monday ma wypełnione pole `competitor_mentioned`

---

## Metryki Sukcesu

### A/B Testing
- **Cel:** Zwiększyć conversion rate follow-up questions o 15%+
- **Monitoruj:** Które warianty mają wyższy response rate
- **Optymalizuj:** Wyłącz gorsze warianty, testuj nowe

### Competitive Intelligence
- **Cel:** Zidentyfikować 100% przypadków gdzie użytkownik wspomina konkurencję
- **Monitoruj:** Priority "high" intel - natychmiast reaguj
- **Akcja:** Zespół sprzedaży dzwoni w ciągu 1h do leadów z competitor mention

---

## Następne Kroki (Future)

1. **Auto-optimization:** System automatycznie wyłącza gorsze warianty
2. **Multi-variate testing:** Testowanie 3+ wariantów jednocześnie
3. **Competitive response templates:** Automatyczne sugerowanie odpowiedzi na sygnały konkurencyjne
4. **Win/Loss analysis:** Tracking dlaczego wygraliśmy/przegraliśmy lead
5. **Price intelligence:** Agregacja informacji o cenach konkurencji
