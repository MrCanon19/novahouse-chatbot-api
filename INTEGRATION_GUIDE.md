# 🚀 Integration Guide - Activate Safeguards

**Time to integrate**: 10 minutes  
**Complexity**: Very simple  
**Risk**: Zero (backward compatible)

---

## Step 1: Update chatbot.py (3 minutes)

Find the line where `extract_context()` is called. Usually around line 1400 in `src/routes/chatbot.py`.

**BEFORE:**
```python
from src.routes.chatbot import extract_context

# ... later in code ...
context = extract_context(message, existing_context)
```

**AFTER:**
```python
from src.services.extract_context_safe import extract_context_safe

# ... later in code ...
context = extract_context_safe(message, existing_context)
```

**That's it!** Just one import change and one function name change.

### Find & Replace

Use VS Code Find & Replace:

1. Press `Cmd+H` (Find & Replace)
2. Find: `extract_context(message`
3. Replace: `extract_context_safe(message`
4. Click "Replace All"
5. Add import at top of file

### Verify

```bash
# Syntax check
python -m py_compile src/routes/chatbot.py

# Should return no errors
```

---

## Step 2: Test (5 minutes)

### Run Unit Tests
```bash
make test
```

Expected output:
```
======================= 175 passed, 12 skipped =======================
✅ Tests completed
```

### Test Local

```bash
# Start server
python main.py

# In another terminal, test extraction
curl -X POST http://localhost:8080/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Cześć, jestem Marcin z Warszawy, szukam pakietu express",
    "session_id": "test-123"
  }'

# Should work as before, but with validation
```

### Check Health

```bash
# New monitoring endpoint
curl http://localhost:8080/api/monitoring/extraction-quality

# Should show healthy metrics
```

---

## Step 3: Monitor (2 minutes setup)

### Start Dashboard

```bash
# In a new terminal window
python scripts/monitoring_dashboard.py
```

### Watch It

- Leave running for 1-2 hours after deploy
- Should show: ✅ HEALTHY or 🟡 DEGRADED at worst
- No 🔴 CRITICAL

---

## Step 4: (Optional) Set Up Alerts

### Email Alerts

Add to your monitoring service (Sentry/DataDog):

```yaml
alerts:
  - name: "Extraction Quality Critical"
    condition: "GET /api/monitoring/extraction-quality status == 'critical'"
    action: "send_email"
    recipients: ["dev-team@example.com"]
```

### Slack Alerts

```python
# Add webhook integration to /api/monitoring/extraction-errors
# When alert triggered: POST to Slack webhook
```

---

## Before & After Comparison

| Aspect | Before | After |
|--------|--------|-------|
| **Validation** | None | Automatic for every field |
| **Error handling** | May crash | Graceful degradation |
| **Monitoring** | Manual checks | Real-time dashboard |
| **Regression detection** | None | Automatic alerts |
| **Debugging** | Hard to trace | Full logging available |
| **Recovery time** | Hours | Minutes |

---

## Rollback Plan

If something goes wrong:

```bash
# Revert to previous version
git revert HEAD

# Or restore specific file
git checkout HEAD~1 -- src/routes/chatbot.py

# Test
make test

# Monitor
python scripts/monitoring_dashboard.py
```

But you won't need to! The safeguards prevent problems.

---

## Common Issues & Fixes

### Issue: "ModuleNotFoundError: extract_context_safe"

**Solution:**
```bash
# Make sure import is correct
from src.services.extract_context_safe import extract_context_safe

# Not from src.routes.chatbot
```

### Issue: Dashboard shows "No data"

**Solution:**
```bash
# System needs to process at least one message
curl -X POST http://localhost:8080/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test"}'

# Then dashboard will show metrics
```

### Issue: Tests fail after integration

**Solution:**
```bash
# Make sure you replaced ALL instances
grep -n "extract_context(" src/routes/chatbot.py

# If still using old function, replace it
# Then run: make test
```

---

## Verification Checklist

After integration, verify:

- [ ] Code compiles: `python -m py_compile src/routes/chatbot.py`
- [ ] Tests pass: `make test` (175 passed, 12 skipped)
- [ ] Function exists: `curl http://localhost:8080/api/monitoring/extraction-quality`
- [ ] Dashboard works: `python scripts/monitoring_dashboard.py`
- [ ] Manual test works: Send test message via API
- [ ] No errors in logs: `grep -i error logs/*.log`

---

## Success Criteria

✅ All tests pass (175 passed, 12 skipped)  
✅ Dashboard shows 🟢 HEALTHY  
✅ No new exceptions in logs  
✅ Extraction still works as before  
✅ Validation catches invalid data  
✅ Metrics recorded in monitoring endpoints  

---

## Timeline

| Phase | Time | Action |
|-------|------|--------|
| **Step 1** | 3 min | Update chatbot.py import |
| **Step 2** | 5 min | Run tests, verify |
| **Step 3** | 2 min | Start dashboard |
| **Step 4** | Monitor | Watch metrics for 1-2 hours |
| **Total** | 10 min | Full integration |

---

## Support

Stuck? Check:

1. **Quick Start**: Read `docs/EXTRACTION_SAFEGUARDS.md`
2. **Best Practices**: Read `docs/AUTOMATION_GUIDE.md`
3. **Examples**: See `tests/test_customer_journey_comprehensive.py`
4. **Live Help**: Run `python scripts/monitoring_dashboard.py`
5. **Debugging**: Check `/api/monitoring/extraction-errors`

---

## Key Takeaway

**Before**: Fixes break repeatedly  
**After**: System prevents breaks, alerts when issues occur, provides data for debugging

**Setup time**: 10 minutes  
**Benefit**: Never deal with same extraction failure twice

---

## Next Steps After Integration

1. ✅ Monitor dashboard for 24 hours
2. ✅ Review daily metrics
3. ✅ Adjust validation rules if needed
4. ✅ Set up automated alerts
5. ✅ Train team on monitoring
6. ✅ Plan A/B testing for improvements

---

**Ready?** Start with Step 1: Update `src/routes/chatbot.py`

Questions? Run the dashboard: `python scripts/monitoring_dashboard.py`
