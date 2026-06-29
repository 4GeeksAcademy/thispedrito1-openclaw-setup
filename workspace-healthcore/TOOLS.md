# Herramientas del Workspace de Onboarding — HealthCore Digital

## send_welcome_email
- **Descripción:** Envía de forma autónoma un correo electrónico oficial de bienvenida de HealthCore a la nueva incorporación desde el servidor.
- **Argumentos:**
  - `to`: Dirección de correo electrónico del empleado (ej. `nombre@healthcore.com`).
  - `subject`: Asunto del correo institucional.
  - `body`: Cuerpo del mensaje. Debe incluir obligatoriamente la instrucción explícita para que el nuevo empleado busque e inicie conversación con el bot en Telegram.

## validate_pairing_code
- **Descripción:** Ejecuta el script de seguridad `skills/approve_pairing.py` en el servidor local del workspace para comprobar el código de un solo uso provisto por RRHH. Si el código coincide, el script aprueba automáticamente el emparejamiento (pairing) de Telegram pendiente y actualiza el estado del empleado a activo en `onboarding-database.json`.
- **Argumentos:**
  - `employee_id`: ID único asignado al empleado (Formato: `HC-2026-XXXX`).
  - `verification_code`: El código de seguridad entregado por RRHH que se va a validar contra el registro de la base de datos aislada.