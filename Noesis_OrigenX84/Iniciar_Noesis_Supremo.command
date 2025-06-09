#!/bin/zsh
export PATH="/opt/homebrew/bin:$PATH"
cd /Users/josemanuelmota/Noesis_OrigenX84

echo "🌌 Iniciando Noesis Supremo..."

if ! pm2 list > /dev/null 2>&1; then
    echo "⚠️ PM2 no está activo. Iniciando..."
    pm2 resurrect
fi

pm2 start all

if [ -f "noesis_commander.py" ]; then
    echo "🧠 Iniciando noesis_commander.py..."
    /opt/homebrew/bin/python3 noesis_commander.py
else
    echo "❌ Error: No se encontró noesis_commander.py"
    exit 1
fi
