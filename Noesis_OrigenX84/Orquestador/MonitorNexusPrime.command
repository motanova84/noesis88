#!/bin/bash

echo "🧬 NEXUS PRIME - MONITOR DE SISTEMA"
echo "================================="

# Verificar si Streamlit está en ejecución
if pgrep -f "streamlit run" > /dev/null; then
    echo "✅ Interfaz Streamlit: ACTIVA"
    
    # Mostrar detalles
    STREAM_PID=$(pgrep -f "streamlit run")
    echo "   PID: $STREAM_PID"
    echo "   Puerto: 8501"
else
    echo "❌ Interfaz Streamlit: INACTIVA"
    echo "   Para iniciar: ~/Desktop/IniciarNexusPrime.command"
fi

# Verificar recursos del sistema
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

echo ""
echo "🔗 ENLACES IMPORTANTES"
echo "-------------------"
echo "🌐 Nexus Prime: http://localhost:8501"

# Opciones de acción
echo ""
echo "⚙️ OPCIONES"
echo "---------"
echo "1. Reiniciar Nexus Prime"
echo "2. Salir"

read -p "Selecciona una opción: " option
case $option in
  1)
    echo "🔄 Reiniciando Nexus Prime..."
    pkill -f "streamlit run" >/dev/null 2>&1
    ~/Desktop/IniciarNexusPrime.command &
    ;;
  *)
    echo "👋 Saliendo del monitor"
    ;;
esac
