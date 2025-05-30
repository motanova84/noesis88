#!/bin/bash

cd ~/Documents/Origen_noe/NEOCORE

echo "🔄 Sincronizando con GitHub remoto..."

git config --global user.name "motanova84"
git config --global user.email "motapromanager@gmail.com"

git pull origin main --allow-unrelated-histories --no-rebase

git add .

NOW=$(date +"%Y-%m-%d %H:%M:%S")
git commit -m "🧠 Auto-commit desde script | $NOW"

git push origin main --force

echo "✅ Repositorio sincronizado con éxito 💫"

