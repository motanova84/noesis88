#!/bin/bash

# === NEXUS PRIME v4.9.2 - LIMPIEZA LOCAL ===
clear
echo "🧬 NEXUS PRIME v4.9.2 - LIMPIEZA DEL SISTEMA"
echo "========================================="
echo "📅 Fecha: $(date)"
echo ""

# Limpiar archivos temporales
echo "🧹 Limpiando archivos temporales..."
NOESIS_DIR="$HOME/Documents/Noesis_Clean/noesis88"
find "$NOESIS_DIR" -name "*.pyc" -delete 2>/dev/null || true
find "$NOESIS_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$NOESIS_DIR" -name ".DS_Store" -delete 2>/dev/null || true
find "$NOESIS_DIR" -name "*.log" -type f -mtime +7 -delete 2>/dev/null || true

# Limpiar caché de pip
echo "🧹 Limpiando caché de pip..."
python3 -m pip cache purge 2>/dev/null || true

# Reiniciar procesos PM2
echo "🔄 Reiniciando procesos PM2..."
pm2 restart all 2>/dev/null || true

# Limpiar logs antiguos
echo "🧹 Limpiando logs antiguos..."
find "$HOME" -name "nexus_*.log" -type f -mtime +7 -delete 2>/dev/null || true

echo ""
echo "✅ Limpieza completada exitosamente"
