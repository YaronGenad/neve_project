#!/usr/bin/env bash
# ── backup.sh ─────────────────────────────────────────────────────────────────
# Database backup for the LOCAL development Postgres container.
#
# For Aurora Serverless (production): Aurora handles automated backups and
# point-in-time recovery natively — no manual backup script is needed.
# See DEPLOYMENT.md §6 for Aurora backup configuration.
#
# Usage (dev):
#   ./scripts/backup.sh                      → saves to backups/YYYY-MM-DD_HHMMSS.sql.gz
#   BACKUP_DIR=/mnt/backups ./scripts/backup.sh
#
# Restore: ./scripts/restore.sh backups/YYYY-MM-DD_HHMMSS.sql.gz

set -euo pipefail

CONTAINER="${DB_CONTAINER:-alhasade-db-1}"
DB_NAME="${POSTGRES_DB:-alhasade}"
DB_USER="${POSTGRES_USER:-alhasade}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
TIMESTAMP=$(date +"%Y-%m-%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"

echo "==> Backing up $DB_NAME from container $CONTAINER"
docker exec "$CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"

SIZE=$(du -sh "$BACKUP_FILE" | cut -f1)
echo "==> Backup saved: $BACKUP_FILE ($SIZE)"

# Optional: remove backups older than 30 days
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +30 -delete 2>/dev/null && echo "==> Cleaned old backups" || true
