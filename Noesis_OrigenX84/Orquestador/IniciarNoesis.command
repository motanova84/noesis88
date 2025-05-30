#!/bin/bash

# Detener procesos previos
pm2 stop all 2>/dev/null || true
pm2 delete all 2>/dev/null || true
sudo pkill -f node 2>/dev/null || true

# Verificar el puerto 5678
if sudo lsof -i :5678 | grep -q node; then
  echo "⚠️ Puerto 5678 aún ocupado, forzando limpieza..."
  sudo pkill -f "node.*5678"
else
  echo "✅ Puerto 5678 libre"
fi

# Cargar entorno virtual
echo "🔄 Cargando entorno Noésico..."
cd ~/Documents/Noesis_Clean/noesis88
source venv_new/bin/activate

# Sincronizar con GitHub
echo "🔄 Sincronizando con GitHub..."
git fetch origin main
git reset --hard origin/main
git pull origin main

# Lanzar Streamlit en local
echo "🚀 Lanzando Noésis en local desde interface/noe_panel.py..."
streamlit run interface/noe_panel.py &

# Lanzar en Streamlit Sharing
echo "🚀 Lanzando Noésis en la nube (Streamlit Sharing)..."
streamlit share interface/noe_panel.py &

# Lanzar n8n (opcional, comenta si no lo quieres activar)
echo "🔄 Iniciando n8n..."
pm2 start n8n --name "noesis_n8n" &

echo "✅ Todo listo. Accede a:"
echo "🌐 Local: http://localhost:8505"
echo "🌐 Red: http://192.168.1.34:8505"
echo "🌐 Streamlit Sharing: (el enlace que se genere)"

