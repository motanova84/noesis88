#!/bin/bash

WATCH_DIR="/mnt/data/autonomos/pendientes"
REPO_DIR="/mnt/data/noesis88"
LOG_FILE="$REPO_DIR/logs/log_comandos_noe.log"
BITACORA="/mnt/data/bitacora_origen.md"

inotifywait -m -e close_write "$WATCH_DIR" --format '%w%f' | while read FILE
do
    FILENAME=$(basename "$FILE")
    DEST="$REPO_DIR/data_auto/$FILENAME"

    echo "🛰️ Subiendo $FILENAME al repositorio..."
    cp "$FILE" "$DEST"

    echo "- [$FILENAME] subido a GitHub por Noé — $(date)" >> "$LOG_FILE"
    echo "- [$FILENAME] subido a GitHub por Noé — $(date)" >> "$BITACORA"

    cd "$REPO_DIR"
    git add .
    git commit -m "📦 Auto-upload: $FILENAME"
    git push origin main
done
