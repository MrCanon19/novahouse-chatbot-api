import glob
import os

from scripts.backup_db import BACKUP_DIR, backup_database


def test_backup_creates_file():
    # Usuń stare backupy
    for f in glob.glob(os.path.join(BACKUP_DIR, "db_backup_*.sqlite")):
        os.remove(f)

    # Przygotuj przykładową bazę SQLite
    import sqlite3

    db_path = "src/database.sqlite"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO test (name) VALUES ('test')")
    conn.commit()
    conn.close()

    backup_database()
    backups = glob.glob(os.path.join(BACKUP_DIR, "db_backup_*.sqlite"))
    assert backups, "Backup nie został utworzony!"
    # Sprawdź, czy backup nie jest pusty
    for b in backups:
        assert os.path.getsize(b) > 0, f"Backup jest pusty: {b}"
    print(f"Backup files: {backups}")
