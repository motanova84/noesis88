#!/bin/bash

echo "🧬 INICIANDO NEXUS PRIME v4.9.2"
echo "=============================="

# Detener procesos previos
pkill -f streamlit >/dev/null 2>&1
pkill -f "node.*webhook_server.js" >/dev/null 2>&1

# Activar entorno virtual si existe
cd ~/Documents/Noesis_Clean/noesis88
if [ -d "venv" ]; then
  source venv/bin/activate
elif [ -d "venv_new" ]; then
  source venv_new/bin/activate
fi

# Iniciar Streamlit en segundo plano
streamlit run interface/noe_panel.py &
echo "✅ Interfaz Streamlit iniciada en http://localhost:8503"

# Iniciar servidor webhook
node ~/Documents/Noesis_Clean/noesis88/webhook_server.js &
echo "✅ Servidor webhook iniciado en http://localhost:8080"

echo ""
echo "🚀 Sistema Nexus Prime iniciado correctamente"
echo "Accede a: http://localhost:8503"
