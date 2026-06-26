# 4Geeks Progress Skill

Resumen de progreso general en 4Geeks Academy: proyectos, ejercicios y lecciones completados vs pendientes, desglosado por cohort.

## Configuración

Requiere `4GEEKS_TOKEN` en `/root/.openclaw/.env`.

## Script

**Ruta:** `scripts/4geeks_progress.sh` (bash) → `scripts/4geeks_progress.py` (procesador Python)

Cruza dos fuentes de datos:
- **`admissions/user/me`** — datos de completitud por cohort del perfil
- **`assignment/task?user={id}`** — todos los tasks con su estado

Muestra:
- **Grand total**: assignments aprobados, entregados y pendientes
- **Por tipo**: desglose PROJECT / EXERCISE / LESSON
- **Por cohort**: tabla con proyectos, ejercicios y lecciones completados + % de progreso

## Uso

```bash
./4geeks_progress.sh [--cohort "nombre o slug"] [--json]
```

### Opciones

- `--cohort` — filtra a un cohort específico (total se recalcula sobre el cohort filtrado)
- `--json` — salida JSON estructurada

### Ejemplos

```bash
# Progreso general
./4geeks_progress.sh

# Progreso de un cohort específico
./4geeks_progress.sh --cohort "spain-aie-pt-1"

# Salida JSON
./4geeks_progress.sh --json | jq '.grand_total'
```

## Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `FG_TOKEN` | — | Token API (sobrescribe `.env`) |
| `FOURGEEKS_API_URL` | `https://breathecode.herokuapp.com/v1` | URL base |