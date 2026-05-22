Para garantizar que el agente ejecute el flujo de trabajo de forma óptima, se tomaron las siguientes decisiones de diseño en el prompt:

1. **Estructura Secuencial:** Se dividió el flujo en 4 pasos estrictos (Chain of Thought) para guiar al LLM paso a paso y evitar que omita acciones intermedias.
2. **Especificación de Herramientas:** Se nombró explícitamente la skill `mcporter` de Composio para acotar el kit de herramientas y reducir errores de selección de API.
3. **Pausa de Validación (Guardrail):** El paso 1 fuerza al agente a evaluar si tiene contexto suficiente antes de actuar, mitigando la creación de documentos incompletos.
