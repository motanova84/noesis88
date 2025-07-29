# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
#!/usr/bin/env python3
# action_executor.py - Ejecutor de acciones del sistema para NEOCORE

import os
import subprocess
import datetime
import platform
import json
import psutil
import time

class ActionExecutor:
    def __init__(self):
        self.base_dir = os.path.expanduser("~/NEOCORE")
        self.actions_log_path = os.path.join(self.base_dir, "logs/actions.log")
        os.makedirs(os.path.dirname(self.actions_log_path), exist_ok=True)
        
        print(f"[ActionExecutor] Sistema de acciones iniciado")
        
    def execute_action(self, action_name, *args, **kwargs):
        """Ejecuta una acción específica y devuelve el resultado"""
        start_time = time.time()
        result = None
        success = False
        
        try:
            # Mapeo de nombres de acciones a métodos
            action_mapping = {
                "abrir_app": self.open_application,
                "crear_nota": self.create_note,
                "buscar_archivo": self.search_files,
                "obtener_estado": self.get_system_status,
                "captura_pantalla": self.take_screenshot,
                "ejecutar_comando": self.run_terminal_command,
                "establecer_recordatorio": self.set_reminder
            }
            
            if action_name in action_mapping:
                action_function = action_mapping[action_name]
                result = action_function(*args, **kwargs)
                success = True
            else:
                result = f"Acción desconocida: {action_name}"
            
        except Exception as e:
            result = f"Error ejecutando acción {action_name}: {str(e)}"
        
        # Registrar acción
        self._log_action(action_name, success, result, time.time() - start_time, args, kwargs)
        
        return result
    
    def _log_action(self, action_name, success, result, execution_time, args, kwargs):
        """Registra la ejecución de una acción en el log"""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action_name,
            "success": success,
            "execution_time": execution_time,
            "args": str(args),
            "kwargs": str(kwargs),
            "result": str(result)
        }
        
        with open(self.actions_log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    # Implementaciones de acciones específicas
    
    def open_application(self, app_name):
        """Abre una aplicación en macOS"""
        try:
            subprocess.Popen(["open", "-a", app_name])
            return f"Aplicación {app_name} abierta correctamente"
        except Exception as e:
            return f"Error al abrir {app_name}: {e}"
    
    def create_note(self, content, title=None):
        """Crea una nota en el sistema"""
        try:
            notes_dir = os.path.join(self.base_dir, "notes")
            os.makedirs(notes_dir, exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            note_title = title if title else f"Nota_{timestamp}"
            filename = os.path.join(notes_dir, f"{note_title}.txt")
            
            with open(filename, "w") as f:
                f.write(f"# {note_title}\n")
                f.write(f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(content)
            
            return f"Nota creada: {filename}"
        except Exception as e:
            return f"Error creando nota: {e}"
    
    def search_files(self, query, location="~", limit=10):
        """Busca archivos en el sistema"""
        try:
            location = os.path.expanduser(location)
            result = subprocess.check_output(["find", location, "-name", f"*{query}*", "-type", "f", "-not", "-path", "*/\.*", "-maxdepth", "3"], stderr=subprocess.STDOUT).decode()
            files = result.strip().split('\n')
            valid_files = [f for f in files if f and os.path.exists(f)][:limit]
            
            if valid_files:
                return valid_files
            else:
                return "No se encontraron archivos"
        except Exception as e:
            return f"Error buscando archivos: {e}"
    
    def get_system_status(self):
        """Obtiene el estado del sistema"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            battery = psutil.sensors_battery()
            
            status = {
                "cpu_usage": f"{cpu}%",
                "memory_usage": f"{memory.percent}%",
                "disk_usage": f"{disk.percent}%",
                "battery": f"{battery.percent}%" if battery else "N/A"
            }
            return status
        except Exception as e:
            return f"Error obteniendo estado: {e}"
    
    def take_screenshot(self, filename=None):
        """Toma una captura de pantalla"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            if not filename:
                filename = f"~/Pictures/neocore_screenshot_{timestamp}.png"
            
            expanded_path = os.path.expanduser(filename)
            subprocess.run(["screencapture", expanded_path])
            return f"Captura guardada en {filename}"
        except Exception as e:
            return f"Error tomando captura: {e}"
    
    def run_terminal_command(self, command, safe_mode=True):
        """Ejecuta un comando en terminal (con restricciones de seguridad)"""
        # Lista de comandos permitidos en modo seguro
        safe_commands = ["ls", "pwd", "echo", "cat", "date", "whoami", "df", "du", "top", "ps", "uptime"]
        
        try:
            # Verificar seguridad
            cmd_parts = command.split()
            base_cmd = cmd_parts[0] if cmd_parts else ""
            
            if safe_mode and base_cmd not in safe_commands:
                return f"Comando no permitido en modo seguro: {base_cmd}"
            
            # Ejecutar comando
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
            return result
        except Exception as e:
            return f"Error ejecutando comando: {e}"
    
    def set_reminder(self, message, minutes=5):
        """Establece un recordatorio usando notificaciones de macOS"""
        try:
            minutes = int(minutes)
            # Crear script AppleScript para la notificación
            script = f'''
            delay {minutes * 60}
            display notification "{message}" with title "NEOCORE Recordatorio" sound name "Glass"
            '''
            
            # Ejecutar AppleScript en segundo plano
            subprocess.Popen(["osascript", "-e", script])
            return f"Recordatorio establecido para {minutes} minutos: {message}"
        except Exception as e:
            return f"Error estableciendo recordatorio: {e}"

# Para pruebas independientes
if __name__ == "__main__":
    executor = ActionExecutor()
    result = executor.get_system_status()
    print(f"Estado del sistema: {result}")
