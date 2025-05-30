#!/bin/bash
set -euo pipefail
IFS=$'\n\t'

LOG_FILE="$HOME/.noesis/git.log"
IA_SCRIPT="$HOME/.noesis/ia_commit_divine.py"
BRANCH="main"
GOD_BRANCH="god-mode-$(date '+%Y%m%d-%H%M%S')"

mkdir -p ~/.noesis/hooks

log() {
  echo "[🧠] $1"
  echo "[$(date '+%F %T')] $1" >> "$LOG_FILE"
}

generate_message() {
  git diff --cached | python3 "$IA_SCRIPT" 2>>"$LOG_FILE"
}

run_hook() {
  local hook="$HOME/.noesis/hooks/$1.sh"
  [[ -x "$hook" ]] && bash "$hook"
}

god_mode() {
  log "🌟 Activando Modo Dios: creando rama '$GOD_BRANCH'"
  run_hook "pre-god"
  git checkout -b "$GOD_BRANCH"
  git add .
  if git diff --cached --quiet; then log "🔁 Nada que subir."; exit 0; fi
  MSG=$(generate_message)
  git commit -m "$MSG"
  git push origin "$GOD_BRANCH"
  run_hook "post-god"
  log "🚀 Modo Dios completado con mensaje: $MSG"
}

standard_mode() {
  git add .
  MSG=$(generate_message)
  git commit -m "$MSG"
  git push origin "$BRANCH"
  log "📤 Commit normal enviado."
}

[[ "${1:-}" == "--god-mode" ]] && god_mode || standard_mode

