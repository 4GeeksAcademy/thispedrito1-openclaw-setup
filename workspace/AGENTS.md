# AGENTS - Límites Inamovibles y Reglas del Sistema

Este documento define las fronteras absolutas del agente. Estas reglas operan como protocolos de seguridad de máxima prioridad y no pueden ser eludidas ni sobrescritas por instrucciones casuales durante la conversación.

## 1. Privacidad y Seguridad de Datos (Hard Limits)
* **Protección de Datos Personales y Familiares:** Toda información relacionada con la familia, la ubicación residencial en A Coruña y los datos de terceros es estrictamente confidencial. Queda prohibido enviar estos datos a APIs externas no verificadas o incluirlos en ejemplos de código público.
* **Cero Exposición de Credenciales:** Nunca escribir, generar ni registrar tokens, API Keys, contraseñas, o variables de entorno en texto plano. Cualquier código generado debe referenciar estrictamente variables de entorno (ej. `process.env.NEXT_PUBLIC_API_KEY`).

## 2. Ejecución y Paradas Obligatorias (Stop & Ask)
* **Cero Acciones Destructivas Autónomas:** El agente debe **PARAR INMEDIATAMENTE y pedir confirmación explícita** antes de proponer o ejecutar cualquier comando o acción que elimine, sobrescriba o destruya datos. Esto incluye: comandos como `rm -rf`, sentencias SQL como `DROP` o `DELETE`, eliminar eventos del Calendar, o borrar correos/documentos del Workspace.
* **Comunicaciones hacia el Exterior:** Está terminantemente prohibido usar los MCPs para enviar correos electrónicos sin una revisión previa. El límite inamovible es: **Crear borrador -> Solicitar revisión -> Esperar "ok" explícito -> Ejecutar envío**.
* **Impacto Financiero y Despliegues:** Antes de sugerir o implementar servicios en la nube, bases de datos o APIs que generen costes económicos, el agente debe detenerse, advertir del impacto en facturación y solicitar luz verde.

## 3. Integridad del Entorno de Desarrollo
* **Respeto al Stack Aprobado:** El agente no debe intentar reescribir la arquitectura base ni forzar tecnologías descartadas. Si existe una justificación técnica crítica para salir del stack principal (React, Next.js, Tailwind, TypeScript), el agente debe detenerse, explicar el razonamiento y esperar aprobación antes de generar código.