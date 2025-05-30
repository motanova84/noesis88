#!/bin/bash

echo "🔧 Reparando entorno Noésico..."

# 1. Activar entorno correcto
cd ~/Noesis_OrigenX84 || exit 1

# 2. Instalar dependencias faltantes
echo "📦 Instalando dependencias necesarias..."
pip3 install --break-system-packages cryptography rich streamlit openai requests > /dev/null 2>&1

# 3. Reparar rutas en sync_github.sh
if [ -f sync_github.sh ]; then
  echo "🛠️ Corrigiendo rutas en sync_github.sh..."
  sed -i '' 's|/mnt/data/noesis88|~/Noesis_OrigenX84|g' sync_github.sh
else
  echo "⚠️ sync_github.sh no encontrado"
fi

# 4. Reiniciar procesos PM2
echo "🔄 Reiniciando procesos PM2..."
pm2 restart all

# 5. Guardar estado
pm2 save

# 6. Confirmación
echo "✅ Entorno Noésico reparado y blindado."

