import os
from datetime import datetime

BACKUP_DIR = os.getenv("BACKUP_DIR", "backups/automated/")
DB_PATH = os.getenv("DB_PATH", "src/database.sqlite")


def backup_database():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"db_backup_{timestamp}.sqlite")
    try:
        if not os.path.exists(DB_PATH):
            raise FileNotFoundError(f"Database file not found: {DB_PATH}")
        with open(DB_PATH, "rb") as src, open(backup_file, "wb") as dst:
            dst.write(src.read())
        print(f"Backup completed: {backup_file}")
    except Exception as e:
        print(f"Backup failed: {e}")


if __name__ == "__main__":
    backup_database()
