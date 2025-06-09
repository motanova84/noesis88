#!/bin/zsh

echo "🔧 Reparando nombres de procesos mal definidos..."
if pm2 list | grep -q "noesis_commander_origen"; then
    pm2 delete noesis_commander_origen
fi

echo "🚀 Iniciando módulos principales..."
pm2 start /Users/josemanuelmota/Noesis_OrigenX84/noesis_commander.py --interpreter python3 --name noesis_commander
pm2 start /Users/josemanuelmota/Noesis_OrigenX84/guardianes.py --interpreter python3 --name noesis_guard
pm2 start /Users/josemanuelmota/Noesis_OrigenX84/interface/noesis_ui.command --name noesis_ui --interpreter bash
pm2 start /Users/josemanuelmota/Noesis_OrigenX84/Orquestador/git_noesis_agent_dios.sh --name noesis_sync --interpreter bash

echo "🌀 Oráculo: Verificando estado del sistema..."
pm2 logs --lines 20

echo "✅ Todos los servicios esenciales están activados."

