#!/usr/bin/env python3
"""4Geeks Pending - Procesa trabajo pendiente desde stdin (two-part JSON)."""
import json, sys, os
from collections import defaultdict

# Leer entrada: dos bloques separados por marcador
raw = sys.stdin.read()
parts = raw.split('---TASKS---')
user_part = parts[0].split('---USER---')[1].strip()
tasks_part = parts[1].strip()

user = json.loads(user_part)
tasks = json.loads(tasks_part)

# Filtros desde variables de entorno
cohort_filter = os.environ.get('COHORT_FILTER', '').lower()
type_filter = os.environ.get('TYPE_FILTER', '').lower()
output_json = os.environ.get('OUTPUT_JSON', '0') == '1'

# --- Clasificar ---
pending = []
seen_slugs = set()
completed_slugs = set()

for t in tasks:
    slug = t.get('associated_slug', '')
    ttype = t.get('task_type', '?')
    tstatus = t.get('task_status', 'PENDING')
    rstatus = t.get('revision_status', 'PENDING')
    delivered = t.get('delivered_at') is not None
    cohort = t.get('cohort', {}) or {}
    cid = cohort.get('id')

    # Saltar completados/calificados
    if rstatus == 'APPROVED' or delivered or tstatus == 'DONE':
        if slug:
            completed_slugs.add(slug)
        continue

    # Evitar duplicados entre cohorts
    if slug:
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)

    pending.append({
        'title': t.get('title', '?'),
        'slug': slug,
        'type': ttype,
        'cohort_id': cid,
        'cohort_name': cohort.get('name', '?') if cohort else '?',
        'cohort_slug': cohort.get('slug', '') if cohort else '',
        'github_url': t.get('github_url'),
        'live_url': t.get('live_url'),
    })

# --- Proyectos 'missing' de completion que NO aparecen en tasks ---
for entry in user.get('cohorts', []):
    c = entry.get('cohort', {})
    cid = c.get('id')
    completion = entry.get('completion', {})
    pending_slugs = completion.get('pending_required_slugs', {}).get('PROJECT', [])
    for slug in pending_slugs:
        if slug not in seen_slugs and slug not in completed_slugs:
            pending.append({
                'title': slug,
                'slug': slug,
                'type': 'PROJECT',
                'cohort_id': cid,
                'cohort_name': c.get('name', '?'),
                'cohort_slug': c.get('slug', ''),
                'github_url': None,
                'live_url': None,
                '_missing_only': True,
            })
            seen_slugs.add(slug)

# --- Filtros ---
if cohort_filter:
    pending = [
        p for p in pending
        if cohort_filter in p['cohort_name'].lower()
        or cohort_filter in p['cohort_slug'].lower()
    ]

if type_filter:
    type_map = {
        'project': 'PROJECT', 'proyecto': 'PROJECT',
        'exercise': 'EXERCISE', 'ejercicio': 'EXERCISE',
        'lesson': 'LESSON', 'leccion': 'LESSON', 'lección': 'LESSON',
        'quiz': 'QUIZ',
    }
    ftype = type_map.get(type_filter, type_filter.upper())
    pending = [p for p in pending if p['type'] == ftype]

# --- Ordenar ---
type_order = {'PROJECT': 0, 'EXERCISE': 1, 'LESSON': 2, 'QUIZ': 3}
pending.sort(key=lambda p: (p['cohort_name'] or '', type_order.get(p['type'], 99), p['title'] or ''))

# --- Salida ---
if output_json:
    print(json.dumps(pending, indent=2, default=str))
    sys.exit(0)

# Agrupar por cohort
by_cohort = defaultdict(list)
for p in pending:
    by_cohort[p['cohort_name']].append(p)

total = len(pending)
print(f'Trabajo pendiente: {total} items\n')

for cohort_name in sorted(by_cohort.keys()):
    items = by_cohort[cohort_name]
    print(f'  {cohort_name}')
    print(f'  {"-" * len(cohort_name)}')

    by_type = defaultdict(list)
    for item in items:
        by_type[item['type']].append(item)

    for ttype in ['PROJECT', 'EXERCISE', 'LESSON', 'QUIZ']:
        if ttype not in by_type:
            continue

        emoji_map = {'PROJECT': '📦', 'EXERCISE': '💻', 'LESSON': '📖', 'QUIZ': '❓'}
        emoji = emoji_map.get(ttype, '•')
        print(f'\n    {emoji} {ttype}s ({len(by_type[ttype])}):')

        for item in by_type[ttype]:
            title = item['title']
            missing_badge = ' (solo slug)' if item.get('_missing_only') else ''
            print(f'      • {title}{missing_badge}')
            if item['slug']:
                print(f'        Slug: {item["slug"]}')
            if item['github_url']:
                print(f'        GitHub: {item["github_url"]}')

    print()

print(f'Total: {total} items pendientes')