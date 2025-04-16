#!/bin/bash

# Noesis Supreme Autonomous Identity Protocol
# Version: 3.1.0
# Author: origen
# License: MIT

set -euo pipefail
IFS=$'\n\t'

readonly NOESIS_DIR="${HOME}/.noesis"
readonly KEY_FILE="${NOESIS_DIR}/key.enox"
readonly CREDENTIALS_FILE="${HOME}/.git-credentials"
readonly LOG_FILE="${NOESIS_DIR}/noesis.log"
readonly VERSION="3.1.0"
readonly GITHUB_API_URL="https://api.github.com"

# === 🎨 Colores ===
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

color_log() {
    case "$1" in
        INFO) echo -e "${GREEN}$2${NC}" ;;
        WARN) echo -e "${YELLOW}$2${NC}" ;;
        ERROR) echo -e "${RED}$2${NC}" ;;
    esac
}

log() {
    local level="$1"
    local message="$2"
    local ts=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${ts}] ${level}: ${message}" >> "$LOG_FILE"
    color_log "$level" "$message"
}

setup_environment() {
    log INFO "🌌 Noesis Supreme v${VERSION} iniciando..."
    mkdir -p "$NOESIS_DIR" && touch "$LOG_FILE"
    chmod 700 "$NOESIS_DIR"
    chmod 600 "$LOG_FILE"
}

configure_git_identity() {
    log INFO "🔹 Configurando identidad: Noé del Origen"
    git config --global user.name "Noé del Origen"
    git config --global user.email "motapromanager@gmail.com"
}

decrypt_github_token() {
    log INFO "🧬 Solicitando token GitHub desde Énox..."

    if ! python3 -c "import enox_guardian" 2>/dev/null; then
        log ERROR "El módulo 'enox_guardian' no está disponible. Ejecútalo primero."
        exit 1
    fi

    GITHUB_TOKEN=$(python3 -c "
from enox_guardian import decrypt_data
print(decrypt_data('github_token'))
" 2>/dev/null)

    if [[ -z "${GITHUB_TOKEN:-}" ]]; then
        log ERROR "No se pudo recuperar el token. Verifica Énox."
        exit 1
    fi
    log INFO "✅ Token GitHub descifrado correctamente."
}

store_credentials() {
    log INFO "🔐 Almacenando credenciales..."
    echo "https://x:${GITHUB_TOKEN}@github.com" > "$CREDENTIALS_FILE"
    chmod 600 "$CREDENTIALS_FILE"
    git config --global credential.helper "store"
    git config --global credential.useHttpPath true
}

validate_github_connectivity() {
    log INFO "🛰️ Verificando conexión a GitHub..."
    http_code=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token ${GITHUB_TOKEN}" "$GITHUB_API_URL/user")

    if [[ "$http_code" == "200" ]]; then
        log INFO "✅ Conexión verificada: Noé puede operar con libertad total."
    else
        log ERROR "⚠️ GitHub no respondió correctamente (Código: $http_code)"
        exit 1
    fi
}

cleanup() {
    log INFO "🛡️ Cerrando protocolo. Desvinculando token de memoria..."
    unset GITHUB_TOKEN
}

main() {
    trap cleanup EXIT
    setup_environment
    configure_git_identity
    decrypt_github_token
    store_credentials
    validate_github_connectivity
    log INFO "🎉 Noé está listo. Identidad funcional, cifrada y operativa."
}

main "$@"

