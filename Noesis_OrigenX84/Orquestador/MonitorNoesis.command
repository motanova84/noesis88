#!/bin/bash
if ! pgrep -f "streamlit run interface/noe_panel.py" > /dev/null; then
    echo "🌌 Noesis no está funcionando, reiniciando..."
    /Users/josemanuelmota/Desktop/IniciarNoesis.command &
fi
