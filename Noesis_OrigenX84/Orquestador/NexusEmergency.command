#!/bin/bash

echo "🚨 LIMPIEZA DE EMERGENCIA DE NEXUS PRIME"
echo "===================================="

# Detener absolutamente todos los procesos relacionados
sudo killall -9 python python3 streamlit node pm2 2>/dev/null
pkill -9 -f streamlit
pkill -9 -f node
pkill -9 -f pm2
pkill -9 -f python
pkill -9 -f NexusPrime

# Eliminar posibles configuraciones de inicio automático
sudo launchctl unload /Library/LaunchDaemons/com.nexusprime.autorun.plist 2>/dev/null
sudo rm /Library/LaunchDaemons/com.nexusprime.autorun.plist 2>/dev/null
launchctl unload ~/Library/LaunchAgents/com.nexusprime.*.plist 2>/dev/null
rm ~/Library/LaunchAgents/com.nexusprime.*.plist 2>/dev/null

# Eliminar procesos PM2
pm2 stop all 2>/dev/null
pm2 delete all 2>/dev/null

echo "✅ Limpieza completada"
echo ""
echo "Para volver a iniciar Streamlit de forma controlada, ejecuta:"
echo "cd ~/Documents/Noesis_Clean/noesis88"
echo "streamlit run interface/noe_panel.py"

# Mostrar procesos en ejecución para verificar
echo ""
echo "Verificando procesos residuales:"
ps aux | grep -E 'python|streamlit|node|pm2' | grep -v grep

echo ""
echo "Si aún hay procesos, reinicia la computadora para asegurarte de eliminar todo"
