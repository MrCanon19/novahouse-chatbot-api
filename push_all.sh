#!/bin/bash
set -euo pipefail

REPO_DIR="$HOME/novahouse-import/novahouse-chatbot-api"
BACKUP_DIR="$REPO_DIR/backups"
DATE_DIR="icloud-$(date +%F)"
DEST_DIR="$BACKUP_DIR/$DATE_DIR"
POBRANE_DIRS=("$HOME/Pobrane" "$HOME/Downloads" "$HOME/Pobrane rzeczy" "$HOME/Desktop")

cd "$REPO_DIR"

echo "📦 Sprawdzam zmiany i ewentualny plik Backup.zip..."

# Szukaj Backup*.zip w typowych katalogach
BACKUP_FILE=""
for d in "${POBRANE_DIRS[@]}"; do
  if [ -d "$d" ]; then
    found=$(find "$d" -maxdepth 1 -type f \( -iname 'Backup.zip' -o -iname 'Backup *.zip' -o -iname 'Backup(*).zip' \) | head -n1 || true)
    if [ -n "${found:-}" ]; then
      BACKUP_FILE="$found"
      break
    fi
  fi
done

if [ -n "$BACKUP_FILE" ]; then
  echo "🗂️  Znaleziono plik: $BACKUP_FILE"
  mkdir -p "$DEST_DIR"
  echo "📤 Rozpakowuję do $DEST_DIR ..."
  TMPDIR="$(mktemp -d)"
  if command -v unzip >/dev/null 2>&1; then
    unzip -q "$BACKUP_FILE" -d "$TMPDIR"
  elif command -v ditto >/dev/null 2>&1; then
    ditto -x -k "$BACKUP_FILE" "$TMPDIR"
  else
    echo "Brak unzip/ditto. Zainstaluj unzip lub użyj macOS 'ditto'."
    exit 1
  fi
  rsync -a "$TMPDIR"/ "$DEST_DIR"/
  rm -rf "$TMPDIR"
  echo "✅ Backup został rozpakowany do: $DEST_DIR"
else
  echo "ℹ️  Nie znaleziono nowego Backup.zip — pomijam etap importu."
fi

echo "🔄 Commituję i wysyłam zmiany..."
git add .
MSG="Auto-backup $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$MSG" || echo "Brak nowych zmian."
git push

echo
echo "✅ Wszystko gotowe! Zmiany wysłane o $(date '+%H:%M:%S')."
git status -sb
