#!/bin/bash
# 4Geeks BreatheCode API Wrapper
# Usage: ./4geeks_api.sh <endpoint> [method] [data]

set -e

BASE_URL="https://breathecode.herokuapp.com/v1"
[ -n "$FOURGEEKS_API_URL" ] && BASE_URL="$FOURGEEKS_API_URL"

ENV_FILE="/root/.openclaw/.env"

# Read token from env file (bash-safe var name)
if [ -z "$FG_TOKEN" ]; then
  if [ -f "$ENV_FILE" ]; then
    FG_TOKEN="$(grep '^4GEEKS_TOKEN=' "$ENV_FILE" | head -1 | cut -d= -f2-)"
  fi
fi

if [ -z "$FG_TOKEN" ]; then
  echo '{"error":"4GEEKS_TOKEN not found"}' >&2
  exit 1
fi

if [ $# -eq 0 ]; then
  echo "Usage: $0 <endpoint> [method] [data]"
  exit 1
fi

ENDPOINT="$1"
METHOD="${2:-GET}"
DATA="${3:-}"

URL="${BASE_URL}/${ENDPOINT}"
URL="${URL%/}"

CURL_ARGS=(-sL --connect-timeout 10 --max-time 30)
CURL_ARGS+=(-H "Authorization: Token ${FG_TOKEN}")
CURL_ARGS+=(-H "Accept: application/json")

if [ "$METHOD" != "GET" ]; then
  CURL_ARGS+=(-X "$METHOD")
  if [ -n "$DATA" ]; then
    CURL_ARGS+=(-H "Content-Type: application/json")
    CURL_ARGS+=(-d "$DATA")
  fi
fi

HTTP_CODE=$(mktemp)
RESPONSE=$(curl "${CURL_ARGS[@]}" -w "%{http_code}" -o "$HTTP_CODE" "$URL")
BODY=$(cat "$HTTP_CODE")
rm -f "$HTTP_CODE"

if echo "$BODY" | python3 -m json.tool > /dev/null 2>&1; then
  echo "$BODY" | python3 -m json.tool
else
  echo "$BODY"
fi

if [ "$RESPONSE" -lt 200 ] || [ "$RESPONSE" -ge 300 ]; then
  exit 1
fi