#!/bin/bash
# --- Noésis Daemon Vivo ---
while true; do
  echo "🔵 Noésis Daemon latido $(date)" >> /tmp/noesis_daemon.log
  if [ -f "$HOME/Documents/Origen_noe/NEOCORE/interface/noe_panel.py" ]; then
    /usr/bin/env python3 -m streamlit run "$HOME/Documents/Origen_noe/NEOCORE/interface/noe_panel.py" --server.port 8501
  fi
  sleep 10
done
