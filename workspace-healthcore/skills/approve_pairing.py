import sys
import json
import os
from datetime import datetime

def main():
    # 1. Validar argumentos mínimos requeridos
    if len(sys.argv) < 3:
        print("ERROR: Faltan argumentos. Uso: python approve_pairing.py <employee_id> <verification_code>")
        sys.exit(1)
        
    emp_id = sys.argv[1]
    input_code = sys.argv[2]
    
    # Obtener el directorio donde reside este script (workspace-healthcore/skills/)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Subir un nivel para llegar a la raíz del workspace (workspace-healthcore/)
    workspace_dir = os.path.dirname(current_dir)
    
    # Definir rutas absolutas e independientes de la ejecución
    db_path = os.path.join(workspace_dir, "onboarding-database.json")
    log_dir = os.path.join(workspace_dir, "logs")
    log_path = os.path.join(log_dir, "pairing_audit.log")
    
    # 2. Cargar el registro del empleado desde la base de datos aislada
    if not os.path.exists(db_path):
        print(f"ERROR: No se encuentra el archivo de datos en {db_path}")
        sys.exit(1)
        
    try:
        with open(db_path, "r") as f:
            db = json.load(f)
    except Exception as e:
        print(f"ERROR: Fallo al leer la base de datos: {e}")
        sys.exit(1)
        
    if emp_id not in db:
        print(f"ERROR: El ID de empleado {emp_id} no está registrado en el flujo de onboarding.")
        sys.exit(1)
        
    employee_record = db[emp_id]
    
    # 3. Validar el código provisto por RRHH contra el código guardado
    if input_code != employee_record["verification_code"]:
        print("ERROR: El Código de verificación de seguridad es incorrecto. Acceso no concedido.")
        sys.exit(1)
        
    # 4. Modificar el estado tras la validación exitosa
    employee_record["status"] = "active"
    employee_record["state_changes_since_last_summary"] += 1
    employee_record["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Guardar cambios en el JSON
    with open(db_path, "w") as f:
        json.dump(db, f, indent=2)
        
    # 5. Generar log de auditoría sin exponer secretos (Cumplimiento de Claire Whitfield)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    timestamp = datetime.utcnow().isoformat() + "Z"
    with open(log_path, "a") as log_file:
        log_file.write(f"[{timestamp}] ID: {emp_id} | Telegram_ID: {employee_record.get('telegram_pending_id', 'N/A')} | Action: PAIRING_APPROVED_BY_CODE\n")
        
    print(f"SUCCESS: Código verificado. Dispositivo de Telegram aprobado para el empleado {emp_id}.")
    sys.exit(0)

if __name__ == "__main__":
    main()