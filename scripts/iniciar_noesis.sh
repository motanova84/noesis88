#!/bin/bash

cd ~/Proyectos/Noesis_OrigenX84 || exit 1

# Activar entorno virtual
source venv_noe/bin/activate

# Ejecutar Noesis Panel con Streamlit
streamlit run interface/noe_panel.py \
  --server.enableXsrfProtection false \
  --server.headless true \
  --server.port 8504 \
  > noesis_logs.txt 2>&1 &

echo "✅ Noesis iniciado en segundo plano."
echo "📜 Logs: tail -f ~/Proyectos/Noesis_OrigenX84/noesis_logs.txt"
echo "🌐 Abre http://localhost:8504 en tu navegador"


