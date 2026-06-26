# 4Geeks Projects Skill

Recupera la lista de proyectos asignados en 4Geeks Academy con su estado actual.

## Configuración

Requiere `4GEEKS_TOKEN` en `/root/.openclaw/.env`.

## Script

**Ruta:** `scripts/4geeks_projects.sh`

**Endpoint:** `GET /v1/assignment/task?user={user_id}`

Filtra solo `task_type == "PROJECT"` y clasifica:

| Estado | Criterio |
|--------|----------|
| ⏳ Pendiente | `task_status == "PENDING"` y no entregado |
| 📤 Entregado | `delivered_at` presente o `task_status == "DONE"` |
| ✅ Calificado | `revision_status == "APPROVED"` |

## Uso

```bash
./4geeks_projects.sh [--cohort "nombre"] [--status pending|delivered|graded] [--json]
```

### Ejemplos

```bash
# Todos los proyectos
./4geeks_projects.sh

# Solo pendientes del cohort principal
./4geeks_projects.sh --status pending --cohort spain-aie-pt-1

# Calificados en JSON
./4geeks_projects.sh --status graded --json

# Proyectos de un cohort específico
./4geeks_projects.sh --cohort "Working with AI"
```

## Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `FG_TOKEN` | — | Token API (sobrescribe `.env`) |
| `FOURGEEKS_API_URL` | `https://breathecode.herokuapp.com/v1` | URL base |