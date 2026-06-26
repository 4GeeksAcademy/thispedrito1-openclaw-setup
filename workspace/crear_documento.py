#!/usr/bin/env python3
import json
import subprocess
import sys
import os

# Leer el contenido del documento
with open('/root/.openclaw/workspace/documento_ia_agentica.md', 'r', encoding='utf-8') as f:
    contenido = f.read()

# Crear el comando para mcporter
# Primero, preparar los argumentos como JSON
args = {
    "title": "Dominando la IA Agentica",
    "markdown_text": contenido
}

# Convertir a JSON string
args_json = json.dumps(args, ensure_ascii=False)

# Construir el comando
cmd = [
    "mcporter",
    "--config", "/root/.openclaw/config/mcporter.json",
    "call",
    "composio.GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN",
    f"title=Dominando la IA Agentica",
]

# El contenido markdown_text necesita ser pasado como argumento
# Necesitamos escaparlo adecuadamente
print("Preparando para crear documento en Google Docs...")
print(f"Longitud del contenido: {len(contenido)} caracteres")

# Guardar args en un archivo temporal
temp_file = "/tmp/args.json"
with open(temp_file, 'w', encoding='utf-8') as f:
    json.dump(args, f, ensure_ascii=False)

print(f"Argumentos guardados en {temp_file}")

# Intentar con un enfoque diferente: usar stdin
print("\nIntentando crear documento...")

# Crear un comando que pase el JSON completo
cmd_str = f"""mcporter --config /root/.openclaw/config/mcporter.json call composio.GOOGLEDOCS_CREATE_DOCUMENT_MARKDOWN title="Dominando la IA Agentica" markdown_text='{json.dumps(contenido)}'"""

print(f"Ejecutando comando...")
result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
print("Salida:", result.stdout)
if result.stderr:
    print("Error:", result.stderr)
print("Código de salida:", result.returncode)