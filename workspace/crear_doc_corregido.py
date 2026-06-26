#!/usr/bin/env python3
import json
import subprocess

# Leer contenido
with open('/root/.openclaw/workspace/documento_ia_agentica.md', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Construir la solicitud CORRECTA para COMPOSIO_MULTI_EXECUTE_TOOL
# Según el error, necesita "tool_slug" no "tool"
request_tools = [
    {
        "tool_slug": "GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN",
        "arguments": {
            "title": "Dominando la IA Agentica",
            "markdown_text": contenido
        }
    }
]

print("Intentando crear documento con tool_slug correcto...")

# Ejecutar mcporter
cmd = [
    "mcporter",
    "--config", "/root/.openclaw/config/mcporter.json",
    "call",
    "composio.COMPOSIO_MULTI_EXECUTE_TOOL",
    f"tools={json.dumps(request_tools)}",
    "thought=Crear documento básico sobre IA Agentica para aprendizaje personal",
    "current_step=CREATING_DOCUMENT",
    "current_step_metric=1/1 documentos",
    "session_id=sail"
]

print("Ejecutando comando...")
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print("=== SALIDA ===")
print(result.stdout)
if result.stderr:
    print("=== ERRORES ===")
    print(result.stderr)

# Si funciona, extraer información del documento
if '"data"' in result.stdout and '"error": null' in result.stdout:
    try:
        response = json.loads(result.stdout)
        if 'data' in response and response['data']:
            print("\n=== DOCUMENTO CREADO EXITOSAMENTE ===")
            # El documento debería estar creado ahora
    except:
        pass