# 📋 Comprehensive Manual Testing Guide - Customer Journey

## Overview
This guide covers 20+ manual test scenarios for the complete customer journey: greeting → chat → data collection → lead creation → integrations (Monday.com, ZenCal).

---

## 🎯 TEST SCENARIO SET 1: Basic Data Collection (Tests 1-5)

### TEST 1: Complete Greeting & Introduction
**Objective:** Verify chatbot recognizes user introduction and extracts name correctly

**Steps:**
1. Open chatbot
2. Send: `"Cześć! Jestem Jan Kowalski. Chciałbym się dowiedzieć coś o waszych usługach."`

**Expected Results:**
- ✅ Bot responds warmly
- ✅ Name "Jan Kowalski" extracted to context
- ✅ Bot acknowledges the name

**Verification:**
- Check conversation context shows: `"name": "Jan Kowalski"`
- Check database: `SELECT * FROM leads WHERE name = 'Jan Kowalski'`

**Edge Cases to Try:**
- Polish special characters: "Jestem Józef Żółć"
- Just first name: "Jestem Katarzyna"
- Full name with prefix: "Mam na imię Małgorzata Nowak"

---

### TEST 2: Email Extraction & Validation
**Objective:** Extract and validate email addresses in various formats

**Steps:**
1. Send: `"Mój email to aleksandra.nowak@email.com"`
2. Send: `"Lub mogę być na adresie: aleksandra_nowak@company.pl"`
3. Send: `"Najlepiej na aleksandra+test@gmail.co.uk"`

**Expected Results:**
- ✅ First email extracted: `aleksandra.nowak@email.com`
- ✅ Subsequent emails either update or are acknowledged
- ✅ All standard email formats recognized

**Verification:**
- Database query: `SELECT email FROM leads WHERE email LIKE 'aleksandra%'`
- Check email format validation (RFC 5322 compliant)

**Invalid Cases to Test:**
- `"kontakt na adres test@.com"` → Should NOT save
- `"mogę być na test@domain"` → Should NOT save
- `"email: test@domain..com"` → Should NOT save

---

### TEST 3: Phone Number Extraction - Multiple Formats
**Objective:** Extract Polish phone numbers in various formats

**Steps:**
1. Send: `"Mój numer to 123 456 789"`
2. Send: `"Lub +48 123 456 789"`
3. Send: `"Zadzwoń na 48123456789"`
4. Send: `"Tel. 123-456-789"`

**Expected Results:**
- ✅ Format 1: `123 456 789` extracted
- ✅ Format 2: `+48 123 456 789` extracted
- ✅ Format 3: `48123456789` extracted
- ⚠️ Format 4: May or may not work (depends on implementation)

**Verification:**
```sql
SELECT phone FROM leads WHERE phone LIKE '123%' OR phone LIKE '+48%';
```

**Valid Polish Formats:**
- ✅ `123 456 789` (9 digits, spaces)
- ✅ `123456789` (9 digits, no spaces)
- ✅ `+48 123 456 789` (with country code)
- ✅ `48123456789` (48 prefix)

---

### TEST 4: Property Size (Square Meters) Extraction
**Objective:** Extract and validate apartment size in various formats

**Steps:**
1. Send: `"Mam mieszkanie 85 m²"`
2. Send: `"Metraż to 120 metrów"`
3. Send: `"To będzie 50 m2"`
4. Send: `"Mieszkam na 180 mkw"`

**Expected Results:**
- ✅ Test 1: `85` extracted
- ✅ Test 2: `120` extracted
- ✅ Test 3: `50` extracted
- ✅ Test 4: `180` extracted

**Verification:**
```sql
SELECT property_size FROM leads WHERE property_size IN (85, 120, 50, 180);
```

**Boundary Cases:**
- Too small: `"Mam 5 m²"` → May flag as unusual
- Too large: `"5000 m²"` → May flag as commercial
- Zero: `"0 m²"` → Should reject
- Unrealistic: `"999999 m²"` → Should reject

---

### TEST 5: City Location Extraction
**Objective:** Extract city names with proper Polish normalization

**Steps:**
1. Send: `"Jestem z Warszawy"`
2. Send: `"Mieszkam w Gdańsku"`
3. Send: `"Ze Wrocławia"`
4. Send: `"Z Krakowa"`

**Expected Results:**
- ✅ Test 1: `Warszawa` extracted
- ✅ Test 2: `Gdańsk` extracted
- ✅ Test 3: `Wrocław` extracted
- ✅ Test 4: `Kraków` extracted

**Verification:**
```sql
SELECT DISTINCT location FROM leads WHERE location IS NOT NULL;
```

**Cities Currently Supported:**
- Warszawa, Gdańsk, Wrocław, Sopot, Gdynia, Kraków, Poznań, Łódź (basic)
- 200+ cities via heuristic declension (GUS database)

**Expansion Needed:**
- Smaller cities (Bielsko-Biała, Rybnik, Tychy, etc.)
- Regional variations (Kraków vs. Cracow)

---

## 🎯 TEST SCENARIO SET 2: Package & Budget Selection (Tests 6-10)

### TEST 6: Package Preference Detection
**Objective:** Identify interested finishing package

**Steps:**
1. Send: `"Interesuje mnie pakiet Express"`
2. Send: `"Comfort by był idealny"`
3. Send: `"Premium sounds good"`
4. Send: `"Chyba indywidualny, potrzebuję customizacji"`

**Expected Results:**
- ✅ Test 1: `Express` extracted
- ✅ Test 2: `Comfort` extracted
- ⚠️ Test 3: English "Premium" → May need handling
- ✅ Test 4: `Indywidualny` extracted

**Packages Recognized:**
1. **Express** - Basic finishing, competitive price
2. **Comfort** - Standard finishes, good balance
3. **Premium** - High-end materials, premium finishes
4. **Indywidualny** - Fully customized

**Verification:**
```sql
SELECT interested_package FROM leads WHERE interested_package IS NOT NULL;
```

---

### TEST 7: Budget Extraction - Exact Figures
**Objective:** Extract budget in various formats and validate ranges

**Steps:**
1. Send: `"Mam budżet 500 tys"`
2. Send: `"Dysponuję 300 000 zł"`
3. Send: `"Do wydania mam około 1 tysiąc"`
4. Send: `"Budżet to 100 tys zł"`
5. Send: `"Mogę wydać 1,5 mln"`

**Expected Results:**
- ✅ Test 1: `500000` extracted
- ✅ Test 2: `300000` extracted
- ✅ Test 3: `1000` extracted (or rejected - too low)
- ✅ Test 4: `100000` extracted
- ✅ Test 5: `1500000` extracted

**Budget Validation:**
- ✅ Accept: 50,000 - 5,000,000 PLN
- ❌ Reject: < 50,000 (too low for residential)
- ❌ Reject: > 5,000,000 (likely commercial)

**Verification:**
```sql
SELECT budget FROM leads WHERE budget BETWEEN 50000 AND 5000000;
```

---

### TEST 8: Budget Boundary Cases
**Objective:** Test budget validation boundaries

**Steps:**
1. Send: `"Mam 30 tys" → Expect: NOT saved (too low)`
2. Send: `"Mam 49 999 zł" → Expect: NOT saved (below minimum)`
3. Send: `"Mam 50 000 zł" → Expect: SAVED (minimum accepted)`
4. Send: `"Mam 5 mln" → Expect: SAVED (maximum accepted)`
5. Send: `"Mam 5,1 mln" → Expect: NOT saved (too high)`
6. Send: `"Mam 10 mln" → Expect: NOT saved (commercial range)`

**Verification:**
```sql
SELECT COUNT(*) FROM leads WHERE budget < 50000;  -- Should be 0 (rejected)
SELECT COUNT(*) FROM leads WHERE budget > 5000000; -- Should be 0 (rejected)
```

---

### TEST 9: Complete Data Combination
**Objective:** Test full data collection in single conversation

**Steps:**
Send multiple messages building complete profile:
```
1. "Cześć! Jestem Maria Kowalska"
2. "Email: maria@example.com"
3. "Telefon: 789 456 123"
4. "Mieszkam w Warszawie"
5. "Mam mieszkanie 95 m²"
6. "Interesuje mnie pakiet Premium"
7. "Budżet to 400 tys zł"
```

**Expected Results:**
- ✅ All data extracted correctly
- ✅ No conflicts between extracted fields
- ✅ Lead score should be HIGH (70+)

**Verification:**
```sql
SELECT * FROM leads WHERE name = 'Maria Kowalska'
AND email = 'maria@example.com'
AND phone = '789456123'
AND location = 'Warszawa'
AND property_size = 95
AND interested_package = 'Premium'
AND budget = 400000;
```

---

### TEST 10: Contradictory Data Handling
**Objective:** Test how system handles conflicting information

**Steps:**
1. Send: `"Interesuje mnie Express"`
2. Send: `"Hmm, a może jednak Premium?"`
3. Send: `"Czy mogę mieć coś pomiędzy Express i Comfort?"`

**Expected Results:**
- ✅ System should note latest preference (Premium)
- ✅ Should offer flexibility to customer
- ✅ No error or crash

**Expected Behavior:**
- Last mentioned package takes precedence
- Bot should ask clarifying question if needed
- Context should update to latest value

---

## 🎯 TEST SCENARIO SET 3: Edge Cases & Language (Tests 11-15)

### TEST 11: Typos and Misspellings
**Objective:** Test resilience to common typing errors

**Steps:**
1. Send: `"Jestem z Warszawy" → Correct`
2. Send: `"Jestem z Warszwy" → Missing 'a'`
3. Send: `"Jestem z Warsawa" → Wrong vowel`
4. Send: `"Jestem z Wroclawa" → No special char`

**Expected Results:**
- ✅ Test 1: Recognized
- ⚠️ Test 2-3: May not be recognized (current limitation)
- ⚠️ Test 4: May partially work

**Current Limitations:**
- Fuzzy matching not implemented
- Exact name matching required
- No spell-checker integration

**Recommendation:**
- Consider adding fuzzy matching (Levenshtein distance)
- Add common typo corrections for cities

---

### TEST 12: Polish Special Characters (Ą, Ę, Ó, Ż, etc.)
**Objective:** Verify Polish language support

**Steps:**
1. Send: `"Jestem Józef Żółć"`
2. Send: `"Z Warszawy"`
3. Send: `"Email: ąęóż@example.com"`
4. Send: `"Mam mieszkanie 85 m² w Łódzkie"`

**Expected Results:**
- ✅ Names with Polish chars extracted correctly
- ✅ Emails with Polish chars accepted
- ✅ City names normalized

**Verification:**
- Database should show correct Polish characters
- No UTF-8 encoding issues
- Forms submission should handle correctly

---

### TEST 13: Emojis and Special Characters
**Objective:** Test handling of modern messaging conventions

**Steps:**
1. Send: `"Cześć! 😊 Jestem Jan"`
2. Send: `"Warszawa 🏠"`
3. Send: `"Premium 💎 by był super!"`
4. Send: `"Budget: 300 tys zł 💰"`

**Expected Results:**
- ✅ Emojis should be stripped/ignored
- ✅ Name still extracted: `Jan`
- ✅ City still extracted: `Warszawa`
- ✅ Package still extracted: `Premium`
- ✅ Budget still extracted: `300000`

**Verification:**
- Database should NOT contain emoji characters
- Context extraction should work around emojis
- No parsing errors

---

### TEST 14: Language Mixing (Polish/English)
**Objective:** Test multilingual input

**Steps:**
1. Send: `"Hello! Jestem Jan Kowalski. I'm from Warszawa. Interested in Premium package."`
2. Send: `"My email: jan@example.com, phone: 123456789, flat size: 85 m²"`

**Expected Results:**
- ✅ Name extracted: `Jan Kowalski`
- ✅ City extracted: `Warszawa`
- ✅ Package extracted: `Premium`
- ✅ Email extracted: `jan@example.com`
- ✅ Phone extracted: `123456789`
- ✅ Size extracted: `85`

**Edge Cases:**
- English package names: "express", "comfort" → Should normalize to Polish
- Mixed decimals: "1.500 tys" vs "1,500 tys" → Both formats

---

### TEST 15: Multiple Similar Entities
**Objective:** Test handling of multiple emails/phones/etc.

**Steps:**
1. Send: `"Mam dwa emaile: jan@work.com i jan.personal@gmail.com. Która brać?"`
2. Send: `"Telefony: główny 123456789, dodatkowy 987654321"`
3. Send: `"Mogę mieszkać w Warszawie albo Krakowie"`

**Expected Behavior:**
- First email should be primary: `jan@work.com`
- First phone should be primary: `123456789`
- First city should be primary: `Warszawa`
- Bot should ask for clarification if needed

---

## 🎯 TEST SCENARIO SET 4: Integration Testing (Tests 16-20)

### TEST 16: Booking Intent - ZenCal Integration
**Objective:** Verify ZenCal booking link is generated on demand

**Steps:**
1. Have complete context (name, email)
2. Send: `"Chciałbym umówić spotkanie"`

**Expected Results:**
- ✅ Bot detects booking intent
- ✅ Booking link provided with ZenCal
- ✅ Link pre-filled with customer name/email
- ✅ Link format: `https://booking.zencal.io/...?name=Jan&email=jan@...`

**Booking Keywords to Test:**
- ✅ "umów", "umówić", "umówienie"
- ✅ "spotkanie", "spotkań"
- ✅ "rezerwacja", "rezerwuj"
- ✅ "termin", "terminu"
- ✅ "wizyta", "wizytę"
- ✅ "konsultacja", "konsultację"

**Verification:**
```sql
SELECT * FROM chat_messages WHERE message LIKE '%umów%' OR message LIKE '%booking%';
```

**ZenCal Verification:**
1. Click provided link
2. Confirm personal data is pre-filled
3. Choose appointment time
4. Verify appointment shows in ZenCal dashboard

---

### TEST 17: Lead Creation - Database Persistence
**Objective:** Verify complete lead record is saved to database

**Steps:**
1. Complete full customer journey (name, email, phone, city, size, package, budget)
2. Send: `"Tak, potwierdźam swoje dane"`
3. Check database immediately

**Expected Results in Database:**
```sql
SELECT * FROM leads WHERE session_id = 'your_session_id';
```

**Should contain:**
- ✅ `name`: "Jan Kowalski"
- ✅ `email`: "jan@example.com"
- ✅ `phone`: "123456789"
- ✅ `location`: "Warszawa"
- ✅ `property_size`: 85
- ✅ `interested_package`: "Premium"
- ✅ `source`: "chatbot"
- ✅ `status`: "qualified"
- ✅ `data_confirmed`: true
- ✅ `lead_score`: >= 70
- ✅ `conversation_summary`: Auto-generated
- ✅ `created_at`: Current timestamp

---

### TEST 18: Monday.com Sync - Lead Creation
**Objective:** Verify lead is automatically synced to Monday.com

**Steps:**
1. Complete full customer journey with HIGH lead score (70+)
2. Confirm data
3. Check Monday.com dashboard immediately

**Expected Results in Monday.com:**
- ✅ New item created in "Leads" board
- ✅ Item name: Customer name
- ✅ Fields populated:
  - Name: "Jan Kowalski"
  - Email: jan@example.com
  - Phone: 123456789
  - Lead Score: 82/100
  - Status: "Qualified"
  - Package Interest: "Premium"
  - Budget: 300000 PLN
  - Next Action: "🔥 HIGH PRIORITY - Call within 1 hour"

**Verification:**
1. Go to Monday.com workspace
2. Open "Leads" board
3. Filter by today's date
4. Confirm customer name appears
5. Click item and verify all fields populated

**Monday.com URL:** `https://monday.com/...`

---

### TEST 19: Email Alert for High-Priority Leads
**Objective:** Verify admin email sent for qualified leads (score >= 70)

**Steps:**
1. Complete customer journey with high-priority data
2. Confirm data with score 70+
3. Check admin email inbox

**Expected Email:**
- **To:** admin@novahouse.pl (or configured ADMIN_EMAIL)
- **Subject:** "🔥 HIGH PRIORITY LEAD - Score: 82/100"
- **Content:**
  - Customer name
  - Email & phone
  - Lead score
  - Package interest
  - Monday.com item ID
  - Recommended action

**Verification:**
1. Check email inbox for message from system
2. Verify all data is correct
3. Click Monday.com link in email
4. Confirm item shows on board

---

### TEST 20: Full End-to-End Journey - Greeting to Booking
**Objective:** Complete customer journey in single session

**Chat Flow:**
```
User: "Cześć! Jestem Tomasz Nowak"
Bot: [Greeting & acknowledgment]

User: "Mój email to tomasz@example.com"
Bot: [Confirms email]

User: "Telefon: +48 123 456 789, mieszkam w Warszawie"
Bot: [Confirms location & phone]

User: "Mam mieszkanie 95 m², interesuje mnie Premium"
Bot: [Confirms package interest]

User: "Budżet to 400 tys zł"
Bot: [Calculates lead score, shows it's high priority]

User: "Tak, wszystko jest poprawne"
Bot: [Creates lead, confirms Monday sync]

User: "Chciałbym umówić spotkanie"
Bot: [Provides ZenCal booking link]

User: [Clicks link, schedules appointment]
✅ COMPLETE: Lead created, synced to Monday, appointment scheduled
```

**Verification Checklist:**
- [ ] Lead in database with score >= 70
- [ ] Lead synced to Monday.com
- [ ] Admin email received
- [ ] Booking link generated
- [ ] Appointment visible in ZenCal
- [ ] All data persisted correctly

---

## 🔧 DEBUGGING CHECKLIST

### If Tests Fail

**Step 1: Check Database Connection**
```bash
psql DATABASE_URL -c "SELECT * FROM leads LIMIT 1;"
```

**Step 2: Verify Monday.com Integration**
```bash
# Check if API key is set
echo $MONDAY_API_KEY

# Test Monday client
python -c "from src.integrations.monday_client import MondayClient; m = MondayClient(); print('✅ Monday connected')"
```

**Step 3: Verify ZenCal Integration**
```bash
echo $ZENCAL_API_KEY
python -c "from src.integrations.zencal_client import ZencalClient; z = ZencalClient(); print('✅ ZenCal connected')"
```

**Step 4: Check Logs**
```bash
tail -f logs/chatbot.log
tail -f logs/errors.log
```

**Step 5: Verify Environment Variables**
```bash
cat .env | grep -E "MONDAY|ZENCAL|DATABASE|ADMIN_EMAIL|OPENAI"
```

---

## 📊 TEST RESULTS TRACKING

Use this table to track manual test results:

| Test # | Scenario | Expected | Actual | Status | Notes |
|--------|----------|----------|--------|--------|-------|
| 1 | Greeting & Name | Name extracted | - | - | - |
| 2 | Email | Email saved | - | - | - |
| 3 | Phone | Phone saved | - | - | - |
| 4 | Square Meters | Size extracted | - | - | - |
| 5 | City | Location saved | - | - | - |
| 6 | Package | Package selected | - | - | - |
| 7 | Budget | Budget saved | - | - | - |
| 8 | Boundaries | Budget validated | - | - | - |
| 9 | Full Data | All fields populated | - | - | - |
| 10 | Contradiction | Latest value used | - | - | - |
| 11 | Typos | Partial recognition | - | - | - |
| 12 | Polish Chars | Chars preserved | - | - | - |
| 13 | Emojis | Stripped correctly | - | - | - |
| 14 | Language Mix | All extracted | - | - | - |
| 15 | Multiple | First value used | - | - | - |
| 16 | Booking Intent | ZenCal link | - | - | - |
| 17 | Lead DB | Lead created | - | - | - |
| 18 | Monday Sync | Item created | - | - | - |
| 19 | Email Alert | Email sent | - | - | - |
| 20 | E2E Journey | Full flow | - | - | - |

---

## 🚀 NEXT STEPS

After completing all tests:

1. **Document Failures** - List any tests that failed
2. **Root Cause Analysis** - Why did they fail?
3. **Fix Priority** - Critical vs. Nice-to-have
4. **Implementation** - Update code as needed
5. **Re-test** - Verify fixes work
6. **Release** - Deploy to production

---

## 📞 SUPPORT

Questions? Check:
- `/docs/README.md` - Architecture documentation
- `/src/routes/chatbot.py` - Core chat logic
- `/src/integrations/` - Integration implementations
