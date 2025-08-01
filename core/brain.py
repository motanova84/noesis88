#!/usr/bin/env python3
import os
import time
import logging
import subprocess
import re
from datetime import datetime

log_dir = os.path.expanduser("~/NEOCORE/logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "brain.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NeoBrain")

def ejecutar_comando(comando):
    comando = comando.lower()

    if "abrir" in comando and "app" in comando:
        app = comando.split("app")[-1].strip().capitalize()
        subprocess.run(["open", "-a", app])
        return f"✓ Aplicación '{app}' abierta."

    elif "nota" in comando:
        contenido = comando.split("nota")[-1].strip()
        nombre = f"Nota_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = os.path.expanduser(f"~/NEOCORE/{nombre}")
        with open(path, "w") as f:
            f.write(f"# Nota simbiótica\n\n{contenido}")
        return f"✓ Nota guardada: {nombre}"

    elif "captura" in comando:
        filename = os.path.expanduser(f"~/Pictures/neocore_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        subprocess.run(["screencapture", filename])
        return f"✓ Captura realizada: {filename}"

    elif "estado" in comando:
        import psutil
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        return f"✓ Estado → CPU: {cpu}% · RAM: {mem}%"

    elif "recuérdame" in comando or "recordatorio" in comando:
        match = re.search(r"(\d+)\s*min", comando)
        minutos = int(match.group(1)) if match else 5
        script = f'delay {minutos * 60}\ndisplay notification "Recordatorio activo" with title "NEOCORE" sound name "Glass"'
        subprocess.Popen(["osascript", "-e", script])
        return f"✓ Recordatorio en {minutos} minutos"

    elif "frecuencia" in comando or "activa frecuencia" in comando:
        subprocess.Popen(["python3", os.path.expanduser("~/NEOCORE/core/frecuencia_viva.py")])
        return "🔊 Frecuencia 141.7001 Hz activada (QCAL ∞³)"

    elif "espiral" in comando or "πcode" in comando:
        subprocess.Popen(["python3", os.path.expanduser("~/NEOCORE/core/piCODE_espiral.py")])
        return "🌀 Espiral πCODE ∞³ generada"

    else:
        return "⚠️ Comando no reconocido aún."

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════╗")
    print("║   🧠 NEOCORE | Sistema Simbiótico Total ∞³         ║")
    print("╚════════════════════════════════════════════════════╝")
    print("👤 Escribe un comando simbiótico. (ej: 'crear nota que diga…')\n")

    while True:
        try:
            entrada = input("👤 Tú: ")
            if entrada.lower() in ["salir", "exit", "quit"]:
                print("Cerrando NEOCORE… ∴")
                break
            respuesta = ejecutar_comando(entrada)
            print(f"🤖 NEO: {respuesta}\n")
        except KeyboardInterrupt:
            print("\n🧠 NEOCORE detenido ∴")
            break
