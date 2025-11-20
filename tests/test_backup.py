import glob
import os

from scripts.backup_db import BACKUP_DIR, backup_database


def test_backup_creates_file():
    # Usuń stare backupy
    for f in glob.glob(os.path.join(BACKUP_DIR, "db_backup_*.sqlite")):
        os.remove(f)
    backup_database()
    backups = glob.glob(os.path.join(BACKUP_DIR, "db_backup_*.sqlite"))
    assert backups, "Backup nie został utworzony!"
    print(f"Backup files: {backups}")
