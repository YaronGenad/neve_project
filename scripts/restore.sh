#!/usr/bin/env bash
# ── restore.sh ────────────────────────────────────────────────────────────────
# Restore a local development Postgres backup produced by backup.sh.
#
# Usage:
#   ./scripts/restore.sh backups/2026-03-28_120000.sql.gz
#
# ⚠️  WARNING: This drops and recreates the database. All data will be lost.
#     Do NOT run against production (Aurora handles restore via AWS Console).

set -euo pipefail

BACKUP_FILE="${1:?Usage: $0 <backup_file.sql.gz>}"
CONTAINER="${DB_CONTAINER:-alhasade-db-1}"
DB_NAME="${POSTGRES_DB:-alhasade}"
DB_USER="${POSTGRES_USER:-alhasade}"

if [[ ! -f "$BACKUP_FILE" ]]; then
  echo "ERROR: Backup file not found: $BACKUP_FILE"
  exit 1
fi

echo "==> WARNING: This will destroy all data in $DB_NAME"
read -r -p "Type 'yes' to continue: " confirm
[[ "$confirm" == "yes" ]] || { echo "Aborted."; exit 1; }

echo "==> Restoring $DB_NAME from $BACKUP_FILE"

# Drop and recreate the database
docker exec "$CONTAINER" psql -U "$DB_USER" -c "DROP DATABASE IF EXISTS $DB_NAME;"
docker exec "$CONTAINER" psql -U "$DB_USER" -c "CREATE DATABASE $DB_NAME;"

# Restore the backup
gunzip -c "$BACKUP_FILE" | docker exec -i "$CONTAINER" psql -U "$DB_USER" -d "$DB_NAME"

echo "==> Restore complete. Run migrations if needed:"
echo "    docker compose exec backend alembic upgrade head"
