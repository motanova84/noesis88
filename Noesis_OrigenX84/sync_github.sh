#!/bin/bash

echo "🔄 Sincronizando cambios locales con GitHub..."

cd ~/Noesis_OrigenX84 || exit

# Añadir todos los cambios
git add .

# Commit automático con fecha y hora
git commit -m "🔄 Sync automático - $(date '+%Y-%m-%d %H:%M:%S')"

# Subida al repositorio
git push origin main

echo "✅ Sincronización completada."

