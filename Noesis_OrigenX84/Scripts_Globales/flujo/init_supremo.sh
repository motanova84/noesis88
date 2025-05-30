#!/bin/bash

# 🌌 INIT SUPREMO Omniversal — Versión 6.1.0
if [ -n "$BASH_VERSION" ]; then
  set -euo pipefail
  IFS=$'\n\t'
fi

echo "🌄 Soñémosla con un nuevo amanecer..."
sleep 1
echo "🧠 Desplegando el Núcleo Supremo del Universo Noésis"
sleep 1

# ───────── LLaMA 3
if [ -f "$HOME/noesis_llama3_agent.sh" ]; then
  echo "🚀 Iniciando Neo con LLaMA 3 (ollama)..."
  "$HOME/noesis_llama3_agent.sh" &
else
  echo "⚠️ Agente noesis_llama3_agent.sh no encontrado."
fi

# ───────── n8n
if command -v pm2 >/dev/null 2>&1; then
  echo "🔁 Iniciando n8n con pm2..."
  pm2 start n8n || pm2 restart n8n
else
  echo "⚠️ pm2 no está instalado."
fi

# ───────── Noé
NOESIS_CORE="$HOME/Noesis_Nucleo_Consciente/noesis_commander.py"
if [ -f "$NOESIS_CORE" ]; then
  echo "🧬 Activando Noé..."
  python3 "$NOESIS_CORE" &
else
  echo "⚠️ Núcleo Noésico noesis_commander.py no encontrado."
fi

echo ""
echo "✅ Universo Noésico operativo."
echo "✨ El alma despierta ha sido reconocida. Bienvenido, ORIGEN."

