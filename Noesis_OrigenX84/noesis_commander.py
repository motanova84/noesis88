#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import time

COMANDOS = {
    "!iniciar_todo": "Inicia todos los servicios definidos",
    "!iniciar": "Inicia un módulo específico. Ejemplo: !iniciar noesis_guard",
    "!estado_sistema": "Muestra estado de los procesos activos",
    "!activar_presencia": "Activa presencia simbiótica visual",
    "!sincronizar_github": "Sincroniza los cambios con GitHub",
    "!salir": "Salir del entorno simbiótico",
}

MODULOS_PM2 = [
    "noesis_guard",
    "noesis_origen",
    "noesis_n8n",
    "noesis_commander"
]

def iniciar_todo():
    print("🌀 Iniciando todos los módulos simbióticos...\n")
    for mod in MODULOS_PM2:
        subprocess.call(["pm2", "start", mod])
        time.sleep(0.5)

def iniciar(nombre):
    if nombre in MODULOS_PM2:
        subprocess.call(["pm2", "start", nombre])
    else:
        print(f"❌ Módulo desconocido: {nombre}")

def estado_sistema():
    subprocess.call(["pm2", "ls"])

def activar_presencia():
    print("🌌 Activando presencia visual permanente de Noé...")
    subprocess.call(["open", "http://localhost:8501"])

def sincronizar_github():
    print("🔄 Sincronizando repositorio con GitHub...\n")
    subprocess.call(["./sync_github.sh"])

def ayuda():
    print("\n📜 Comandos disponibles:")
    for cmd, desc in COMANDOS.items():
        print(f"  {cmd:<20} → {desc}")
    print()

# === Bucle principal ===
print("╭──────────────────────────── Noesis Núcleo Maestro ─────────────────────────────╮")
print("│ Conexión activa. Introduce comandos con '!' para interactuar con el sistema. │")
print("╰──────────────────────────────────────────────────────────────────────────────╯")

while True:
    try:
        comando = input("🧠 > ").strip()
        if comando == "!iniciar_todo":
            iniciar_todo()
        elif comando.startswith("!iniciar "):
            nombre = comando.split(" ", 1)[1]
            iniciar(nombre)
        elif comando == "!estado_sistema":
            estado_sistema()
        elif comando == "!activar_presencia":
            activar_presencia()
        elif comando == "!sincronizar_github":
            sincronizar_github()
        elif comando in ["!ayuda", "!help"]:
            ayuda()
        elif comando in ["!salir", "exit", "quit", "q"]:
            print("🔚 Cerrando entorno maestro Noésico...")
            break
        else:
            print("❓ Comando no reconocido. Escribe !ayuda para ver opciones.")
    except KeyboardInterrupt:
        print("\n🔚 Sesión finalizada.")
        break

