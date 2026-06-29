# Estrategia de Memoria y Resolución de Amnesia de Contexto — HealthCore Digital

## 1. Justificación del Tipo de Memoria Seleccionado

Para el flujo de incorporación de HealthCore, se ha optado por un enfoque híbrido optimizado utilizando la carpeta `/memory` combinada con el archivo persistente estructurado `onboarding-database.json` dentro del workspace:

- **`Memory.md` / `IDENTITY.md`:** Se utiliza exclusivamente para albergar instrucciones permanentes, reglas del sistema y restricciones legales estáticas (como los marcos HIPAA y UK GDPR bajo la supervisión de Claire Whitfield).
- **Carpeta `/memory` y `onboarding-database.json`:** Se eligen para el almacenamiento cronológico y de estado de los empleados. Un proceso de onboarding es un flujo de estados dinámico (`not started` -> `active` -> `completed`). Almacenar cada transición, entregable recibido y log de eventos de manera estructurada en archivos locales garantiza que los datos sobrevivan a cualquier ciclo de vida de la sesión de chat.

Esta decisión es coherente con el caso de uso sanitario de HealthCore: las ventanas de contexto de los LLM sufren de amnesia tras un reinicio, y Diane Foster no puede depender de que el historial de un chat de Telegram mantenga a salvo datos críticos de licencias médicas.

---

## 2. Resolución de la Amnesia de Contexto

### ¿Qué debe recordar el agente si se reinicia el VPS mañana?

Para garantizar un impacto operativo nulo, se ha mapeado la persistencia de los siguientes datos específicos por empleado:

| Ítem de Dato | Ubicación de Almacenamiento | Método de Recuperación por el Agente |
| :--- | :--- | :--- |
| **Identidad del Empleado** (ID, Nombre, Rol, Sede) | `workspace-healthcore/onboarding-database.json` | Búsqueda exacta por Clave ID / Consulta Semántica QMD |
| **Estado Actual del Proceso** (`not started`, `active`, `completed`) | `workspace-healthcore/onboarding-database.json` | Lectura directa del atributo `status` en el JSON |
| **Entregables Clínicos Pendientes/Recibidos** | `workspace-healthcore/onboarding-database.json` | Mapeo de booleanos en el objeto interno `deliverables` |
| **Código de Verificación Emitido** | `workspace-healthcore/onboarding-database.json` | Comparación lógica interna durante la llamada a la herramienta |
| **Contador de Cambios de Estado** (para el resumen diario) | `workspace-healthcore/onboarding-database.json` | Atributo numérico incremental `state_changes_since_last_summary` |

---

## 3. Configuración y Evidencia de Consulta QMD

QMD se encuentra activo con búsqueda por palabras clave, similitud semántica y re-ranking habilitados. Esto soluciona problemas de consultas aproximadas por parte del equipo de RRHH.

### Consulta de Prueba Documentada

**Query ejecutada por Diane Foster:**
> *"¿Qué empleados de Texas están activos pero tienen pendientes sus papeles de privacidad?"*

**Resultado de Recuperación Semántica QMD (Payload de coincidencia más alta):**
```json
{
  "employee_id": "HC-2026-0042",
  "name": "Alex Rivera",
  "position": "Asistente de Dirección",
  "location": "Sede de Austin",
  "legal_region": "US (HIPAA)",
  "status": "active",
  "deliverables": {
    "medical_license": { "received": true, "date": "2026-06-29T21:15:00Z" },
    "privacy_form_hipaa": { "received": false, "date": null },
    "operations_manual": { "received": true, "date": "2026-06-29T21:20:00Z" }
  },
  "score_qmd_rerank": 0.945
}