#!/bin/zsh

cd ~/Documents/Noesis_Clean/noesis88 || exit
source venv/bin/activate

echo "🌀 Activando entorno Noésico..."

# Iniciar procesos clave
pm2 start nexus_webhook_server.js --name "Nexus_Webhook" --watch
pm2 start "n8n start" --name "Nexus_n8n" --watch

# Verifica que el archivo de panel exista antes de ejecutarlo
if [ -f "interface/nexus_panel.py" ]; then
  streamlit run interface/nexus_panel.py
else
  echo "⚠️ Error: interface/nexus_panel.py no encontrado"
fi

