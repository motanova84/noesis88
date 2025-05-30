#!/bin/bash
# NEXUS PRIME v4.9.2 - Sincronización Neuronal

# Variables de configuración
SSH_KEY="$HOME/.ssh/id_ed25519"
REMOTE_USER="kmm2mlfa1xda5lbd4foj"
REMOTE_HOST="103.196.86.112"
REMOTE_PORT="12724"
REMOTE_PATH="/workspace/noesis88"
LOCAL_PATH="$HOME/Documents/Origen_noe/NEOCORE"
LOCAL_BRAIN="$LOCAL_PATH/core/brain.py"
LOCAL_MEMORY="$LOCAL_PATH/memory"

# Cargar claves
export OPENAI_API_KEY=$(security find-generic-password -s "openai_key" -w 2>/dev/null || echo "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")
export GITHUB_TOKEN=$(security find-generic-password -s "github_token" -w 2>/dev/null || echo "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")

echo "🧬 NEXUS PRIME - SINCRONIZACIÓN NEURONAL"
echo "======================================"

# Verificar conexión SSH
if ssh -o ConnectTimeout=5 -o BatchMode=yes -i "$SSH_KEY" -p $REMOTE_PORT "$REMOTE_USER@$REMOTE_HOST" "echo SYNAPSE_ACTIVE" &>/dev/null; then
  echo "✅ Conexión SSH establecida"
  
  # Sincronizar archivos
  echo "🔄 Sincronizando archivos con RunPod..."
  if [ -f "$LOCAL_BRAIN" ]; then
    scp -P $REMOTE_PORT -i "$SSH_KEY" "$LOCAL_BRAIN" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/core/" || echo "⚠️ Error al sincronizar brain.py"
  else
    echo "⚠️ No se encontró el archivo brain.py local"
  fi
  
  if [ -d "$LOCAL_MEMORY" ]; then
    scp -P $REMOTE_PORT -i "$SSH_KEY" -r "$LOCAL_MEMORY" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/core/" || echo "⚠️ Error al sincronizar carpeta memory"
  else
    echo "⚠️ No se encontró la carpeta memory local"
  fi
  
  # Reiniciar proceso en RunPod
  echo "🔄 Reiniciando proceso neuronal en RunPod..."
  ssh -i "$SSH_KEY" -p $REMOTE_PORT "$REMOTE_USER@$REMOTE_HOST" "
    cd $REMOTE_PATH/core && 
    tmux kill-session -t noebrain 2>/dev/null || true && 
    tmux new-session -d -s noebrain 'python3 brain.py'
  " || echo "⚠️ Error al reiniciar proceso en RunPod"
  
  echo "✅ Sincronización completada exitosamente"
else
  echo "⚠️ No se pudo conectar a RunPod. Verifique la conexión SSH."
fi
