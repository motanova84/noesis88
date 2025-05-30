#!/bin/bash

# === NEXUS PRIME v4.9.2 - MONITOR LOCAL ===
clear
echo "🧬 NEXUS PRIME v4.9.2 - MONITOR NEURONAL"
echo "======================================"
echo "📅 Fecha: $(date)"
echo ""

# Verificar procesos críticos
echo "🔍 Verificando procesos críticos..."

# Comprobar Streamlit
if pgrep -f "streamlit run interface/noe_panel.py" > /dev/null; then
    echo "✅ Interfaz Streamlit: ACTIVA"
else
    echo "❌ Interfaz Streamlit: INACTIVA"
    echo "🔄 Reactivando Streamlit..."
    ~/Desktop/NexusPrimeActivate.command &
fi

# Comprobar Webhook
if curl -s http://localhost:8080/ping > /dev/null; then
    echo "✅ Servidor Webhook: ACTIVO"
else
    echo "❌ Servidor Webhook: INACTIVO"
    echo "🔄 Reactivando servidor webhook..."
    pm2 restart Nexus_Webhook >/dev/null 2>&1 || pm2 start ~/Desktop/nexus_webhook_server.js --name "Nexus_Webhook"
fi

# Comprobar recursos del sistema
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

# Mostrar procesos PM2
echo ""
echo "🔄 PROCESOS PM2"
echo "------------"
pm2 list

echo ""
echo "✅ Monitorización completada"
echo "Para monitorización continua, ejecuta este script con --loop"

# Modo de monitorización continua
if [[ "$1" == "--loop" ]]; then
    echo ""
    echo "🔄 Iniciando monitorización continua (Ctrl+C para detener)..."
    echo ""
    while true; do
        clear
        ~/Desktop/NexusPrimeMonitor.command
        sleep 60
    done
fi
