#!/bin/bash

# === NEXUS PRIME v4.9.2 - MASTER ACTIVATION SCRIPT ===
# Sistema Neural Avanzado - Activación Total

# Limpiar pantalla
clear
echo "🧬 NEXUS PRIME v4.9.2 - INICIANDO SISTEMA NEURAL"
echo "=============================================="
echo ""

# Configuración de rutas
NEXUS_PATH="$HOME/NexusPrime"
DATA_PATH="$NEXUS_PATH/data"
CORE_PATH="$NEXUS_PATH/core"
INTEGRATION_PATH="$NEXUS_PATH/integrations"
INTERFACE_PATH="$NEXUS_PATH/interface"

# Crear directorios necesarios
mkdir -p "$DATA_PATH" "$CORE_PATH" "$INTEGRATION_PATH" "$INTERFACE_PATH"

# Verificar dependencias
echo "🔍 Verificando dependencias..."
pip3 install streamlit pandas requests python-dotenv >/dev/null 2>&1

# Detener procesos previos
echo "🔄 Preparando entorno..."
pkill -f "streamlit run" >/dev/null 2>&1
pkill -f "nexus_core.py" >/dev/null 2>&1
pkill -f "python.*NexusPrime" >/dev/null 2>&1

# Exportar claves y variables
export OPENAI_API_KEY="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"
export GITHUB_TOKEN="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"
export N8N_API_KEY="rpa_TEFDNRAOJICU3TRNTG2PRAUJMBVAUSBWAB2W2CYFfkhnpf"
export GOOGLE_API_KEY="AIzaSyC49O2xUQTaiJTRmrjDBRLC_Yfz6Nvxe0A"
export RUNPOD_USER="kmm2mlfa1xda5lbd4foj"
export RUNPOD_HOST="103.196.86.112"
export RUNPOD_PORT="12724"
export RUNPOD_PASSWORD="6lqd98ry4zhj627mgbl4"

# Iniciar núcleo del sistema
echo "🧠 Iniciando núcleo neuronal..."
python3 "$CORE_PATH/nexus_core.py" &
CORE_PID=$!
echo "✅ Núcleo iniciado (PID: $CORE_PID)"

# Esperar a que el núcleo se inicialice
sleep 2

# Verificar GitHub y RunPod
echo "🔄 Sincronizando con servicios externos..."
python3 "$INTEGRATION_PATH/github_sync.py" &
python3 "$INTEGRATION_PATH/runpod_sync.py" &

# Esperar a que las sincronizaciones se completen
sleep 3

# Iniciar interfaz Streamlit
echo "🚀 Iniciando interfaz neural..."
cd "$NEXUS_PATH"
streamlit run "$INTERFACE_PATH/nexus_panel.py" &
INTERFACE_PID=$!

echo ""
echo "✅ NEXUS PRIME ESTÁ ACTIVO Y OPERATIVO"
echo "====================================="
echo "🌐 Interfaz Neural: http://localhost:8501"
echo ""
echo "Estado de componentes:"
echo "🧠 Núcleo Neuronal: Activo (PID: $CORE_PID)"
echo "🖥️ Interfaz Neural: Activa (PID: $INTERFACE_PID)"
echo "📡 Conexiones Externas: En proceso"
echo ""
echo "Sistema completamente automatizado y autónomo."
