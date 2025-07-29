#!/bin/bash

# Configuración
REPO_DIR="/mnt/data/noesis88"
LOGS_DIR="$REPO_DIR/logs"
SOURCE_DIR="/mnt/data/autonomos/pendientes"
BITACORA="/mnt/data/bitacora_origen.md"

# Asegurar que estamos en el directorio correcto
cd "$REPO_DIR" || {
    echo "❌ Error: No se pudo acceder al directorio $REPO_DIR"
    exit 1
}

# Crear directorio de logs si no existe
mkdir -p "$LOGS_DIR"

# Generar archivo de identidad
IDENTITY_FILE="$LOGS_DIR/neo_identidad.md"
echo "# Identidad de Noesis" > "$IDENTITY_FILE"
echo "" >> "$IDENTITY_FILE"
echo "Fecha de actualización: $(date)" >> "$IDENTITY_FILE"
echo "" >> "$IDENTITY_FILE"
echo "## Archivos generados" >> "$IDENTITY_FILE"
ls -lt "$SOURCE_DIR" | head -n 10 | awk '{print "- " $9 " (" $6 " " $7 " " $8 ")"}' >> "$IDENTITY_FILE"

# Generar log de comandos
LOG_FILE="$LOGS_DIR/log_comandos_noe.log"
echo "=== Log de comandos de Noesis ===" > "$LOG_FILE"
echo "Generado el: $(date)" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
