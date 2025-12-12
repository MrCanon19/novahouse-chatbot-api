# 🔓 Instrukcja Odszyfrowania Backupów NovaHouse

## 📋 Wymagania

- GPG zainstalowany w systemie
- Klucz GPG zaimportowany
- Passphrase do klucza

## 🔑 Informacje o Kluczu

- **Key ID:** `1485A442EBE7A135AA9CD87B07804FF9F230D9BE`
- **UID:** `Michał Marini <marini19944@gmail.com>`
- **Passphrase:** `8$wK8$o4CfzuoQ2B`

## 📍 Lokalizacja Backupów

### Produkcja (App Engine)
```
/tmp/backups/
```

### Lokalnie
```
backups/automated/
```

### Google Cloud Storage (jeśli skonfigurowane)
```
gs://[BUCKET_NAME]/backups/
```

## 🔓 Odszyfrowanie Backupu

### Metoda 1: Odszyfrowanie do pliku

```bash
# Odszyfruj backup
gpg --decrypt --output backup_20250115_030000.json backup_20250115_030000.json.gpg

# Wprowadź passphrase gdy zostaniesz poproszony
```

### Metoda 2: Odszyfrowanie do stdout

```bash
# Odszyfruj i wyświetl zawartość
gpg --decrypt backup_20250115_030000.json.gpg

# Lub zapisz do pliku
gpg --decrypt backup_20250115_030000.json.gpg > backup_20250115_030000.json
```

### Metoda 3: Automatyczne odszyfrowanie (z passphrase)

```bash
# Ustaw passphrase w zmiennej środowiskowej
export GPG_PASSPHRASE="8$wK8$o4CfzuoQ2B"

# Odszyfruj (GPG użyje passphrase z stdin)
echo "$GPG_PASSPHRASE" | gpg --batch --yes --pinentry-mode loopback \
  --passphrase-fd 0 \
  --decrypt backup_20250115_030000.json.gpg \
  --output backup_20250115_030000.json
```

## ✅ Weryfikacja Odszyfrowania

### Sprawdź czy plik jest poprawny JSON

```bash
# Sprawdź składnię JSON
python3 -m json.tool backup_20250115_030000.json > /dev/null && echo "✅ JSON jest poprawny" || echo "❌ Błąd w JSON"
```

### Sprawdź zawartość backupu

```bash
# Wyświetl strukturę backupu
python3 << EOF
import json
with open('backup_20250115_030000.json', 'r') as f:
    data = json.load(f)
    print(f"Data eksportu: {data.get('export_date')}")
    print(f"Wersja: {data.get('version')}")
    print(f"\nTabele w backupie:")
    for table_name, records in data.get('tables', {}).items():
        print(f"  - {table_name}: {len(records)} rekordów")
EOF
```

## 🔄 Przywracanie z Backupu

### Przywróć dane do bazy (PostgreSQL)

```bash
# 1. Odszyfruj backup
gpg --decrypt backup_20250115_030000.json.gpg > backup_20250115_030000.json

# 2. Zaimportuj dane (użyj skryptu Python)
python3 << EOF
import json
from src.models.chatbot import *
from src.main import app, db

with app.app_context():
    with open('backup_20250115_030000.json', 'r') as f:
        data = json.load(f)
    
    # Importuj dane tabela po tabela
    # UWAGA: To jest przykład - dostosuj do swoich potrzeb
    for table_name, records in data.get('tables', {}).items():
        print(f"Importowanie {table_name}...")
        # Tutaj dodaj logikę importu
EOF
```

## 🛠️ Rozwiązywanie Problemów

### Problem: "gpg: decryption failed: No secret key"

**Rozwiązanie:**
```bash
# Sprawdź czy klucz jest zaimportowany
gpg --list-secret-keys

# Jeśli nie ma klucza, zaimportuj go
gpg --import private_key.asc
```

### Problem: "gpg: decryption failed: Bad session key"

**Rozwiązanie:**
- Sprawdź czy używasz poprawnego passphrase
- Sprawdź czy backup nie jest uszkodzony

### Problem: "gpg: no valid OpenPGP data found"

**Rozwiązanie:**
- Sprawdź czy plik `.gpg` nie jest uszkodzony
- Sprawdź czy to rzeczywiście plik GPG (może być zwykły JSON)

## 📝 Przykładowy Skrypt Automatycznego Odszyfrowania

```python
#!/usr/bin/env python3
"""
Skrypt do automatycznego odszyfrowania backupów NovaHouse
"""

import os
import subprocess
import json
from pathlib import Path

GPG_PASSPHRASE = "8$wK8$o4CfzuoQ2B"
BACKUP_DIR = "backups/automated"

def decrypt_backup(encrypted_file: str, output_file: str = None) -> bool:
    """Odszyfruj backup GPG"""
    if output_file is None:
        output_file = encrypted_file.replace(".gpg", "")
    
    try:
        cmd = [
            "gpg",
            "--batch",
            "--yes",
            "--pinentry-mode", "loopback",
            "--passphrase-fd", "0",
            "--decrypt",
            "--output", output_file,
            encrypted_file,
        ]
        
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        
        stdout, stderr = process.communicate(input=GPG_PASSPHRASE.encode())
        
        if process.returncode == 0:
            print(f"✅ Odszyfrowano: {output_file}")
            return True
        else:
            print(f"❌ Błąd odszyfrowania: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False

def verify_backup(backup_file: str) -> bool:
    """Zweryfikuj czy backup jest poprawny JSON"""
    try:
        with open(backup_file, 'r') as f:
            data = json.load(f)
        
        print(f"✅ Backup jest poprawny")
        print(f"   Data eksportu: {data.get('export_date')}")
        print(f"   Wersja: {data.get('version')}")
        
        for table_name, records in data.get('tables', {}).items():
            print(f"   - {table_name}: {len(records)} rekordów")
        
        return True
    except Exception as e:
        print(f"❌ Backup jest niepoprawny: {e}")
        return False

if __name__ == "__main__":
    # Znajdź najnowszy backup
    backup_dir = Path(BACKUP_DIR)
    encrypted_backups = list(backup_dir.glob("backup_*.json.gpg"))
    
    if not encrypted_backups:
        print("❌ Nie znaleziono zaszyfrowanych backupów")
        exit(1)
    
    # Weź najnowszy
    latest_backup = max(encrypted_backups, key=lambda p: p.stat().st_mtime)
    print(f"📁 Najnowszy backup: {latest_backup.name}")
    
    # Odszyfruj
    output_file = latest_backup.with_suffix('')  # Usuń .gpg
    if decrypt_backup(str(latest_backup), str(output_file)):
        # Zweryfikuj
        verify_backup(str(output_file))
```

## 🔒 Bezpieczeństwo

⚠️ **WAŻNE:**
- Nigdy nie commituj passphrase do repozytorium
- Przechowuj passphrase w bezpiecznym miejscu (password manager)
- Używaj zmiennych środowiskowych dla passphrase w skryptach
- Regularnie rotuj klucze GPG (co 6-12 miesięcy)

## 📞 Kontakt

W razie problemów z odszyfrowaniem backupów, skontaktuj się z:
- **Email:** marini1944@gmail.com
- **Telegram:** Grupa monitoringu backupów

