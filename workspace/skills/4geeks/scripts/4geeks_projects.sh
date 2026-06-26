#!/bin/bash
# 4Geeks Projects Skill - Lista proyectos del alumno con su estado
# Uso: ./4geeks_projects.sh [--cohort slug|id] [--status pending|delivered|graded] [--json]

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
STATUS_FILTER=""
OUTPUT_JSON=0

while [ $# -gt 0 ]; do
  case "$1" in
    --cohort) COHORT_FILTER="$2"; shift 2 ;;
    --status) STATUS_FILTER="$2"; shift 2 ;;
    --json) OUTPUT_JSON=1; shift ;;
    *) echo "Usage: $0 [--cohort slug|name] [--status pending|delivered|graded] [--json]" >&2; exit 1 ;;
  esac
done

# Obtener user ID
USER_ID=$(curl -sL --connect-timeout 10 --max-time 30 \
  -H "Authorization: Token ${FG_TOKEN}" \
  -H "Accept: application/json" \
  "${BASE_URL}/admissions/user/me" | python3 -c "import json,sys; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)

if [ -z "$USER_ID" ]; then
  echo '{"error":"Failed to get user ID"}' >&2
  exit 1
fi

# Obtener tasks y procesar en pipeline
curl -sL --connect-timeout 10 --max-time 30 \
  -H "Authorization: Token ${FG_TOKEN}" \
  -H "Accept: application/json" \
  "${BASE_URL}/assignment/task?user=${USER_ID}" | python3 -c "
import json, sys

data = json.load(sys.stdin)

# Filtrar solo PROJECTS
projects = [t for t in data if t.get('task_type') == 'PROJECT']

cohort_filter = '${COHORT_FILTER}'.lower()
status_filter = '${STATUS_FILTER}'.lower()
output_json = ${OUTPUT_JSON}

if cohort_filter:
    projects = [
        p for p in projects
        if cohort_filter in p.get('cohort',{}).get('name','').lower()
        or cohort_filter in p.get('cohort',{}).get('slug','').lower()
    ]

# Clasificar estado
for p in projects:
    task_status = p.get('task_status', 'PENDING')
    rev_status = p.get('revision_status', 'PENDING')
    delivered = p.get('delivered_at') is not None

    if task_status == 'PENDING' and not delivered:
        p['_status'] = 'pendiente'
        p['_status_emoji'] = '⏳'
    elif rev_status == 'APPROVED':
        p['_status'] = 'calificado'
        p['_status_emoji'] = '✅'
    elif delivered or task_status == 'DONE':
        p['_status'] = 'entregado'
        p['_status_emoji'] = '📤'
    else:
        p['_status'] = 'pendiente'
        p['_status_emoji'] = '⏳'

# Mapear filtro de estado (inglés/español)
if status_filter:
    status_map = {
        'pending': 'pendiente', 'pendiente': 'pendiente',
        'delivered': 'entregado', 'entregado': 'entregado', 'done': 'entregado',
        'graded': 'calificado', 'calificado': 'calificado', 'approved': 'calificado',
    }
    filter_val = status_map.get(status_filter, status_filter)
    projects = [p for p in projects if p['_status'] == filter_val]

if output_json:
    print(json.dumps(projects, indent=2, default=str))
    sys.exit(0)

# Salida formateada
print(f'Proyectos asignados: {len(projects)}\n')
for p in projects:
    emoji = p['_status_emoji']
    cohort_name = p.get('cohort',{}).get('name','?')
    title = p.get('title','?')
    rev = p.get('revision_status','?')
    slug = p.get('associated_slug','')

    print(f'  {emoji} {title}')
    print(f'     Cohort: {cohort_name}')
    print(f'     Revision: {rev} | Slug: {slug}')

    if p.get('github_url'):
        print(f'     GitHub: {p[\"github_url\"]}')
    if p.get('live_url'):
        print(f'     Live: {p[\"live_url\"]}')
    print()
" 2>&1