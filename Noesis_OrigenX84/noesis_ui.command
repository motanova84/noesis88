#!/bin/zsh
cd ~/Noesis_OrigenX84
source venv/bin/activate

# Verificar si el puerto 8505 está en uso
if lsof -i :8505 > /dev/null; then
  echo "⚠️ El puerto 8505 ya está en uso. Cerrando proceso anterior..."
  PID=$(lsof -ti :8505)
  kill -9 $PID
  sleep 1
fi

# Lanzar interfaz
streamlit run interface/noe_panel.py --server.port 8505


