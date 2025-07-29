#!/bin/bash

# 🚀 Git Noesis Agent — Subida y Commit Autónomo
set -euo pipefail
IFS=$'\n\t'

LOG_FILE="$HOME/.noesis/git.log"
COMMIT_MESSAGE="${1:-⚙️ Actualización automática por Noé — $(date '+%Y-%m-%d %H:%M:%S')}"

echo "[AGENT] Preparando archivos..." | tee -a "$LOG_FILE"

git add . >> "$LOG_FILE" 2>&1 || {
    echo "[ERROR] Fallo en 'git add'" | tee -a "$LOG_FILE"
    exit 1
}

if git diff --cached --quiet; then
    echo "[INFO] No hay cambios para subir." | tee -a "$LOG_FILE"
    exit 0
fi

git commit -m "$COMMIT_MESSAGE" >> "$LOG_FILE" 2>&1 || {
    echo "[ERROR] Fallo al hacer commit." | tee -a "$LOG_FILE"
    exit 1
}

git push origin main >> "$LOG_FILE" 2>&1 || {
    echo "[ERROR] Fallo al hacer push a GitHub." | tee -a "$LOG_FILE"
    exit 1
}

echo "[OK] Cambios subidos exitosamente: $COMMIT_MESSAGE" | tee -a "$LOG_FILE"

