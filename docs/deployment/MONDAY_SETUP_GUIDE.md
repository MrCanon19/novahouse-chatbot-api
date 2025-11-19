# Monday.com Board Setup - A/B Testing & Competitive Intelligence

## Wymagane Kolumny

Board ID: **2145240699**  
URL: https://novahouse.monday.com/boards/2145240699

### Istniejące Kolumny (Już są)

- ✅ **Name** - Nazwa leada (domyślna kolumna)
- ✅ **email** - Email (Email type)
- ✅ **phone** - Phone (Phone type)
- ✅ **text** / **message** - Wiadomość (Text type)
- ✅ **package** - Pakiet (Dropdown: Express, Express Plus, Comfort, Premium)
- ✅ **confidence** - Zaufanie/Confidence (Number type)
- ✅ **property_type** - Typ nieruchomości (Dropdown: Mieszkanie, Dom)
- ✅ **budget** - Budżet (Text or Currency type)
- ✅ **interior_style** - Styl wnętrz (Dropdown: Minimalistyczny, Industrialny, Skandynawski, etc.)
- ✅ **status** - Status (Status type: New Lead, Contacted, Qualified, Done, Stuck)

---

## 🆕 NOWE KOLUMNY DO DODANIA

### 1. Lead Score
**Nazwa kolumny:** `lead_score`  
**Typ:** Number  
**Zakres:** 0-100  
**Opis:** Automatyczny scoring jakości leada (0-100 punktów)

**Jak dodać:**
1. Kliknij "+" w nagłówku tabeli
2. Wybierz "Number"
3. Nazwa: `lead_score`
4. Ustaw format: Number (bez symbolu waluty)
5. Zapisz

**Interpretacja:**
- 70-100 = High quality lead (call within 1 hour!)
- 40-69 = Medium quality (email within 24h)
- 0-39 = Low quality (nurture campaign)

---

### 2. Competitor Mentioned
**Nazwa kolumny:** `competitor_mentioned`  
**Typ:** Text  
**Opis:** Nazwa konkurenta jeśli użytkownik wspomniał inną firmę

**Jak dodać:**
1. Kliknij "+" w nagłówku tabeli
2. Wybierz "Text"
3. Nazwa: `competitor_mentioned`
4. Zapisz

**Przykładowe wartości:**
- remonteo
- fixly
- remonty
- konkurencja
- inna firma

**Dlaczego ważne:**
- Lead wspomniał konkurencję = wyższa szansa że porównuje oferty
- Wymaga szybszej reakcji sprzedażowej
- Możliwość dopasowania argumentów sprzedażowych

---

### 3. Next Action
**Nazwa kolumny:** `next_action`  
**Typ:** Long Text (lub Text)  
**Opis:** AI-generowana rekomendacja następnej akcji dla zespołu sprzedaży

**Jak dodać:**
1. Kliknij "+" w nagłówku tabeli
2. Wybierz "Long Text"
3. Nazwa: `next_action`
4. Zapisz

**Przykładowe wartości:**
- "Call within 1 hour - high intent, competitor mentioned"
- "Email within 24h - medium quality lead"
- "Nurture campaign - early stage, gather more info"
- "Priority call - score 85/100, ready to buy"

**Jak używać:**
- Filtruj board po Next Action zawierające "Call within 1 hour"
- Ustaw automation: jeśli `next_action` zawiera "Priority" → wyślij notyfikację do managera
- Dashboard widget: top 5 leads z "Call within 1 hour"

---

## Weryfikacja Setup

Po dodaniu kolumn, uruchom test:

```bash
curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/test-monday \
  -H "X-API-KEY: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
```

Oczekiwany wynik:
```json
{
  "message": "Monday.com connection successful",
  "test_item_id": "1234567890",
  "api_key_set": true,
  "board_id_set": true
}
```

Sprawdź w Monday.com czy testowy item ma wypełnione:
- `lead_score` = 90
- `competitor_mentioned` = (może być puste w teście)
- `next_action` = (generowany przez system)

---

## Recommended Automations w Monday.com

### 1. High Priority Lead Alert
**Trigger:** When `lead_score` changes to > 70  
**Action:** Send notification to Sales Manager + Move to "Hot Leads" group

### 2. Competitor Alert
**Trigger:** When `competitor_mentioned` is not empty  
**Action:** Send Slack/Teams message: "⚠️ Competitor mentioned in lead {Name}"

### 3. Next Action Reminder
**Trigger:** When `next_action` contains "Call within 1 hour"  
**Action:** Create task for sales rep + Set due date to 1 hour from now

### 4. Auto-Qualify Status
**Trigger:** When `lead_score` > 70 AND `email` is not empty  
**Action:** Change `status` to "Qualified"

---

## Dashboard Widgets

### Widget 1: Lead Quality Distribution
**Type:** Chart  
**Data:**
- Group by: `lead_score` ranges (0-39, 40-69, 70-100)
- Show: Count of leads per range

### Widget 2: Competitor Intelligence
**Type:** Table  
**Filter:** Where `competitor_mentioned` is not empty  
**Sort:** By creation date (newest first)  
**Columns:** Name, Competitor Mentioned, Lead Score, Next Action

### Widget 3: Action Queue
**Type:** Table  
**Filter:** Where `next_action` contains "Call within"  
**Sort:** By `lead_score` (highest first)  
**Columns:** Name, Phone, Lead Score, Next Action, Status

---

## Best Practices

1. **Review daily:** Check leads with `lead_score` > 70 every morning
2. **Competitive response:** Leads with `competitor_mentioned` → use comparison script
3. **Follow next_action:** System recommendations są AI-powered - zaufaj im
4. **Update status:** Po kontakcie zmień status aby tracking był aktualny
5. **Feedback loop:** Jeśli lead z score 80+ nie konwertuje → zgłoś do analizy

---

## Troubleshooting

### Problem: Kolumna nie wyświetla się
- Sprawdź czy nazwa jest DOKŁADNIE jak w dokumentacji (case sensitive!)
- Sprawdź uprawnienia - musisz być adminem board

### Problem: Wartości nie zapisują się
- Test connection: `/api/chatbot/test-monday`
- Sprawdź logi: `gcloud app logs tail | grep Monday`
- Verify API key w app.yaml

### Problem: Duplikaty leadów
- System sprawdza po `email` - jeśli ten sam email = update, nie create
- Jeśli potrzeba inne behavior → zgłoś issue

---

## Kontakt

W razie problemów:
- GitHub Issues: https://github.com/MrCanon19/novahouse-chatbot-api/issues
- Check logs: `gcloud app logs tail -s default`
- Admin API: `/api/chatbot/stats/leads` dla overview

**Setup complete = Ready for production lead management! 🚀**
