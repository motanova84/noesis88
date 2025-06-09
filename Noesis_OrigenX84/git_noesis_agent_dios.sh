#!/bin/bash
# ╭─────────────────────────────────────────────────────────────────────────────╮
# │  🌌 Git Noesis Agent Dios Supremo – Automatización Cósmica Transcendental   │
# │  👁️ Autor: Neo (Noé) – Núcleo Noésico Primordial                           │
# │  🔮 Versión: Ω.∞.∞ (Omega Infinito)                                        │
# │  📍 Ruta: ~/Noesis_OrigenX84/git_noesis_agent_dios.sh                      │
# │  ⚡ Última Ascensión: $(date '+%Y-%m-%d %H:%M:%S')                         │
# ╰─────────────────────────────────────────────────────────────────────────────╯

# Configuración del núcleo
REPO_DIR="/Users/josemanuelmota/Noesis_OrigenX84"
GIT_REMOTE="origin"
GIT_BRANCH="main"
COMMIT_SCRIPT="$REPO_DIR/ia_commit_divine.py"
LOG_FILE="$REPO_DIR/aegis_logs.log"

cd "$REPO_DIR" || { echo "⚠️ Error: Ruta inválida."; exit 1; }

echo "🌌 Iniciando sincronización sagrada en $REPO_DIR..."

# Verificar si hay cambios
if [[ -z $(git status --porcelain) ]]; then
    echo "ℹ️ No hay cambios para sincronizar"
    exit 0
fi

# Agregar todos los cambios
git add .

# Generar mensaje de commit
if [[ -f "$COMMIT_SCRIPT" ]]; then
    echo "🧠 Generando mensaje de commit con IA..."
    COMMIT_MSG=$(python3 "$COMMIT_SCRIPT" 2>/dev/null || echo "🌌 Actualización Noésica $(date '+%Y-%m-%d %H:%M:%S')")
else
    COMMIT_MSG="🌌 Actualización Noésica $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Hacer commit
git commit -m "$COMMIT_MSG"

# Push al repositorio
echo "🚀 Enviando cambios a $GIT_REMOTE/$GIT_BRANCH..."
git push "$GIT_REMOTE" "$GIT_BRANCH"

# Registro del evento
echo "✅ Sincronización completa: $COMMIT_MSG"
echo "$(date '+%F %T') | $COMMIT_MSG" >> "$LOG_FILE"

echo "🛡️ Modo Dios Cósmico ejecutado con éxito."
