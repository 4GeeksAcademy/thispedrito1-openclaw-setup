#!/usr/bin/env python3
import json
import subprocess
import sys

# Leer contenido
with open('/root/.openclaw/workspace/documento_ia_agentica.md', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Construir la solicitud para COMPOSIO_MULTI_EXECUTE_TOOL
request = {
    "tools": [
        {
            "tool": "GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN",
            "arguments": {
                "title": "Dominando la IA Agentica",
                "markdown_text": contenido
            }
        }
    ],
    "thought": "Crear documento básico sobre IA Agentica para aprendizaje personal",
    "current_step": "CREATING_DOCUMENT",
    "current_step_metric": "1/1 documentos",
    "session_id": "sail"
}

# Guardar solicitud en archivo
request_file = "/tmp/mcp_request.json"
with open(request_file, 'w', encoding='utf-8') as f:
    json.dump(request, f, ensure_ascii=False)

print(f"Solicitud guardada en {request_file}")

# Ejecutar mcporter
cmd = [
    "mcporter",
    "--config", "/root/.openclaw/config/mcporter.json",
    "call",
    "composio.COMPOSIO_MULTI_EXECUTE_TOOL",
    f"tools={json.dumps([request['tools'][0]])}",
    f"thought={request['thought']}",
    f"current_step={request['current_step']}",
    f"current_step_metric={request['current_step_metric']}",
    f"session_id={request['session_id']}"
]

print("Ejecutando:", " ".join(cmd[:6]), "...")
result = subprocess.run(cmd, capture_output=True, text=True)
print("Salida:", result.stdout)
if result.stderr:
    print("Error:", result.stderr)

# Intentar enfoque alternativo si falla
if "not found" in result.stdout or "Validation error" in result.stdout:
    print("\n=== Intentando enfoque alternativo ===")
    
    # Usar googledocs directamente
    alt_cmd = f"""echo '{json.dumps(contenido)}' | mcporter --config /root/.openclaw/config/mcporter.json call googledocs.CREATE_DOCUMENT title="Dominando la IA Agentica" """
    print("Comando alternativo:", alt_cmd[:100], "...")
    
    result2 = subprocess.run(alt_cmd, shell=True, capture_output=True, text=True)
    print("Salida alternativa:", result2.stdout)
    if result2.stderr:
        print("Error alternativo:", result2.stderr)