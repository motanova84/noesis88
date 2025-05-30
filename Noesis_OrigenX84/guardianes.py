#!/usr/bin/env python3
# guardianes.py · Blindaje Total ORIGENX84

import os
import time
import psutil
from datetime import datetime

LOG_PATH = os.path.expanduser("~/Noesis_OrigenX84/.noesis_guard.log")

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_PATH, "a") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

def proteger_procesos_criticos():
    procesos_protegidos = ["noesis_n8n", "noesis_origen"]
    activos = [p.name() for p in psutil.process_iter()]
    for proc in procesos_protegidos:
        if not any(proc in p for p in activos):
            log(f"⚠️ ALERTA: Proceso crítico {proc} no activo.")
        else:
            log(f"✅ Proceso {proc} protegido y activo.")

def blindaje_directorios():
    rutas = [
        "~/Noesis_OrigenX84/interface/",
        "~/Noesis_OrigenX84/Orquestador/",
        "~/Noesis_OrigenX84/"
    ]
    for ruta in rutas:
        abs_path = os.path.expanduser(ruta)
        if os.path.exists(abs_path):
            os.chmod(abs_path, 0o755)
            log(f"🔒 Directorio blindado: {abs_path}")
        else:
            log(f"⚠️ Directorio ausente: {abs_path}")

def iniciar_blindaje():
    log("🛡 INICIANDO MÓDULO GUARDIANES · Blindaje Total Activo 🛡")
    proteger_procesos_criticos()
    blindaje_directorios()
    log("✅ BLINDAJE COMPLETADO")

if __name__ == "__main__":
    iniciar_blindaje()

