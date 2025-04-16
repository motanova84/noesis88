#!/bin/bash

echo "🌀 Iniciando sincronización automática con GitHub..."
cd ~/Documents/noesis_agent

# Resolver conflictos antes de intentar push
git pull --rebase origin main

git add .
git commit -m "🤖 Sync automático desde PM2"
git push origin main
echo "✅ Sincronización completada."
