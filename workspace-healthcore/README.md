# HealthCore Onboarding Agent — Workspace de Incorporación Persistente

Este proyecto implementa un agente de onboarding aislado en OpenClaw para la red de clínicas de HealthCore, capaz de persistir de forma real el estado de los empleados a lo largo del tiempo, evadiendo la amnesia de contexto.

## 🔐 Nota de Seguridad sobre Aprobación de Pairings
Por defecto, OpenClaw requiere aprobación manual de cada dispositivo para prevenir accesos no autorizados[cite: 1, 2]. En un entorno de alto volumen como el onboarding de HealthCore, la aprobación manual de hilos de Telegram desconocidos genera fatiga de alertas y riesgos de ingeniería social (aprobar por error a un atacante exterior). 

Este proyecto implementa un skill con un script del lado del servidor (`skills/approve_pairing.py`) que automatiza el proceso mediante un enfoque *gated*: solo se aprueba la conexión si el canal de comunicación es validado por una clave de un solo uso de la que únicamente disponen el empleado (recibida vía email seguro) y RRHH (quien la introduce en el bot)[cite: 1, 2]. Al correr en el servidor local y omitir la ventana del chat directo con el usuario externo, se reduce la superficie de ataque y se mantiene la conformidad con HIPAA/GDPR al auditar de manera estricta quién aprobó a quién y cuándo en los registros locales.

## 🛠️ Instrucciones de Uso y Prueba del Flujo Completo

1. **Paso 1 (Notificación de RRHH):** Diane Foster notifica los datos de un nuevo empleado seleccionado a través de Telegram. El bot crea el registro en `onboarding-database.json` con estado `not started` y genera un código único de formato `HC-XXXX`.
2. **Paso 2 (Email Autónomo):** El agente manda un correo de bienvenida a la persona con la instrucción de contactar al bot en Telegram.
3. **Paso 3-4 (Contacto de la Persona):** El empleado escribe al bot, y este le instruye que entregue su código a RRHH por seguridad.
4. **Paso 5-6 (Validación de Pairing):** RRHH introduce el código en el bot, el cual dispara el comando interno `python skills/approve_pairing.py <ID> <CÓDIGO>`. Si coincide, se realiza la aprobación del pairing de Telegram (`openclaw pairing approve telegram <CODE>`) y se escribe la transacción en `logs/pairing_audit.log`.
5. **Paso 7 (Instrucciones):** El agente saluda al empleado por su canal de Telegram ahora verificado y le despliega los 3 entregables requeridos según su región de cumplimiento (HIPAA para EE.UU. o UK GDPR para el Reino Unido).
6. **Resumen Matutino:** El agente ejecuta de forma diaria una tarea que lee el JSON, clasifica los procesos en (No iniciados, Activos, Terminados) y reporta el contador de cambios netos a RRHH.

## 🧪 Verificación de la Amnesia de Contexto (Prueba de Reinicio)
Para verificar que el estado es recuperable e independiente de la sesión activa:
1. Inicie un proceso de onboarding y colóquelo en estado `active`.
2. Reinicie el servicio de OpenClaw en la terminal del VPS.
3. Envíe un mensaje de seguimiento; el motor de búsqueda **QMD** hidratará el contexto semántico de inmediato desde el archivo de persistencia física local, permitiendo continuar el flujo sin pérdidas.