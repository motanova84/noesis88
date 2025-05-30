#!/bin/bash

# Función para detener todo
stop_all() {
  echo "🛑 Deteniendo todos los procesos..."
  pkill -9 -f streamlit
  pkill -f "node.*webhook"
  pm2 stop all 2>/dev/null
  echo "✅ Todos los procesos detenidos"
}

# Función para iniciar todo
start_all() {
  echo "🚀 Iniciando sistema Nexus Prime..."
  
  # Asegurarse de que no haya otras instancias
  stop_all
  
  # Iniciar Streamlit (solo una instancia)
  cd ~/Documents/Noesis_Clean/noesis88
  if [ -d "venv" ]; then
    source venv/bin/activate
  elif [ -d "venv_new" ]; then
    source venv_new/bin/activate
  fi
  
  # Iniciar sin abrir el navegador (evita múltiples ventanas)
  streamlit run interface/noe_panel.py --server.headless true &
  STREAMLIT_PID=$!
  echo "✅ Streamlit iniciado (PID: $STREAMLIT_PID)"
  
  # Iniciar webhook solo si no está corriendo
  if ! pgrep -f "node.*webhook" > /dev/null; then
    node ~/Documents/Noesis_Clean/noesis88/webhook_server.js &
    echo "✅ Webhook iniciado"
  fi
  
  echo ""
  echo "Sistema Nexus Prime iniciado"
  echo "Accede manualmente a: http://localhost:8501"
}

# Función para mostrar estado
show_status() {
  echo "📊 Estado del Sistema Nexus Prime:"
  echo "--------------------------"
  if pgrep -f "streamlit run" > /dev/null; then
    echo "✅ Streamlit: Ejecutándose"
  else
    echo "❌ Streamlit: Detenido"
  fi
  
  if pgrep -f "node.*webhook" > /dev/null; then
    echo "✅ Webhook: Ejecutándose"
  else
    echo "❌ Webhook: Detenido"
  fi
}

# Menú de opciones
show_menu() {
  clear
  echo "🧬 NEXUS PRIME - PANEL DE CONTROL"
  echo "=============================="
  echo "1. Iniciar sistema"
  echo "2. Detener sistema"
  echo "3. Ver estado"
  echo "4. Salir"
  echo ""
  read -p "Selecciona una opción: " choice
  
  case $choice in
    1) start_all ;;
    2) stop_all ;;
    3) show_status ;;
    4) exit 0 ;;
    *) echo "Opción no válida" ;;
  esac
  
  read -p "Presiona Enter para continuar..."
  show_menu
}

# Iniciar menú
show_menu
