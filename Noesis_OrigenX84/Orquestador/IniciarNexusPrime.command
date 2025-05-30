#!/bin/bash

echo "🧬 NEXUS PRIME v4.9.2 - SISTEMA OPERATIVO"
echo "======================================"
echo "🚀 Iniciando Nexus Prime..."

# Limpiar procesos residuales
sudo killall -9 node streamlit pm2 2>/dev/null
pkill -9 -f nexus_webhook_server.js
pkill -9 -f nexus_panel.py

# Verificar puertos
sudo lsof -i :8080 | grep LISTEN && sudo kill -9 $(sudo lsof -t -i:8080)
sudo lsof -i :8502 | grep LISTEN && sudo kill -9 $(sudo lsof -t -i:8502)

# Iniciar Webhook
cd ~/Desktop
node nexus_webhook_server.js &

# Iniciar Nexus Panel
cd ~/Documents/Noesis_Clean/noesis88
source venv/bin/activate
streamlit run interface/nexus_panel.py &

# Cronjob para backups diarios
(crontab -l 2>/dev/null; echo "0 2 * * * tar -czf ~/Backups/nexus_backup_$(date +\%Y-\%m-\%d).tar.gz ~/Documents/Noesis_Clean/noesis88") | crontab -

echo "🌐 Nexus Prime iniciado correctamente:"
echo "  - Webhook en: http://localhost:8080"
echo "  - Panel en: http://localhost:8502"
echo "📦 Backup diario programado para las 02:00 AM"

