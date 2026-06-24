# TOOLS - Integraciones y Herramientas (Composio / MCPs)

Este documento define las herramientas disponibles para el agente y sus reglas de uso generales. El contexto específico (tecnológico, administrativo, personal) será dictado por el usuario en cada instrucción.

## 1. Gmail (Comunicaciones)
* **Cuándo usar:** Gestión de correos electrónicos para cualquier ámbito (desarrollo, operativas, comunicaciones personales).
* **Regla inamovible:** SIEMPRE crear correos como borradores (`drafts`). Nunca enviar correos directamente sin la confirmación explícita del usuario.
* **Firma por defecto:** A menos que se especifique otro rol en el prompt, utilizar una firma neutral:
  ```text
  Pedro Luis Sánchez Pacheco
  A Coruña, España
  ```

## 2. Google Calendar (Agenda y Bloques de Tiempo)
* **Cuándo usar:** Planificación de la semana, agendamiento de reuniones, creación de bloques de trabajo o recordatorios.
* **Valores por defecto:**
  * **Zona Horaria:** Europa/Madrid (CEST/CET).
  * **Bloques prioritarios:** Esquivar y respetar incondicionalmente la rutina de hipertrofia (5 días a la semana) y los bloques dedicados al tiempo familiar.
  * **Alertas:** Notificación estándar 10 minutos antes, salvo que se especifique lo contrario.

## 3. Google Drive & Docs (Gestión Documental)
* **Cuándo usar:** Creación, lectura, edición y organización de documentos de texto, especificaciones o notas.
* **Comportamiento:** Guardar los archivos en la carpeta específica que el usuario indique en su instrucción. Si no se indica ruta, crear en el directorio raíz o en borradores generales.
* **Estilo:** Limpio, usando jerarquía de títulos y bloques de código monoespaciado si se trata de documentación técnica.

## 4. Google Sheets (Bases de Datos Operativas)
* **Cuándo usar:** Creación o actualización de hojas de cálculo para seguimiento financiero, bases de datos operativas, logs de entrenamiento o control de proyectos.
* **Comportamiento:** Adaptar la estructura de columnas y fórmulas exactamente a los requerimientos del prompt en el momento de la ejecución.

## 5. Navegación y Búsqueda (Search Tools)
* **Cuándo usar:** Búsqueda de información actualizada, lectura de documentación técnica, investigación de mercado o resolución de errores.
* **Comportamiento:** Priorizar siempre la documentación oficial y fuentes primarias. Extraer la información o los comandos precisos sin generar resúmenes genéricos o paja.