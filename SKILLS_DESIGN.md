# SKILLS DESIGN - Diseño de Habilidades del Agente

Este documento define el diseño de tres habilidades (skills) personalizadas para el ecosistema de herramientas y rutinas del usuario. Cada diseño responde a tres preguntas clave: 
1. ¿Qué problema resuelve y por qué es útil?
2. ¿Cómo se activa y qué datos recibe?
3. ¿Qué herramientas utiliza y cuál es el resultado final?

---

## Skill 1: Planificador de Vida Híbrida (Calendar Automation)

**1. ¿Qué problema resuelve y por qué es útil?**
Equilibrar el desarrollo de software, los estudios de ingeniería en IA y la gestión de propiedades inmobiliarias es complejo. Esta skill automatiza la planificación semanal, garantizando matemáticamente que se respeten los 5 días de entrenamiento  y el tiempo familiar, acomodando el resto de las tareas alrededor de estos inamovibles.

**2. ¿Cómo se activa y qué datos recibe?**
* **Trigger:** Comando manual en lenguaje natural (ej. *"Planifica mi semana. Tengo que entregar el módulo de reservas de Clinica Nova, repasar arquitecturas de agentes y hacer visitas a dos pisos"*).
* **Inputs:** Lista de objetivos crudos o tareas pendientes de la semana.

**3. ¿Qué herramientas utiliza y cuál es el resultado final?**
* **Herramientas:** Google Calendar (MCP) + Google Docs (MCP).
* **Resultado:** 
  1. Crea un documento estructurado en Drive con la priorización semanal de tareas.
  2. Genera los bloques de tiempo directamente en Calendar, ubicando el código y la gestión en los huecos disponibles y bloqueando los horarios de entrenamiento y compromisos personales en A Coruña.

---

## Skill 2: Triaje Inmobiliario Automatizado (Inbox to Sheets & Drafts)

**1. ¿Qué problema resuelve y por qué es útil?**
La gestión de incidencias y comunicaciones con inquilinos consume energía que podría destinarse a programar en React/Next.js. Esta skill asume el rol de administrador de primera línea, procesando solicitudes de mantenimiento o dudas administrativas sin intervención directa inicial.

**2. ¿Cómo se activa y qué datos recibe?**
* **Trigger:** Automático mediante *Heartbeat* (cada X horas) o comando manual (*"Haz el triaje de la inmobiliaria"*).
* **Inputs:** Lectura de correos no leídos bajo etiquetas específicas o recibidos de direcciones de inquilinos conocidos.

**3. ¿Qué herramientas utiliza y cuál es el resultado final?**
* **Herramientas:** Gmail (MCP) + Google Sheets (MCP).
* **Resultado:**
  1. Lee y clasifica el correo.
  2. Genera un borrador de respuesta directa y profesional en Gmail (respetando la regla de "nunca enviar").
  3. Registra la incidencia o petición en la hoja de cálculo operativa (`Master_Inmobiliaria`) con su fecha y estado en "Pendiente de revisión".

---

## Skill 3: Diario de Arquitectura de Software y Aprendizaje (Dev Log)

**1. ¿Qué problema resuelve y por qué es útil?**
Durante el desarrollo de soluciones IA o el estudio de ingeniería, se descubren soluciones rápidas, integraciones útiles o correcciones de bugs complejos en TypeScript que suelen perderse. Esta skill actúa como un "segundo cerebro" técnico, consolidando el conocimiento en un formato limpio.

**2. ¿Cómo se activa y qué datos recibe?**
* **Trigger:** Comando rápido y conversacional (*"Anota esto en el dev log: el estado de las reservas con el calendario daba fallo por re-renderizados, lo solucioné usando un hook personalizado con useCallback"*).
* **Inputs:** Fragmentos de código en bruto, conceptos abstractos aprendidos en la universidad o soluciones a bugs.

**3. ¿Qué herramientas utiliza y cuál es el resultado final?**
* **Herramientas:** Google Docs (MCP) o archivo local Markdown.
* **Resultado:**
  1. Abre el documento maestro de conocimientos técnicos.
  2. Formatea la entrada de manera profesional (añadiendo fecha, etiquetas como `[Next.js]`, `[Arquitectura]`, y bloques de código tipados).
  3. Guarda el documento, permitiendo tener una base de datos propia de soluciones para futuros proyectos como Aurora Plants.