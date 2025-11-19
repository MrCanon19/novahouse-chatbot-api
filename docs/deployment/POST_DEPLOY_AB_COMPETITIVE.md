# Post-Deployment Checklist - A/B Testing & Competitive Intelligence

## Po wdrożeniu wykonaj te kroki:

### 1. Uruchom migrację bazy danych na produkcji

```bash
# SSH do GAE instance
gcloud app ssh

# Przejdź do katalogu app
cd /app

# Uruchom migrację
python migrations/run_migration_simple.py

# Sprawdź czy tabele zostały utworzone
python -c "
from src.models.chatbot import db, FollowUpTest, CompetitiveIntel
from main import app
with app.app_context():
    print('FollowUpTest count:', FollowUpTest.query.count())
    print('CompetitiveIntel count:', CompetitiveIntel.query.count())
"
```

### 2. Dodaj kolumny w Monday.com Board

Otwórz board: https://novahouse.monday.com/boards/2145240699

Dodaj nowe kolumny:

1. **Lead Score** (Number column)
   - Name: `lead_score`
   - Type: Number
   - Range: 0-100

2. **Competitor Mentioned** (Text column)
   - Name: `competitor_mentioned`
   - Type: Text

3. **Next Action** (Long Text column)
   - Name: `next_action`
   - Type: Long Text or Text

### 3. Test A/B Testing

```bash
# Sprawdź domyślne testy A/B
curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/ab-tests/results \
  -H "X-ADMIN-API-KEY: $ADMIN_API_KEY"

# Powinieneś zobaczyć 3 testy:
# - package_to_sqm
# - sqm_to_location
# - price_to_budget
```

### 4. Test Competitive Intelligence

Rozpocznij test conversation:

1. Idź na chatbot
2. Napisz: "Remonteo mi powiedział że jest taniej"
3. Sprawdź czy zapisało się:

```bash
curl "https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/competitive-intelligence?days=1" \
  -H "X-ADMIN-API-KEY: $ADMIN_API_KEY"
```

4. Sprawdź czy lead w Monday.com ma wypełnione pole `competitor_mentioned`

### 5. Monitoruj Logi

```bash
gcloud app logs tail -s default
```

Szukaj:
- `[A/B Test]` - śledzenie testów
- `[Competitive Intel]` - wykryte sygnały konkurencyjne
- `[Monday]` - tworzenie leadów z nowymi polami

### 6. Sprawdź Endpointy

```bash
# Health check
curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health

# A/B Test Results
curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/ab-tests/results \
  -H "X-ADMIN-API-KEY: $ADMIN_API_KEY"

# Competitive Intelligence
curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/competitive-intelligence \
  -H "X-ADMIN-API-KEY: $ADMIN_API_KEY"

# Lead Stats (powinny zawierać hot leads z scoring)
curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/stats/leads \
  -H "X-ADMIN-API-KEY: $ADMIN_API_KEY"
```

### 7. Test E2E Flow

Scenariusz testowy:

1. **Rozpocznij konwersację**
   - User: "Cześć, chciałbym wykończyć mieszkanie"
   - Bot: odpowie standardowo

2. **Wymień pakiet**
   - User: "Interesuje mnie pakiet Premium"
   - Bot: zapyta o metraż (A lub B wariant!)

3. **Podaj metraż**
   - User: "70 metrów"
   - Bot: zapyta o lokalizację (A lub B wariant!)

4. **Wspomni konkurencję**
   - User: "Remonteo zaproponował mi 120k, a wy?"
   - Bot: odpowie + zapisze competitive intel

5. **Potwierdź dane**
   - Bot: zapyta "Czy wszystko się zgadza?"
   - User: "TAK"
   - Bot: utworzy lead w Monday.com

6. **Sprawdź Monday.com**
   - Lead powinien mieć:
     - `lead_score`: 50-70 (zależnie od danych)
     - `competitor_mentioned`: "remonteo"
     - `next_action`: "Call within 24h" lub podobne

7. **Sprawdź A/B Test**
   ```bash
   curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/ab-tests/results \
     -H "X-ADMIN-API-KEY: $ADMIN_API_KEY"
   ```
   - `variant_a_shown` lub `variant_b_shown` powinno wzrosnąć o 1
   - Jeśli user odpowiedział, `responses` też wzrośnie

### 8. Weryfikacja Monday.com Columns

Jeśli kolumny nie działają w Monday.com, sprawdź:

```bash
# Test Monday connection
curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/test-monday \
  -H "X-ADMIN-API-KEY: $ADMIN_API_KEY"
```

Jeśli błąd, upewnij się że:
- `MONDAY_API_KEY` jest poprawny
- `MONDAY_BOARD_ID` = 2145240699
- Kolumny w Monday mają DOKŁADNIE nazwy: `lead_score`, `competitor_mentioned`, `next_action`

### 9. Ustaw Alerty (Opcjonalnie)

Skonfiguruj alerty dla high-priority competitive intel:

1. Stwórz skrypt który sprawdza `/competitive-intelligence?days=1` co godzinę
2. Jeśli `priority: "high"` → wyślij notyfikację do zespołu
3. Lub użyj Monday.com automation do trackowania `competitor_mentioned`

### 10. Dashboard Monitoring

Ustaw dashboard w Monday.com:

1. Widget: "Lead Score Distribution"
   - Grupuj leady po `lead_score`
   - Range: 0-39 (low), 40-69 (medium), 70-100 (high)

2. Widget: "Competitor Mentions"
   - Pokaż leady gdzie `competitor_mentioned` is not empty
   - Sortuj po dacie utworzenia

3. Widget: "A/B Test Performance"
   - External iframe: `https://YOUR-APP/admin/ab-test-dashboard`
   - (do zbudowania później)

## Troubleshooting

### Problem: Migracja nie działa na produkcji

```bash
# Sprawdź czy wszystkie zmienne środowiskowe są ustawione
gcloud app ssh
env | grep DATABASE_URL

# Ręcznie uruchom SQL
psql $DATABASE_URL
```

### Problem: A/B testy nie trackują responses

- Sprawdź czy `conversation.followup_variant` jest ustawiane
- Sprawdź logi: `gcloud app logs tail | grep "A/B Test"`
- Sprawdź czy `track_ab_test_response()` jest wywoływana

### Problem: Competitive intel nie wykrywa konkurencji

- Sprawdź czy słowa kluczowe są case-insensitive
- Dodaj więcej konkurentów do listy w `detect_competitive_intelligence()`
- Sprawdź logi: `gcloud app logs tail | grep "Competitive Intel"`

### Problem: Monday.com nie zapisuje nowych pól

- Sprawdź czy kolumny są DOKŁADNIE nazwane jak w kodzie
- Sprawdź czy typy kolumn są poprawne (Number, Text)
- Test połączenia: `/api/chatbot/test-monday`

## Success Criteria

✅ Migracja wykonana - 3 tabele utworzone
✅ 3 domyślne testy A/B aktywne
✅ Monday.com board ma 3 nowe kolumny
✅ Test conversation z konkurencją → zapisuje intel
✅ Lead creation → Monday.com ma wypełnione lead_score i competitor_mentioned
✅ A/B tests trackują impressions i responses
✅ Admin endpointy działają

## Następne Kroki

1. Monitoruj przez 7 dni aby zebrać wystarczająco danych do A/B testów
2. Po 100+ impressions sprawdź wyniki i wybierz zwycięzców
3. Analizuj competitive intelligence co tydzień
4. Dostosuj strategie sprzedażowe na podstawie danych

Powodzenia! 🚀
