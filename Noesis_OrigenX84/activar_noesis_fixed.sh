#!/bin/bash

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RESET='\033[0m'

# Directorio base
BASE_DIR="/Users/josemanuelmota/Noesis_OrigenX84"
cd "$BASE_DIR"

echo -e "${BLUE}🔧 Limpiando procesos anteriores...${RESET}"
pm2 delete all 2>/dev/null
pm2 kill 2>/dev/null

echo -e "${BLUE}🚀 Iniciando módulos principales...${RESET}"

# 1. Iniciar noesis_commander
pm2 start noesis_commander.py \
    --interpreter python3 \
    --name noesis_commander \
    --max-restarts 3

# 2. NO iniciar guardianes.py - tiene errores

# 3. NO iniciar git_noesis_agent_dios.sh automáticamente
# Este script debe ejecutarse MANUALMENTE cuando quieras sincronizar

echo -e "${GREEN}✅ Sistema iniciado correctamente${RESET}"
echo -e "${BLUE}📝 Para sincronizar con GitHub, ejecuta manualmente:${RESET}"
echo -e "   ${GREEN}./git_noesis_agent_dios.sh${RESET}"

pm2 status
