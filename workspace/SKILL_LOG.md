# SKILL_LOG.md

> Bitácora de skills creadas, conversaciones que las originaron, decisiones técnicas y lecciones aprendidas.

---

## 2026-06-26: `4geeks` — Integración API BreatheCode / 4Geeks Academy

### Origen
El usuario quería que pudiera conectarme a su cuenta de 4Geeks usando su token de estudiante, sin que él tuviera que escribir código. El token ya existía en `/.openclaw/.env` y me pidió explorar qué hacer.

### Decisión técnica
1. **Composio** no tiene integración con 4Geeks → descartado.
2. Busqué la URL del API real en el bundle JS de la SPA de `breatheco.de` y `4geeksacademy.com`.
3. Encontré `runtimeConfig.BREATHECODE_HOST: "https://breathecode.herokuapp.com"` en el SSG de Next.js, clave para descubrir el backend.
4. Scaneé endpoints vía curl hasta dar con `v1/auth/user/me` (200), que devolvió el perfil del usuario.
5. Creé un **script wrapper bash** (`scripts/4geeks_api.sh`) que:
   - Lee el token del `.env`
   - Construye la URL contra `https://breathecode.herokuapp.com/v1/`
   - Formatea respuesta JSON con `python3 -m json.tool`
   - Soporta GET/POST/PUT/PATCH/DELETE
6. Documenté la skill en `SKILL.md` con endpoints verificados y modo de uso.

### Endpoints descubiertos
| Endpoint | Status | Descripción |
|---|---|---|
| `auth/user/me` | 200 | Perfil completo + roles + academias + permisos |
| `auth/user/<id>` | 200 | Info pública de usuario |
| `certificate/me` | 200 | Certificados emitidos |
| `auth/token/validate` | 403 | Validación de token (requiere permisos admin) |

### Lecciones aprendidas
- El nombre `4GEEKS_TOKEN` no es válido como variable bash (empieza con número) → usé `FG_TOKEN` internamente en el script.
- La API de BreatheCode está hosteada en Heroku y usa middleware New Relic.
- El Swagger/OpenAPI del backend está roto (500), así que el descubrimiento de endpoints fue por fuerza bruta desde los JS bundles del frontend.
- `4geeksacademy.com` y `breatheco.de` son SPAs en Express/Next.js que redirigen todas las rutas al HTML — solo `breathecode.herokuapp.com` devuelve JSON real.
- 4geeksacademy.com tiene un API interno (`/api/content-types`, `/api/settings/tracking`) pero es para el CMS de Prismic, no para datos de estudiante.

### Archivos creados
- `skills/4geeks/SKILL.md`
- `skills/4geeks/scripts/4geeks_api.sh`
- `memory/2026-06-26-4geeks.md`

---

## 2026-06-26: `4geeks_projects` — Listado de proyectos con estado

### Origen
El usuario quería recuperar su lista de proyectos de 4Geeks con estado (pendiente, entregado, calificado) para trackear su progreso automáticamente.

### Proceso de discovery

1. **Partida:** Solo se conocían `auth/user/me`, `auth/role`, `certificate/me` de la sesión anterior.
2. **Búsqueda sin documentación:** No hay docs públicos de la API de BreatheCode. Se exploraron ~50 endpoints por fuerza bruta.
3. **Callejones sin salida:**
   - `assignment`, `assignments`, `project`, `projects`, `task`, `tasks` → 404
   - `learnpack/*`, `deliverable/*`, `delivery/*`, `student/*` → 404
   - `admissions/cohort/*`, `admissions/cohortuser/*` → 404
4. **Pista clave:** `assignment/task` devolvió **503** (no 404) — el endpoint existe pero algo falla.
5. **Solución:** `GET /v1/assignment/task?user=21146` → **200 OK** con 205 tasks.
6. **Bonus:** `admissions/user/me` da perfil completo + cohorts + progreso detallado por proyecto.

### Endpoints descubiertos

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `admissions/user/me` | GET | Perfil usuario + cohorts + progreso projects (más detallado que `auth/user/me`) |
| `admissions/academy/{id}` | GET | Info de la academia |
| `admissions/academy/{id}/syllabus` | GET | Syllabi disponibles |
| `assignment/task?user={id}` | GET | **Todos los assignments** (ejercicios, lecciones, proyectos, quizzes) |

### Estructura del response (`assignment/task`)

```json
{
  "id": int,
  "title": string,
  "task_status": "PENDING" | "DONE",
  "task_type": "PROJECT" | "EXERCISE" | "LESSON" | "QUIZ",
  "revision_status": "PENDING" | "APPROVED",
  "associated_slug": string,
  "delivered_at": datetime | null,
  "reviewed_at": datetime | null,
  "github_url": string | null,
  "live_url": string | null,
  "cohort": { "id": int, "name": string, "slug": string },
  "user": { "id": int, "first_name": string, "last_name": string }
}
```

### Skill creada

- **Script:** `scripts/4geeks_projects.sh`
- **Pipeline:** `curl | python3` directo para evitar problemas con respuestas grandes (~3MB)
- **Filtros:** `--cohort slug|name`, `--status pending|delivered|graded`, `--json`
- **Clasificación de estados:**
  - `⏳ Pendiente`: `task_status == PENDING` y no entregado
  - `📤 Entregado`: `delivered_at` presente o `task_status == DONE`
  - `✅ Calificado`: `revision_status == APPROVED`
- **Mapeo bilingüe:** Acepta `pending|pendiente`, `delivered|entregado`, `graded|calificado|approved`

### Lecciones aprendidas

- La API usa nombres en **singular** para rutas: `assignment/task`, no `assignments/tasks`.
- Algunos endpoints devuelven **503** (no 404) indicando que existen pero requieren permisos distintos (ej. `activity/me` requiere `Academy` header y permiso `read_activity`).
- `admissions/user/me` incluye datos de progreso **más detallados** que `auth/user/me` — incluye `completion.required.missing` con los slugs pendientes.
- La respuesta es enorme (~3MB, 205 items). El script anterior asumía que cabía en variable bash y la pasaba como heredoc → fallaba. **Solución:** pipeline directo `curl | python3`.
- `set -e` en bash + pipe hacia Python puede matar el script si la salida no es parseable. Mejor validar en Python directamente.

### Archivos creados/modificados
- `skills/4geeks/scripts/4geeks_projects.sh` **(nuevo)**
- `skills/4geeks/SKILL.md` **(actualizado)** — sección Projects añadida
- `skills/4geeks/skill_log.md` **(nuevo)** — documento interno de la skill

---

## 2026-06-26: `4geeks_pending` — Trabajo pendiente completo

### Origen
El usuario pidió una skill que le dijera específicamente qué trabajos, lecciones, ejercicios le faltan completar — no solo proyectos, sino todo el contenido pendiente.

### Proceso

1. **Partida:** Ya teníamos `assignment/task?user={id}` (todos los tasks) y `admissions/user/me` (progreso por cohort).
2. **Estrategia:** Cruzar ambos datasets: tasks pendientes de la API + proyectos `missing` de la completitud del perfil.
3. **Complejidad:** La respuesta de tasks incluye **todo** (ejercicios, lecciones, quizzes, proyectos). Había que filtrar items no completados (`revision_status != APPROVED`, sin `delivered_at`, `task_status != DONE`).
4. **Problema con heredoc bash:** El primer intento intentó inyectar JSON gigante en un heredoc Python → explota por los `${}` interpretados por bash.

### Decisiones técnicas

1. **Separar lógica:** `4geeks_pending.sh` (bash) solo obtiene datos y los pipea a `4geeks_pending.py` (Python puro).
2. **Marcadores en stdin:** El shell emite `---USER---` y `---TASKS---` como separadores, Python parsea el flujo.
3. **Variables vía env:** `COHORT_FILTER`, `TYPE_FILTER`, `OUTPUT_JSON` se pasan como variables de entorno, no como expansión inline.
4. **Doble fuente de verdad:**
   - Tasks de la API para detectar lo pendiente por estado
   - `pending_required_slugs` del perfil para capturar proyectos que la plataforma espera pero no tienen task creada
5. **Deduplicación:** Un slug puede aparecer en múltiples cohorts → se marca como `seen_slugs` para evitar duplicados.
6. **Bug detectado y corregido:** Proyectos ya entregados aparecían como "solo slug" porque el perfil los lista como `missing` incluso cuando ya tienen task entregada. Solución: rastrear `completed_slugs` aparte y excluirlos del barrido de `pending_required_slugs`.

### Endpoints usados

| Endpoint | Propósito |
|----------|-----------|
| `admissions/user/me` | User ID + cohorts + progreso + `pending_required_slugs` |
| `assignment/task?user={id}` | Todos los assignments con estado |

### Lecciones aprendidas

- **Nunca** meter JSON grande en heredoc de bash → usar pipeline + script Python separado.
- `admissions/user/me` tiene datos de completitud que `assignment/task` no cubre (proyectos mandatory que ni siquiera tienen task creada todavía).
- El campo `pending_required_slugs` del perfil es la fuente más autoritativa para proyectos mandatory pendientes.
- Algunos proyectos aparecen como `missing` incluso cuando ya tienen un task entregado (inconsistencia de la API). Siempre cruzar ambas fuentes.

### Archivos creados
- `skills/4geeks-pending/SKILL.md` **(nuevo)**
- `skills/4geeks-pending/scripts/4geeks_pending.sh` **(nuevo)**
- `skills/4geeks-pending/scripts/4geeks_pending.py` **(nuevo)**

---

## 2026-06-26: `4geeks_progress` — Resumen de progreso

### Origen
El usuario pidió una skill que le diera una visión general de cuánto ha avanzado en el curso — no solo pendientes, sino el panorama completo.

### Proceso

1. **Partida:** Teníamos `assignment/task` con 205 tasks y `admissions/user/me` con datos de completitud por cohort.
2. **Estrategia:** Agregar por cohort y tipo de task (PROJECT/EXERCISE/LESSON) para mostrar aprobados vs total.
3. **Descubrimiento clave:** El perfil (`admissions/user/me`) tiene un campo `completion` por cohort con:
   - `strategy.type`: `LEGACY_PROJECTS` (solo proyectos cuentan) o `NO_COMPLETION_STRATEGY`
   - `overall`: total/completed/percent
   - `required`: desglose por tipo (PROJECT, etc.) con total, completed, percent, is_met
   - `is_complete`: booleano
   - Cohorts con `educational_status: GRADUATED` y `is_complete: True`
4. **Datos de la API:**
   - 205 tasks totales (139 EXERCISE, 38 PROJECT, 28 LESSON)
   - 31 aprobados, 89 entregados (sin calificar), 85 pendientes
   - 7 cohorts completados, 11 activos

### Decisiones técnicas

1. **Pipeline idéntico a pending:** `bash → python3` con marcadores `---USER---` / `---TASKS---` en stdin.
2. **Doble fuente de datos:**
   - Tasks de la API para desglose exacto por tipo
   - Perfil `completion` para overall % y status GRADUATED/ACTIVE
3. **Orden de cohorts:** Graduados primeros (con ✅), luego activos (con 🟢), alfabético dentro de cada grupo.
4. **Filtro `--cohort`:** Recalcula los totales globales (gt y bt) filtrando solo los cohorts seleccionados.
5. **Columna de %:** Usa `overall_pct` del perfil cuando está disponible (más preciso que calcular de tasks, porque el perfil sabe qué projects son mandatory).

### Endpoints usados

| Endpoint | Propósito |
|----------|-----------|
| `admissions/user/me` | Datos de completitud + status por cohort |
| `assignment/task?user={id}` | Desglose detallado por tipo y estado |

### Lecciones aprendidas

- El `completion.overall.percent` del perfil solo refleja **proyectos mandatory** (por la strategy `LEGACY_PROJECTS`). Para el % real hay que calcular de tasks.
- Cohorts con `NO_COMPLETION_STRATEGY` no tienen datos de progreso (ej. "Authentication in web applications").
- Algunos cohorts no tienen tasks asociados en `assignment/task` (ej. "Application telemetry"). En ese caso aparecen sin datos.
- La plataforma tiene 7 cohorts GRADUATED ✅ y 11 ACTIVE 🟢 para este usuario.

### Archivos creados
- `skills/4geeks-progress/SKILL.md` **(nuevo)**
- `skills/4geeks-progress/scripts/4geeks_progress.sh` **(nuevo)**
- `skills/4geeks-progress/scripts/4geeks_progress.py` **(nuevo)**
