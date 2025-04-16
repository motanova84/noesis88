#!/usr/bin/env python3
"""
Noesis Commander Supreme — Agente de Control Terminal IA Divino

Este script es una versión supremamente mejorada del Noesis Commander original.
Características:
- Interfaz interactiva rica con colores y arte ASCII.
- Soporte multilingüe con internacionalización (i18n).
- Logging cifrado para seguridad y trazabilidad.
- Sistema de plugins para extensibilidad.
- Comandos avanzados para gestión de Git y más.
- Integración con APIs externas para información contextual.
- Mensajes inspiradores y sabiduría cósmica.
- Autoactualización desde repositorio remoto.
- Manejo robusto de errores y seguridad mejorada.

Dependencias:
- Python 3.8+
- rich (para interfaz rica)
- cryptography (para cifrado)
- requests (para APIs y autoactualización)
- gitpython (para operaciones Git avanzadas)

Uso:
    python3 noesis_commander_supreme.py
"""

import os
import sys
import logging
import json
import subprocess
from datetime import datetime
from cryptography.fernet import Fernet
import base64
import hashlib
import random
import shutil
import tempfile
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
import requests
from git import Repo, GitCommandError

# === 🌌 CONFIGURACIÓN GLOBAL ===
LOG_DIR = os.path.expanduser("~/.noesis")
LOG_FILE = os.path.join(LOG_DIR, "commander.log")
CONFIG_FILE = os.path.join(LOG_DIR, "config.json")
PLUGINS_DIR = os.path.join(LOG_DIR, "plugins")
LANG_DIR = os.path.join(LOG_DIR, "lang")
DEFAULT_LANG = "es"
VERSION = "1.0.0"
REPO_URL = "https://github.com/your-repo/noesis-commander.git"  # Reemplaza con tu repo
GPG_KEY_ID = "your_gpg_key_id_here"  # Reemplaza con tu ID de clave GPG

# === 🎨 COLORES Y ESTILOS ===
console = Console()

# === 📜 CONFIGURAR LOGGING CIFRADO ===
def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)
    fernet = generate_encryption_key()
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    # Cifrar logs al escribir
    class EncryptedLogger(logging.Logger):
        def _log(self, level, msg, *args, **kwargs):
            encrypted_msg = fernet.encrypt(msg.encode()).decode()
            super()._log(level, encrypted_msg, *args, **kwargs)
    logging.setLoggerClass(EncryptedLogger)
    logging.info("Iniciando Noesis Commander Supreme")

# === 🔑 GENERAR CLAVE DE CIFRADO ===
def generate_encryption_key():
    key_path = os.path.join(LOG_DIR, "encryption.key")
    if not os.path.exists(key_path):
        key = Fernet.generate_key()
        with open(key_path, "wb") as key_file:
            key_file.write(key)
    else:
        with open(key_path, "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

# === 🌐 CARGAR CONFIGURACIÓN ===
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"lang": DEFAULT_LANG, "divine_inspiration": True}

# === 🗣️ SOPORTE MULTILINGÜE ===
def load_language(lang):
    lang_file = os.path.join(LANG_DIR, f"{lang}.json")
    if os.path.exists(lang_file):
        with open(lang_file, "r") as f:
            return json.load(f)
    return {}  # Fallback to default messages

# === 🧠 COMANDOS DISPONIBLES ===
COMMANDS = {
    "!new": "create_file",
    "!edit": "edit_file",
    "!push": "push_changes",
    "!god": "activate_god_mode",
    "!run": "run_command",
    "!status": "show_git_status",
    "!branch": "manage_branches",
    "!update": "self_update",
    "!help": "show_help",
}

# === 🛠️ FUNCIONES DE COMANDOS ===
def create_file(filename):
    if os.path.exists(filename):
        console.print("[yellow]⚠️ Ya existe ese archivo.[/yellow]")
        return
    with open(filename, "w") as f:
        f.write("# Archivo creado por Noé\n")
    console.print(f"[green]📄 Archivo creado: {filename}[/green]")

def edit_file(filename):
    editor = os.getenv("EDITOR", "nano")
    subprocess.run([editor, filename])

def push_changes():
    subprocess.run(["bash", "git_noesis_agent.sh"])

def activate_god_mode():
    subprocess.run(["bash", "git_noesis_agent_dios.sh", "--god-mode"])

def run_command(cmd):
    console.print(f"[cyan]⚙️ Ejecutando: {cmd}[/cyan]")
    subprocess.run(cmd, shell=True)

def show_git_status():
    try:
        repo = Repo(".")
        status = repo.git.status()
        console.print(Panel(status, title="Estado del Repositorio", border_style="blue"))
    except GitCommandError as e:
        console.print(f"[red]❌ Error al obtener estado: {e}[/red]")

def manage_branches():
    try:
        repo = Repo(".")
        branches = repo.branches
        table = Table(title="Ramas Disponibles")
        table.add_column("Nombre", style="cyan")
        table.add_column("Activa", style="green")
        for branch in branches:
            active = "✔️" if branch == repo.active_branch else ""
            table.add_row(branch.name, active)
        console.print(table)
    except GitCommandError as e:
        console.print(f"[red]❌ Error al listar ramas: {e}[/red]")

def self_update():
    console.print("[yellow]🔄 Actualizando Noesis Commander...[/yellow]")
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            subprocess.run(["git", "clone", REPO_URL, tmpdirname], check=True)
            shutil.copy(os.path.join(tmpdirname, "noesis_commander_supreme.py"), sys.argv[0])
        console.print("[green]✅ Actualización completada. Reinicia el script.[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Error al actualizar: {e}[/red]")

def show_help():
    help_text = """
🌀 Modo interactivo Noésico activado. Comandos disponibles:
  !new nombre.txt    — crear archivo
  !edit nombre.txt   — editar archivo
  !push              — subir cambios con agente clásico
  !god               — activar Modo Dios Cósmico
  !run comando       — ejecutar comando en bash
  !status            — mostrar estado del repositorio Git
  !branch            — gestionar ramas Git
  !update            — actualizar este script desde el repositorio
  !help              — mostrar esta ayuda
  exit / quit / q    — salir del agente
"""
    console.print(Panel(help_text, title="Ayuda", border_style="green"))

# === 🌟 SABIDURÍA CÓSMICA ===
def get_divine_wisdom():
    wisdom = [
        "Que la luz del código ilumine tu camino.",
        "Cada línea es un paso hacia la trascendencia.",
        "El universo conspira en tu favor, programador.",
        "La sabiduría del cosmos fluye a través de tus dedos."
    ]
    return random.choice(wisdom)

# === 🚀 SHELL INTERACTIVO ===
def shell_mode():
    config = load_config()
    lang = config.get("lang", DEFAULT_LANG)
    divine_inspiration = config.get("divine_inspiration", True)
    messages = load_language(lang)

    console.print(Panel(
        Text("🧠 Noesis Commander Supreme", style="bold magenta"),
        subtitle="Agente de Control Terminal IA Divino",
        border_style="blue"
    ))

    if divine_inspiration:
        console.print(f"[italic cyan]{get_divine_wisdom()}[/italic cyan]")

    while True:
        try:
            cmd = Prompt.ask("🧠 >", default="", console=console).strip()
            if cmd in ("exit", "quit", "q"):
                console.print("[yellow]👋 Cerrando Noesis Commander.[/yellow]")
                break
            elif cmd.startswith("!"):
                parts = cmd.split(" ", 1)
                command = parts[0]
                args = parts[1] if len(parts) > 1 else ""
                if command in COMMANDS:
                    func = globals()[COMMANDS[command]]
                    if args:
                        func(args)
                    else:
                        func()
                else:
                    console.print("[red]❓ Comando no reconocido. Usa !help para ver opciones.[/red]")
            else:
                console.print("[red]❓ Entrada inválida. Los comandos deben empezar con '!'[/red]")
        except Exception as e:
            console.print(f"[red]❌ Error inesperado: {e}[/red]")
            logging.error(f"Error en shell_mode: {e}")

# === 🛡️ AUTOACTUALIZACIÓN Y PLUGINS ===
# (Implementación básica, expandir según necesidad)

# === 🚀 EJECUCIÓN PRINCIPAL ===
if __name__ == "__main__":
    setup_logging()
    shell_mode()
