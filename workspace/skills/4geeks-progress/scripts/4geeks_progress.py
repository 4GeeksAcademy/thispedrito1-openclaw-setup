#!/usr/bin/env python3
"""4Geeks Progress - Resumen de progreso desde stdin (two-part JSON)."""
import json, sys, os
from collections import defaultdict

raw = sys.stdin.read()
parts = raw.split('---TASKS---')
user_part = parts[0].split('---USER---')[1].strip()
tasks_part = parts[1].strip()

user = json.loads(user_part)
tasks = json.loads(tasks_part)

cohort_filter = os.environ.get('COHORT_FILTER', '').lower()
output_json = os.environ.get('OUTPUT_JSON', '0') == '1'

# --- Datos de completitud por cohort desde el perfil ---
comp_info = {}
for entry in user.get('cohorts', []):
    c = entry.get('cohort', {})
    cid = c.get('id')
    comp_info[cid] = {
        'name': c.get('name', '?'),
        'slug': c.get('slug', ''),
        'status': entry.get('educational_status', '?'),
        'role': entry.get('role', ''),
        'strategy': entry.get('completion', {}).get('strategy', {}),
        'is_complete': entry.get('completion', {}).get('is_complete', False),
        'overall_pct': (entry.get('completion', {}).get('overall', {}) or {}).get('percent', 0),
        'required': entry.get('completion', {}).get('required', {}),
    }

# Crear lookup name -> status
name_to_status = {}
name_to_slug = {}
name_to_overall = {}
name_to_required = {}
for v in comp_info.values():
    name_to_status[v['name']] = v['status']
    name_to_slug[v['name']] = v['slug']
    name_to_overall[v['name']] = v['overall_pct']
    name_to_required[v['name']] = v['required']

# --- Agregar tasks por cohort y tipo ---
tc = defaultdict(lambda: defaultdict(lambda: {'total':0, 'approved':0, 'delivered':0, 'pending':0}))
gt = {'total':0, 'approved':0, 'delivered':0, 'pending':0}
bt = defaultdict(lambda: {'total':0, 'approved':0, 'delivered':0, 'pending':0})

for t in tasks:
    cohort = t.get('cohort', {}) or {}
    cname = cohort.get('name', '?')
    tt = t.get('task_type', '?')
    rs = t.get('revision_status', '')
    ts = t.get('task_status', '')
    dl = t.get('delivered_at')

    tc[cname][tt]['total'] += 1
    bt[tt]['total'] += 1
    gt['total'] += 1

    if rs == 'APPROVED':
        tc[cname][tt]['approved'] += 1
        bt[tt]['approved'] += 1
        gt['approved'] += 1
    elif dl or ts == 'DONE':
        tc[cname][tt]['delivered'] += 1
        bt[tt]['delivered'] += 1
        gt['delivered'] += 1
    else:
        tc[cname][tt]['pending'] += 1
        bt[tt]['pending'] += 1
        gt['pending'] += 1

# Colleccionar nombres de cohorts (de tasks + perfil)
all_names = set(tc.keys()) | set(name_to_status.keys())

if cohort_filter:
    all_names = {n for n in all_names if cohort_filter in n.lower()}

# Orden: GRADUATED al final, luego por nombre
def sort_key(n):
    s = name_to_status.get(n, 'ACTIVE')
    return (0 if s == 'GRADUATED' else 1, n.lower())

sorted_names = sorted(all_names, key=sort_key)

# --- Recalcular grand totals si hay filtro ---
if cohort_filter:
    gt = {'total':0, 'approved':0, 'delivered':0, 'pending':0}
    bt = defaultdict(lambda: {'total':0, 'approved':0, 'delivered':0, 'pending':0})
    for cname in all_names:
        cohort_tasks = tc.get(cname, {})
        for tt, d in cohort_tasks.items():
            for k in gt:
                gt[k] += d[k]
            for k in bt[tt]:
                bt[tt][k] += d[k]

# --- OUTPUT ---
if output_json:
    out = {
        'grand_total': dict(gt),
        'by_type': {k: dict(v) for k, v in bt.items()},
        'cohorts': [],
    }
    for cname in sorted_names:
        cohort_tasks = tc.get(cname, {})
        totals = {'total':0, 'approved':0, 'delivered':0, 'pending':0}
        for td in cohort_tasks.values():
            for k in totals:
                totals[k] += td[k]
        out['cohorts'].append({
            'name': cname,
            'slug': name_to_slug.get(cname, ''),
            'status': name_to_status.get(cname, '?'),
            'overall_pct': name_to_overall.get(cname, 0),
            'totals': totals,
            'by_type': {k: dict(v) for k, v in cohort_tasks.items()},
            'required': name_to_required.get(cname, {}),
        })
    print(json.dumps(out, indent=2, default=str))
    sys.exit(0)

# --- SALIDA FORMATEADA ---
print('=' * 70)
print('  📊  RESUMEN DE PROGRESO — 4Geeks Academy')
print('=' * 70)

pct = round(gt['approved'] / gt['total'] * 100, 1) if gt['total'] > 0 else 0
print(f'\n  📈  Total: {gt["approved"]}/{gt["total"]} aprobados ({pct}%)')
print(f'     📤  Entregados: {gt["delivered"]}  |  ⏳ Pendientes: {gt["pending"]}')
print()

print('  Por tipo:')
for tt in ['PROJECT', 'EXERCISE', 'LESSON', 'QUIZ']:
    if tt in bt:
        d = bt[tt]
        tpct = round(d['approved'] / d['total'] * 100, 1) if d['total'] > 0 else 0
        emoji = {'PROJECT': '📦', 'EXERCISE': '💻', 'LESSON': '📖', 'QUIZ': '❓'}[tt]
        print(f'    {emoji}  {tt:10s}  {d["approved"]:3d}/{d["total"]:<3d} ({tpct:5.1f}%)  '
              f'→ {d["delivered"]} entregados, {d["pending"]} pendientes')
print()

print('  Por cohort:')
header = f'  {"Cohort":42s} {"Status":10s} {"Prj":4s} {"Exc":4s} {"Les":4s} {"%":6s}'
print(header)
print('  ' + '-' * (len(header) - 2))

for cname in sorted_names:
    status = name_to_status.get(cname, '?')
    overall = name_to_overall.get(cname, 0)
    cohort_tasks = tc.get(cname, {})

    # Sum totals across types
    totals = {'total':0, 'approved':0, 'delivered':0, 'pending':0}
    for td in cohort_tasks.values():
        for k in totals:
            totals[k] += td[k]

    prj = cohort_tasks.get('PROJECT', {})
    exc = cohort_tasks.get('EXERCISE', {})
    les = cohort_tasks.get('LESSON', {})
    prj_str = f'{prj.get("approved",0)}/{prj.get("total",0)}' if prj.get('total',0) > 0 else '-'
    exc_str = f'{exc.get("approved",0)}/{exc.get("total",0)}' if exc.get('total',0) > 0 else '-'
    les_str = f'{les.get("approved",0)}/{les.get("total",0)}' if les.get('total',0) > 0 else '-'

    # Overall pct: use profile data if available, else compute from tasks
    total_tasks = totals['total']
    total_app = totals['approved']
    pct_overall = overall if overall > 0 else (round(total_app / total_tasks * 100, 1) if total_tasks > 0 else 0)
    pct_str = f'{pct_overall:.0f}%' if total_tasks > 0 else '-'

    status_display = status
    if status == 'GRADUATED':
        status_display = '✅'
    elif status == 'ACTIVE':
        status_display = '🟢'

    print(f'  {cname[:40]:42s} {status_display:10s} {prj_str:4s} {exc_str:4s} {les_str:4s} {pct_str:6s}')

print()
completed = sum(1 for n in sorted_names if name_to_status.get(n) == 'GRADUATED')
active = sum(1 for n in sorted_names if name_to_status.get(n) == 'ACTIVE')
filter_note = f' (filtrado: {len(sorted_names)} cohorts)' if cohort_filter else ''
print(f'  Resumen: {completed} completados  |  {active} activos{filter_note}  |  {gt["approved"]}/{gt["total"]} aprobados ({pct}%)')