#!/bin/zsh
export PATH="/opt/homebrew/bin:$PATH"
cd /Users/josemanuelmota/Noesis_OrigenX84
echo "🌌 Iniciando Noesis Supremo..."
pm2 start all 2>/dev/null || echo "PM2 ya está activo"
if [ -f "noesis_commander.py" ]; then
    /opt/homebrew/bin/python3 noesis_commander.py
else
    echo "❌ Error: No se encontró noesis_commander.py"
fi
