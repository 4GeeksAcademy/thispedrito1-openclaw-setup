#!/bin/bash
# 4Geeks Progress Skill - Resumen de progreso en el curso
# Uso: ./4geeks_progress.sh [--cohort slug|name] [--json]

set -e

BASE_URL="https://breathecode.herokuapp.com/v1"
[ -n "$FOURGEEKS_API_URL" ] && BASE_URL="$FOURGEEKS_API_URL"

ENV_FILE="/root/.openclaw/.env"
FG_TOKEN=$(grep '^4GEEKS_TOKEN=' "$ENV_FILE" 2>/dev/null | head -1 | cut -d= -f2-)

if [ -z "$FG_TOKEN" ]; then
  echo '{"error":"4GEEKS_TOKEN not found"}' >&2
  exit 1
fi

COHORT_FILTER=""
OUTPUT_JSON=0

while [ $# -gt 0 ]; do
  case "$1" in
    --cohort) COHORT_FILTER="$2"; shift 2 ;;
    --json) OUTPUT_JSON=1; shift ;;
    *) echo "Usage: $0 [--cohort slug|name] [--json]" >&2; exit 1 ;;
  esac
done

# Obtener user ID
USER_ID=$(curl -sL --connect-timeout 10 --max-time 30 \
  -H "Authorization: Token ${FG_TOKEN}" \
  -H "Accept: application/json" \
  "${BASE_URL}/admissions/user/me" \
  | python3 -c "import json,sys; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)

if [ -z "$USER_ID" ]; then
  echo '{"error":"Failed to get user ID"}' >&2
  exit 1
fi

export COHORT_FILTER
[ "$OUTPUT_JSON" = "1" ] && export OUTPUT_JSON=1 || export OUTPUT_JSON=0

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

{
  echo "---USER---"
  curl -sL --connect-timeout 10 --max-time 30 \
    -H "Authorization: Token ${FG_TOKEN}" \
    -H "Accept: application/json" \
    "${BASE_URL}/admissions/user/me"
  echo ""
  echo "---TASKS---"
  curl -sL --connect-timeout 10 --max-time 30 \
    -H "Authorization: Token ${FG_TOKEN}" \
    -H "Accept: application/json" \
    "${BASE_URL}/assignment/task?user=${USER_ID}"
} | python3 "${SCRIPT_DIR}/4geeks_progress.py" 2>&1