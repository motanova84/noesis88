#!/bin/bash

# === NEXUS PRIME v4.9.2 - ESTADO LOCAL ===
clear
echo "🧬 NEXUS PRIME v4.9.2 - ESTADO DEL SISTEMA"
echo "========================================"
echo "📅 Fecha: $(date)"
echo ""

# Verificar procesos críticos
echo "🔍 PROCESOS CRÍTICOS"
echo "----------------"

# Comprobar Streamlit
if pgrep -f "streamlit run interface/noe_panel.py" > /dev/null; then
    echo "✅ Interfaz Streamlit: ACTIVA"
else
    echo "❌ Interfaz Streamlit: INACTIVA"
fi

# Comprobar Webhook
if curl -s http://localhost:8080/ping > /dev/null; then
    echo "✅ Servidor Webhook: ACTIVO"
else
    echo "❌ Servidor Webhook: INACTIVO"
fi

# Verificar claves API
echo ""
echo "🔑 CLAVES API"
echo "---------"

check_key() {
    local key_name="$1"
    local key_value="$2"
    
    if [[ -z "$key_value" ]]; then
        echo "❌ $key_name: No configurada"
    else
        local prefix="${key_value:0:5}"
        local suffix="${key_value: -5}"
        echo "✅ $key_name: ${prefix}...${suffix}"
    fi
}

# Cargar claves
OPENAI_KEY="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"
GITHUB_KEY="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"
N8N_KEY="rpa_TEFDNRAOJICU3TRNTG2PRAUJMBVAUSBWAB2W2CYFfkhnpf"
GOOGLE_KEY="AIzaSyC49O2xUQTaiJTRmrjDBRLC_Yfz6Nvxe0A"

# Verificar claves
check_key "OpenAI API" "$OPENAI_KEY"
check_key "GitHub Token" "$GITHUB_KEY"
check_key "n8n API" "$N8N_KEY"
check_key "Google API" "$GOOGLE_KEY"

# Mostrar procesos PM2
echo ""
echo "🔄 PROCESOS PM2"
echo "------------"
pm2 list

# Mostrar recursos del sistema
echo ""
echo "📊 RECURSOS DEL SISTEMA"
echo "-------------------"
# CPU
CPU_USAGE=$(ps -A -o %cpu | awk '{s+=$1} END {print s}')
CPU_CORES=$(sysctl -n hw.ncpu)
echo "⚡ Uso de CPU: ${CPU_USAGE}% (${CPU_CORES} núcleos)"

# Memoria
MEM_TOTAL=$(sysctl -n hw.memsize | awk '{print $1 / 1024 / 1024 / 1024 " GB"}')
MEM_USED=$(ps -caxm -orss= | awk '{ sum += $1 } END { print sum / 1024 / 1024 " GB" }')
echo "🧠 Uso de Memoria: ${MEM_USED} / ${MEM_TOTAL}"

# Disco
DISK_USAGE=$(df -h ~ | awk 'NR==2 {print $5 " (" $4 " libre)"}')
echo "💾 Uso de Disco: ${DISK_USAGE}"

# Enlaces importantes
echo ""
echo "🔗 ENLACES IMPORTANTES"
echo "-------------------"
echo "🌐 Interfaz web: http://localhost:8505"
echo "🌐 Estado del sistema: http://localhost:8080/status"
echo "🌐 Webhook: http://localhost:8080/webhook/sync_node"

echo ""
echo "✅ Verificación de estado completada"
