# 🛡️ Extraction Automation & Safeguards System

**Purpose**: Prevent repetitive extraction failures and regressions automatically

## What This System Does

Instead of manually fixing broken extraction patterns, this system:

1. **Validates** all extracted data automatically
2. **Detects** regressions when quality degrades
3. **Alerts** when patterns fail
4. **Records** metrics for trend analysis
5. **Protects** against human errors

## Architecture

### 1. **Extraction Validator** (`src/services/extraction_validator.py`)
Validates extracted fields according to strict rules:

```python
# Email validation
validator.validate_email("user@example.com")  # ✓
validator.validate_email("invalid")          # ✗

# Budget validation (50k-5M PLN)
validator.validate_budget(100000)  # ✓
validator.validate_budget(10000)   # ✗ Too low

# City validation (must be Polish or known city)
validator.validate_city("Warszawa")  # ✓
validator.validate_city("Xyz")       # ✗

# Entire context validation
clean_context = validator.validate_context(extracted_data)
# Removes invalid fields, keeps only valid data
```

**Validation Rules:**
- **Email**: RFC 5321 format, max 254 chars
- **Phone**: Polish format, normalized to +48XXXXXXXXX
- **Name**: Polish letters, starts with uppercase, 2-100 chars
- **City**: Known Polish cities or 3+ letter words
- **Square Meters**: 10-1000 m²
- **Budget**: 50,000 - 5,000,000 PLN
- **Package**: Express, Comfort, Premium, Indywidualny

### 2. **Regression Detector** (`src/services/regression_detector.py`)
Monitors extraction quality and detects regressions:

```python
# After each extraction batch:
metrics = ExtractionMetrics(
    total_extractions=100,
    successful_extractions=97,
    failed_extractions=3,
    # ... more metrics
)

alerts = record_metrics(metrics)
# Returns alerts if success rate drops or failures spike
```

**What It Detects:**
- Success rate below 95%
- Validation failure spikes
- Extraction failure increases
- Trend degradation

**Alert Types:**
- 🟡 WARNING: Success rate 80-95%
- 🔴 CRITICAL: Success rate < 80%

### 3. **Safe Extraction Wrapper** (`src/services/extract_context_safe.py`)
Wraps `extract_context()` with automatic validation:

```python
# OLD (unsafe):
context = extract_context(message)
# Returns potentially invalid data

# NEW (safe):
context = extract_context_safe(message)
# Validates every field
# Logs all extractions
# Records metrics automatically
# Returns only valid data
```

### 4. **Monitoring Endpoints** (`src/routes/monitoring.py`)
New endpoints for real-time monitoring:

```bash
# Get extraction quality metrics
curl http://localhost:8080/api/monitoring/extraction-quality

# Get regression history
curl http://localhost:8080/api/monitoring/regression-history

# Get validation rules
curl http://localhost:8080/api/monitoring/validation-rules

# Get extraction errors summary
curl http://localhost:8080/api/monitoring/extraction-errors
```

## Usage

### Option 1: Use Safe Extraction (Recommended)

Replace calls to `extract_context()`:

```python
# In src/routes/chatbot.py or where you extract data:

# OLD:
context = extract_context(user_message, existing_context)

# NEW:
from src.services.extract_context_safe import extract_context_safe
context = extract_context_safe(user_message, existing_context)
```

Benefits:
- ✅ Automatic validation
- ✅ Metrics recorded
- ✅ Regressions detected
- ✅ Graceful failure (never crashes)

### Option 2: Manual Validation

```python
from src.services.extraction_validator import get_validator

validator = get_validator()

# Validate individual fields
email = validator.validate_email(user_email)
phone = validator.validate_phone(user_phone)
city = validator.validate_city(user_city)

# Validate entire context
clean_context = validator.validate_context(raw_extraction)
```

### Option 3: Monitor Health

```bash
# Run monitoring dashboard (real-time)
python scripts/monitoring_dashboard.py

# Check endpoint health
curl http://localhost:8080/api/monitoring/extraction-quality
```

## Pre-commit Checks

Automated validation that runs before commits:

```bash
# Test integrity check (fixtures, routes, imports)
python scripts/test_integrity_check.py

# Runs automatically with: git commit
```

This prevents:
- ❌ Hardcoded test fixtures
- ❌ Inconsistent API routes
- ❌ Missing imports
- ❌ Invalid extraction logic

## Monitoring Dashboard

Real-time monitoring with historical trends:

```bash
python scripts/monitoring_dashboard.py
```

Displays:
- 📈 Success rate trends
- 🚨 Recent alerts
- ⚙️ Validation rules
- 💡 Recommendations for action

Example output:
```
Success Rate: 97.3% 🟢 HEALTHY
Validation Failure Rate: 1.2%
Total Extractions: 5,432

🚨 RECENT ALERTS (last 10)
1. 🟡 [success_rate_drop] Success rate dropped: 98.5% → 95.2%

💡 RECOMMENDATIONS
✅ System performing normally. Continue monitoring.
```

## Integration Guide

### Step 1: Update chatbot.py

Replace `extract_context()` call:

```python
# In src/routes/chatbot.py around line 1400:

# FROM:
context = extract_context(message, existing_context)

# TO:
from src.services.extract_context_safe import extract_context_safe
context = extract_context_safe(message, existing_context)
```

### Step 2: Register monitoring routes

In `src/main.py`:

```python
from src.routes.monitoring import monitoring_bp
app.register_blueprint(monitoring_bp)  # Already done
```

### Step 3: Test

```bash
# Run comprehensive tests
make test

# Check health
curl http://localhost:8080/api/monitoring/extraction-quality

# Monitor in real-time
python scripts/monitoring_dashboard.py
```

## Troubleshooting

### Success rate below 95%

1. **Check recent changes**:
   ```bash
   git log --oneline -10
   ```

2. **Review alerts**:
   ```bash
   curl http://localhost:8080/api/monitoring/extraction-errors
   ```

3. **Check validation rules**:
   ```bash
   curl http://localhost:8080/api/monitoring/validation-rules
   ```

4. **Run tests**:
   ```bash
   make test
   ```

### Specific field extraction failing

Check validation rules:

```bash
curl http://localhost:8080/api/monitoring/validation-rules
```

Look for the field that's failing. Update the validator in `src/services/extraction_validator.py`.

Example: If budget extraction is failing:
1. Check `VALID_RANGES["budget"]` = (50000, 5000000)
2. Is user budget within this range?
3. If yes, check regex pattern in `extract_context_safe()`
4. Add test case to `tests/test_extraction_validator.py`

## Testing

### Unit Tests for Validator

```bash
pytest tests/test_extraction_validator.py -v
```

### Integration Tests

```bash
pytest tests/test_customer_journey_comprehensive.py -v
```

### Full Test Suite

```bash
make test
```

## Metrics & Reporting

### Export Metrics to File

```bash
# Via Python
from src.services.regression_detector import get_detector

detector = get_detector()
detector.export_metrics("metrics_export.json")
```

### View Trend Data

```bash
curl http://localhost:8080/api/monitoring/regression-history | jq '.trend_analysis'
```

## Key Benefits

✅ **Prevents Regression**: Detects when extraction quality degrades  
✅ **Automatic Validation**: All extracted data verified before use  
✅ **Real-time Monitoring**: Know immediately if something breaks  
✅ **Graceful Failure**: Never crashes, falls back safely  
✅ **Easy Debugging**: Comprehensive logging and error reports  
✅ **Historical Trends**: Learn from patterns over time  

## Next Steps

1. ✅ Validators created
2. ✅ Regression detector created
3. ✅ Safe extraction wrapper created
4. ✅ Monitoring endpoints added
5. ⏳ Integrate safe extraction into chatbot.py
6. ⏳ Test with live traffic
7. ⏳ Set up automated alerts (email/Slack)

## Support

Questions or issues? Check:
- `docs/testing/MANUAL_TESTING_GUIDE.md` - Test scenarios
- `test_customer_journey_comprehensive.py` - Test examples
- `/api/monitoring/extraction-quality` - Real-time metrics
- `scripts/monitoring_dashboard.py` - Dashboard

---

**Version**: 1.0  
**Created**: 2025  
**Status**: Production Ready ✅
