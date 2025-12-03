# 💾 DATABASE & PERFORMANCE AUDIT

**Data:** 2025-12-03  
**Status:** 🔴 CRITICAL - Missing Indexes

---

## 🔥 PROBLEM #1: BRAK INDEXES NA FOREIGN KEYS

### Analiza modeli
Przeskanowałem wszystkie modele w `src/models/`:
- `chatbot.py` - 7 tabel, **0 indexes zdefiniowanych**
- `ab_testing.py` - 3 tabele, **0 indexes**  
- `analytics.py` - 2 tabele, **0 indexes**
- `user.py` - 1 tabela

### Foreign Keys bez indexes (CRITICAL!)

#### 1. leads.session_id
```python
# Query używany wszędzie:
Lead.query.filter_by(session_id=session_id).first()
```

**Problem:** Full table scan przy każdym zapytaniu!

**Fix:**
```python
__table_args__ = (
    db.Index('idx_leads_session_id', 'session_id'),
)
```

#### 2. chat_conversations.session_id
```python
# Query używany często:
ChatConversation.query.filter_by(session_id=session_id).first()
```

**Fix:**
```python
__table_args__ = (
    db.Index('idx_chat_conversations_session_id', 'session_id'),
)
```

#### 3. chat_messages.conversation_id (ma FK ale brak indexu)
```python
conversation_id = db.Column(db.Integer, db.ForeignKey("chat_conversations.id"))
```

SQLAlchemy **NIE TWORZY AUTO INDEXU** na FK! PostgreSQL też nie.

**Fix:**
```python
__table_args__ = (
    db.Index('idx_chat_messages_conversation_id', 'conversation_id'),
)
```

#### 4. leads.status (filtrowane często)
```python
# W analytics i filter endpoints:
Lead.query.filter_by(status='new').count()
```

**Fix:**
```python
__table_args__ = (
    db.Index('idx_leads_status', 'status'),
    db.Index('idx_leads_created_at', 'created_at'),  # Dla ORDER BY
)
```

#### 5. audit_logs.session_id (RODO queries)
```python
AuditLog.query.filter(AuditLog.session_id == session_id)
```

**Fix:**
```python
__table_args__ = (
    db.Index('idx_audit_logs_session_id', 'session_id'),
    db.Index('idx_audit_logs_action', 'action'),
)
```

---

## 🐛 PROBLEM #2: N+1 Query Problem

### Znalezione w kodzie

#### 1. src/routes/leads.py:102
```python
leads = Lead.query.order_by(Lead.created_at.desc()).all()

for lead in leads:
    # Jeśli kiedykolwiek dodamy relationships...
    lead.bookings  # ← N+1!
```

**Status:** Currently OK (brak relationships w iteracji)  
**Risk:** MEDIUM - jeśli dodamy eager loading interactions

#### 2. Potencjalny problem w analytics
```python
# src/routes/analytics.py
conversations = ChatConversation.query.all()
for conv in conversations:
    conv.messages  # ← Możliwy N+1!
```

**Fix:** Use eager loading
```python
from sqlalchemy.orm import joinedload

conversations = ChatConversation.query.options(
    joinedload(ChatConversation.messages)
).all()
```

---

## 📊 PROBLEM #3: Connection Pool Config

### Current config (src/main.py:119)
```python
if db_url.startswith("postgresql://"):
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": 3,  # Max 3 connections per instance
        "max_overflow": 1,  # Max 1 additional
        "pool_pre_ping": True,
        "pool_recycle": 1800,  # 30 min
    }
```

### Analiza
- **pool_size=3**: OK dla F2 instance (512 MB RAM)
- **max_overflow=1**: OK, total 4 connections max
- **pool_pre_ping=True**: ✅ Good - detects stale connections
- **pool_recycle=1800**: ✅ Good - prevents timeout issues

### Cloud SQL limits
```
F2 instance (1 max): 4 connections total ✅
Max instances: 5
Theoretical max: 5 × 4 = 20 connections
Cloud SQL tier: db-f1-micro supports 25 connections ✅
```

**Status:** ✅ GOOD - no issues here

---

## 🔍 PROBLEM #4: Missing Query Optimization

### Slow queries identified

#### 1. Dashboard stats (chatbot.py:1440-1448)
```python
total_leads = Lead.query.count()  # Full scan
confirmed_leads = Lead.query.filter_by(data_confirmed=True).count()  # Scan
high_quality = Lead.query.filter(Lead.lead_score >= 70).count()  # Scan
```

**Problem:** 3 separate full table scans!

**Fix:** Single query with aggregation
```python
from sqlalchemy import func, case

stats = db.session.query(
    func.count(Lead.id).label('total'),
    func.sum(case((Lead.data_confirmed == True, 1), else_=0)).label('confirmed'),
    func.sum(case((Lead.lead_score >= 70, 1), else_=0)).label('high_quality')
).first()
```

Reduces 3 queries → 1 query!

#### 2. Conversation history (chatbot.py:1578)
```python
conversation = ChatConversation.query.filter_by(session_id=session_id).first()
# Later...
messages = ChatMessage.query.filter_by(conversation_id=conversation.id).all()
```

**Problem:** 2 queries when 1 suffices

**Fix:** Use relationship with joinedload
```python
conversation = ChatConversation.query.options(
    joinedload(ChatConversation.messages)
).filter_by(session_id=session_id).first()

messages = conversation.messages  # No additional query!
```

#### 3. Lead filtering with pagination (leads.py:313)
```python
query = Lead.query
# Multiple filter_by() calls...
paginated = query.paginate(page=page, per_page=per_page)
```

**Status:** ✅ OK - używa LIMIT/OFFSET properly

---

## 📈 PROBLEM #5: No Query Performance Monitoring

### Missing metrics
- Brak slow query logging
- Brak query execution time tracking
- Brak database connection pool metrics

### Recommendation
```python
# Add to src/utils/logging.py

import time
from functools import wraps

def log_query_time(threshold_ms=100):
    """Log slow queries"""
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            duration_ms = (time.time() - start) * 1000

            if duration_ms > threshold_ms:
                logger.warning(
                    f"Slow query in {f.__name__}: {duration_ms:.2f}ms",
                    extra={"query_time_ms": duration_ms}
                )

            return result
        return wrapped
    return decorator
```

---

## 📊 ESTIMATED IMPACT

### Before Indexes (current)
```
Query: Lead.query.filter_by(session_id='xyz').first()
Execution: SEQUENTIAL SCAN on leads
Cost: O(n) - checks every row
Time: ~50-200ms (depending on table size)
```

### After Indexes (predicted)
```
Query: Same
Execution: INDEX SCAN on idx_leads_session_id
Cost: O(log n) - binary search on index
Time: ~1-5ms
```

**Improvement:** 40-100x faster queries! 🚀

### Impact na API response time
```
BEFORE indexes:
/api/chat: 200-400ms (multiple DB queries)
/api/leads/: 300-500ms (full table scan)

AFTER indexes:
/api/chat: 50-150ms (✅ 60-70% faster)
/api/leads/: 50-100ms (✅ 80% faster)
```

---

## 🛠️ MIGRATION SCRIPT

### Utwórz nową migrację
```bash
# 1. Create migration file
cat > migrations/add_missing_indexes.py << 'EOF'
"""
Add missing database indexes for performance
Run with: python migrations/add_missing_indexes.py
"""

from src.main import app, db
from sqlalchemy import text

def add_indexes():
    """Add missing indexes to improve query performance"""

    indexes = [
        # Leads table
        ("idx_leads_session_id", "leads", "session_id"),
        ("idx_leads_status", "leads", "status"),
        ("idx_leads_created_at", "leads", "created_at"),
        ("idx_leads_email", "leads", "email"),  # For duplicate detection

        # ChatConversation
        ("idx_chat_conv_session_id", "chat_conversations", "session_id"),
        ("idx_chat_conv_started_at", "chat_conversations", "started_at"),

        # ChatMessage
        ("idx_chat_msg_conversation_id", "chat_messages", "conversation_id"),
        ("idx_chat_msg_timestamp", "chat_messages", "timestamp"),

        # AuditLog (RODO)
        ("idx_audit_session_id", "audit_logs", "session_id"),
        ("idx_audit_action", "audit_logs", "action"),
        ("idx_audit_timestamp", "audit_logs", "timestamp"),

        # RodoConsent
        ("idx_rodo_session_id", "rodo_consents", "session_id"),

        # Bookings
        ("idx_bookings_lead_id", "bookings", "lead_id"),
        ("idx_bookings_session_id", "bookings", "session_id"),
    ]

    with app.app_context():
        for index_name, table_name, column_name in indexes:
            try:
                # Check if index exists
                result = db.session.execute(text(f"""
                    SELECT 1 FROM pg_indexes
                    WHERE indexname = '{index_name}'
                """)).fetchone()

                if not result:
                    print(f"Creating index: {index_name}")
                    db.session.execute(text(
                        f"CREATE INDEX {index_name} ON {table_name} ({column_name})"
                    ))
                    db.session.commit()
                    print(f"✅ Created {index_name}")
                else:
                    print(f"⚠️  {index_name} already exists")

            except Exception as e:
                print(f"❌ Error creating {index_name}: {e}")
                db.session.rollback()

if __name__ == "__main__":
    add_indexes()
EOF

# 2. Run migration
python migrations/add_missing_indexes.py
```

---

## 📋 ACTION ITEMS

### 🔴 CRITICAL (Do Immediately)
1. [ ] Create and run index migration script
2. [ ] Verify indexes created in database: `\d+ leads` in psql
3. [ ] Monitor query performance before/after

### 🟠 HIGH (This Week)
4. [ ] Add eager loading to conversation queries
5. [ ] Optimize dashboard stats (3 queries → 1)
6. [ ] Add slow query logging

### 🟡 MEDIUM (This Month)
7. [ ] Add query performance monitoring
8. [ ] Review all .query.all() calls for N+1
9. [ ] Consider adding composite indexes for complex filters

---

## 🎯 MONITORING AFTER FIX

### Verify indexes work
```sql
-- In Cloud SQL psql console
EXPLAIN ANALYZE SELECT * FROM leads WHERE session_id = 'test';

-- Should show:
-- Index Scan using idx_leads_session_id on leads
-- (cost=0.29..8.31 rows=1 width=XXX)
```

### Benchmark improvement
```bash
# Before indexes
time curl -X POST https://APP_URL/api/chat -d '{"message": "test"}'
# ~200-300ms

# After indexes
time curl -X POST https://APP_URL/api/chat -d '{"message": "test"}'
# ~50-100ms expected
```

---

**Raport wygenerowany:** 2025-12-03  
**Auditor:** GitHub Copilot (40 years experience mode)  
**Priority:** 🔴 CRITICAL - Indexes missing = slow production queries
