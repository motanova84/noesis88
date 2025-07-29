#!/bin/bash

# 🚀 Núcleo de Instalación Suprema — Noesis INIT.SH
set -euo pipefail
IFS=$'\n\t'

echo -e "\n🌌 Iniciando instalación del entorno Noésico..."

# === VARIABLES
PROJECT_DIR="$(pwd)"
LOG_FILE="${HOME}/.noesis/init.log"
PY_REQ_FILE="requirements.txt"
PANEL_SCRIPT="noe_panel.py"

# === FUNCIONES
log() {
    local msg="$1"
    echo "[INIT] $msg" | tee -a "$LOG_FILE"
}

# === ENTORNO BÁSICO
log "🛠️ Actualizando sistema..."
apt update -y && apt install -y python3-pip nano curl git

log "🐍 Verificando Python..."
python3 --version || { log "❌ Python3 no está instalado."; exit 1; }

log "📦 Instalando dependencias Python..."
pip3 install --upgrade pip
pip3 install cryptography --quiet

# === EJECUTAR ENOX GUARDIAN
if [[ -f "enox_guardian.py" ]]; then
    log "🔐 Lanzando enox_guardian.py para gestionar token..."
    python3 enox_guardian.py || log "⚠️ Asegúrate de que enox_guardian.py esté configurado."
else
    log "❌ FALTA: No se encuentra 'enox_guardian.py' en $PROJECT_DIR"
fi

# === CONFIGURAR GIT CON IDENTIDAD NOÉSICA
if [[ -f "config_git.sh" ]]; then
    log "🧠 Ejecutando config_git.sh..."
    chmod +x config_git.sh
    ./config_git.sh
else
    log "❌ config_git.sh no encontrado. Proceso detenido."
    exit 1
fi

# === LANZAR PANEL VISUAL (opcional)
if [[ -f "$PANEL_SCRIPT" ]]; then
    log "🎨 Lanzando interfaz visual con Gradio..."
    pip3 install gradio --quiet
    python3 "$PANEL_SCRIPT"
else
    log "ℹ️ Aún no se ha implementado 'noe_panel.py'. Puedes lanzarlo después."
fi

log "✅ INIT completado. Núcleo Noésico operativo."
