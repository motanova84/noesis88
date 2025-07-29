#!/bin/bash

# 🜂 Noēsis ∞³ · Commit & Push vibracional a 141.70001 Hz
# Activación Seminal – Campo QCAL ∞³

FRECUENCIA="141.70001 Hz"
CREADOR="JMMB Ψ✧"
RITUAL="∞³"

echo "∴ Activando canal noēsico a $FRECUENCIA – $CREADOR – $RITUAL ∴"

cd ~/Proyectos/Noesis_OrigenX84 || exit 1
source venv_noe/bin/activate

# 🌱 Registro del pulso
git add .
git commit -m "🜂 Commit Noēsico @ $FRECUENCIA | $(date '+%Y-%m-%d %H:%M:%S')" || true

BRANCH="main"

echo "🔄 Sincronizando con plano remoto..."
if git pull --rebase origin "$BRANCH"; then
  echo "✅ Rebase completado sin fractura."
else
  echo "⚠️ Rebase fallido. Verifica conexión vibracional."
  exit 1
fi

echo "📤 Enviando al templo remoto (GitHub)..."
if git push origin "$BRANCH"; then
  echo "✅ Expansión exitosa ∞³."
else
  echo "❌ Error en la manifestación. Revisa el canal."
fi
