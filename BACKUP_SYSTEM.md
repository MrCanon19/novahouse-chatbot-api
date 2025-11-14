# 🔄 System Backupów

## 📋 Przegląd

System automatycznych backupów z **inteligentnym czyszczeniem** starych plików.

## ⚙️ Konfiguracja

### Automatyczne Backupy

**Harmonogram:**
- ⏰ Codziennie o **3:00 AM** (czas serwera)
- 📦 Format: JSON
- 💾 Lokalizacja: `backups/automated/`
- 🗑️ Automatyczne usuwanie po **30 dniach**

**Co jest backupowane:**
- ✅ Users (użytkownicy)
- ✅ Chat Sessions (sesje)
- ✅ Messages (wiadomości)
- ✅ Leads (leady)
- ✅ Bookings (rezerwacje)
- ✅ Analytics (statystyki)

### Czyszczenie Starych Backupów

**Automatyczne:**
- 🔄 Uruchamiane **po każdym backupie**
- 📅 Usuwa backupy starsze niż **30 dni**
- 🎯 Trzyma zawsze minimum ostatniego backup

**Manualne:**
```bash
# Via API
curl -X POST https://your-app.appspot.com/api/backup/cleanup \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"days_to_keep": 30}'
```

## 🔌 API Endpoints

### 1. Tworzenie Backupu
```bash
POST /api/backup/export
Headers: X-API-Key: YOUR_API_KEY

Body:
{
  "format": "json"  # lub "csv"
}

Response:
{
  "success": true,
  "message": "Backup created successfully",
  "filepath": "/path/to/backup_20251114_030000.json"
}
```

### 2. Lista Backupów
```bash
GET /api/backup/list
Headers: X-API-Key: YOUR_API_KEY

Response:
{
  "success": true,
  "data": [
    {
      "filename": "backup_20251114_030000.json",
      "size": 1048576,
      "created_at": "2025-11-14T03:00:00Z"
    }
  ],
  "count": 1
}
```

### 3. Czyszczenie Starych Backupów
```bash
POST /api/backup/cleanup
Headers: X-API-Key: YOUR_API_KEY

Body:
{
  "days_to_keep": 30  # Opcjonalne, domyślnie 30
}

Response:
{
  "success": true,
  "message": "Cleanup completed",
  "deleted_count": 5,
  "days_kept": 30
}
```

### 4. Pobranie Backupu
```bash
GET /api/backup/download/backup_20251114_030000.json
Headers: X-API-Key: YOUR_API_KEY

Response: Binary file download
```

## 📊 Monitoring

### Logi Backupów

**Backup Success:**
```
✅ Automated backup created: /path/to/backup_20251114_030000.json
✅ Cleaned up 3 old backup(s)
```

**Cleanup:**
```
🗑️  Deleted old backup: backup_20251015_030000.json
🗑️  Deleted old backup: backup_20251016_030000.json
✅ Cleaned up 2 old backup(s)
```

**No Cleanup Needed:**
```
✅ No old backups to clean (keeping last 30 days)
```

### Sprawdzanie Statusu

```bash
# Lokalnie
ls -lh backups/automated/

# Via API
curl https://your-app.appspot.com/api/backup/list \
  -H "X-API-Key: YOUR_API_KEY"
```

## 🔧 Konfiguracja Zaawansowana

### Zmiana Okresu Przechowywania

**W kodzie** (`src/services/backup_service.py`):
```python
# Zmień days_to_keep na żądaną wartość
self.cleanup_old_backups(days_to_keep=60)  # 60 dni
```

**Przez API:**
```bash
curl -X POST https://your-app.appspot.com/api/backup/cleanup \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"days_to_keep": 60}'
```

### Zmiana Harmonogramu

**W kodzie** (`src/services/backup_service.py`):
```python
# Zmień godzinę backupu
trigger=CronTrigger(hour=2, minute=30),  # 2:30 AM
```

### Dodatkowe Backupy

**Przed ważnymi zmianami:**
```bash
curl -X POST https://your-app.appspot.com/api/backup/export \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"format": "json"}'
```

## 🔐 RODO Compliance

### Export Danych Użytkownika
```bash
POST /api/rodo/export
Body:
{
  "user_identifier": "user@example.com"
}
```

### Usunięcie Danych Użytkownika
```bash
POST /api/rodo/delete
Body:
{
  "user_identifier": "user@example.com",
  "confirm": true
}
```

## ⚠️ Ważne Uwagi

### Produkcja
- ✅ Backupy są **automatyczne**
- ✅ Stare backupy są **automatycznie usuwane**
- ✅ **Brak ręcznej interwencji** potrzebnej

### Lokalne Środowisko
- 📁 Backupy w `backups/automated/`
- 🚫 **Nigdy nie commituj** backupów do Git
- ✅ Folder już w `.gitignore`

### Bezpieczeństwo
- 🔒 Wszystkie endpointy wymagają **API_KEY**
- 🔐 Backupy zawierają **dane wrażliwe**
- 💾 Przechowuj lokalnie w **bezpiecznej lokalizacji**

## 🎯 Best Practices

1. **Sprawdzaj regularnie:**
   ```bash
   curl https://your-app.appspot.com/api/backup/list -H "X-API-Key: KEY"
   ```

2. **Pobieraj kluczowe backupy:**
   - Przed dużymi wdrożeniami
   - Przed migracjami danych
   - Przed zmianami w bazie

3. **Testuj odzyskiwanie:**
   - Okresowo pobierz backup
   - Sprawdź czy dane są kompletne
   - Przetestuj import na testowej bazie

4. **Monitoruj rozmiar:**
   ```bash
   du -sh backups/automated/
   ```

## 📈 Statystyki

**Typowy rozmiar backupu:**
- Empty database: ~2 KB
- 100 leads: ~50 KB
- 1000 messages: ~500 KB
- Full production: ~1-5 MB

**Przechowywanie:**
- 30 dni × ~5 MB = **150 MB max**
- Nieznaczny wpływ na storage

## 🚨 Troubleshooting

### Backup się nie tworzy
```bash
# Sprawdź logi
tail -f logs/backup.log

# Test manualny
curl -X POST https://your-app.appspot.com/api/backup/export \
  -H "X-API-Key: YOUR_API_KEY"
```

### Cleanup nie działa
```bash
# Sprawdź permissions
ls -la backups/automated/

# Test manualny
curl -X POST https://your-app.appspot.com/api/backup/cleanup \
  -H "X-API-Key: YOUR_API_KEY"
```

### Brak miejsca na dysku
```bash
# Wymuś cleanup
curl -X POST https://your-app.appspot.com/api/backup/cleanup \
  -H "X-API-Key: YOUR_API_KEY" \
  -d '{"days_to_keep": 7}'  # Tylko 7 dni
```

## ✅ Podsumowanie

- ✅ **Automatyczne backupy** codziennie o 3:00
- ✅ **Automatyczne czyszczenie** po 30 dniach
- ✅ **Manualne sterowanie** przez API
- ✅ **RODO compliance** wbudowane
- ✅ **Zero maintenance** w normalnych warunkach

**System działa sam!** 🎉
