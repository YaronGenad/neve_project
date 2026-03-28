#!/usr/bin/env bash
# ── health-check.sh ───────────────────────────────────────────────────────────
# Verify all production services are healthy.
# Run on the LightSail server or from any machine with curl access.
#
# Usage:
#   ./scripts/health-check.sh                    → checks localhost
#   DOMAIN=yourdomain.com ./scripts/health-check.sh → checks production

set -euo pipefail

DOMAIN="${DOMAIN:-localhost}"
SCHEME="${SCHEME:-http}"
BASE_URL="$SCHEME://$DOMAIN"
PASS=0
FAIL=0

check() {
  local name="$1"
  local url="$2"
  local expect="${3:-200}"

  HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" --max-time 10 "$url" || echo "000")
  if [[ "$HTTP_CODE" == "$expect" ]]; then
    echo "  ✓ $name ($HTTP_CODE)"
    ((PASS++)) || true
  else
    echo "  ✗ $name — expected $expect, got $HTTP_CODE  ($url)"
    ((FAIL++)) || true
  fi
}

echo "==> Health Check: $BASE_URL"
echo ""

echo "── HTTP endpoints ────────────────────────────────────────────────────────"
check "Root"            "$BASE_URL/"
check "Health"          "$BASE_URL/health"
check "Metrics"         "$BASE_URL/metrics"

echo ""
echo "── Auth guards ───────────────────────────────────────────────────────────"
check "Generations (no auth → 401/403)" "$BASE_URL/api/generations/" "401"
check "Search (no auth → 401/403)"      "$BASE_URL/api/search/?q=test" "401"

echo ""
echo "── Docker container status ───────────────────────────────────────────────"
if command -v docker &> /dev/null; then
  for svc in nginx frontend backend redis; do
    STATUS=$(docker inspect --format='{{.State.Health.Status}}' "alhasade-$svc-1" 2>/dev/null || echo "not_found")
    if [[ "$STATUS" == "healthy" ]]; then
      echo "  ✓ $svc: healthy"
      ((PASS++)) || true
    else
      echo "  ✗ $svc: $STATUS"
      ((FAIL++)) || true
    fi
  done
else
  echo "  (docker not available — skipping container checks)"
fi

echo ""
echo "── Summary ───────────────────────────────────────────────────────────────"
echo "  Passed: $PASS  |  Failed: $FAIL"
echo ""

if [[ $FAIL -gt 0 ]]; then
  echo "HEALTH CHECK FAILED — review errors above"
  exit 1
fi
echo "All checks passed!"
