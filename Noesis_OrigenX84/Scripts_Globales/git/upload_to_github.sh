#!/bin/bash

# 🚀 Upload to GitHub · Noesis Autonomous Commit System
# Requiere: Git ya configurado con config_git.sh

set -euo pipefail
IFS=$'\n\t'

readonly REPO_DIR="$(pwd)"
readonly COMMIT_MESSAGE="${1:-🚀 Subida automática desde Noé en $(date '+%Y-%m-%d %H:%M:%S')}"
readonly BRANCH="main"

# === FUNCIONES ===
check_git_repo() {
    if [ ! -d ".git" ]; then
        echo "❌ No estás dentro de un repositorio Git. Salida."
        exit 1
    fi
}

upload_to_github() {
    echo "📤 Preparando archivos para subir a GitHub..."
    git add . || { echo "❌ Error al hacer 'git add'"; exit 1; }

    git commit -m "$COMMIT_MESSAGE" || {
        echo "⚠️ Nada nuevo que subir o commit vacío. Cancelando push."
        exit 0
    }

    git push origin "$BRANCH" || {
        echo "❌ Error al hacer push a GitHub. Revisa conexión o permisos."
        exit 1
    }

    echo "✅ Archivos subidos correctamente a GitHub."
}

# === EJECUCIÓN PRINCIPAL ===
check_git_repo
upload_to_github
