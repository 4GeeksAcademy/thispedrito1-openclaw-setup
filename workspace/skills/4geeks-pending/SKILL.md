# 4Geeks Pending Skill

Recupera todo el trabajo pendiente de 4Geeks Academy: proyectos, ejercicios, lecciones y quizzes que aún no has completado.

## Configuración

Requiere `4GEEKS_TOKEN` en `/root/.openclaw/.env`.

## Script

**Ruta:** `scripts/4geeks_pending.sh` (bash) → `scripts/4geeks_pending.py` (procesador Python)

Cruza dos fuentes de datos:
- **`admissions/user/me`** — datos de completitud por cohort (proyectos mandatory faltantes)
- **`assignment/task?user={id}`** — tasks individuales con su estado

Filtra items con `revision_status == "APPROVED"`, `task_status == "DONE"` o `delivered_at` presente. Incluye proyectos marcados como `missing` en el perfil que aún no tienen task creada.

## Uso

```bash
./4geeks_pending.sh [--cohort "nombre o slug"] [--type project|exercise|lesson|quiz] [--json]
```

### Opciones

- `--cohort` — Filtra por cohort específico
- `--type` — Filtra por tipo: `project`, `exercise`, `lesson`, `quiz` (acepta español)
- `--json` — Salida en JSON

### Ejemplos

```bash
# Todo el trabajo pendiente
./4geeks_pending.sh

# Solo proyectos pendientes del bootcamp principal
./4geeks_pending.sh --type project --cohort spain-aie-pt-1

# Lecciones sin completar
./4geeks_pending.sh --type lesson

# Salida JSON para procesar
./4geeks_pending.sh --json
```

## Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `FG_TOKEN` | — | Token API (sobrescribe `.env`) |
| `FOURGEEKS_API_URL` | `https://breathecode.herokuapp.com/v1` | URL base |