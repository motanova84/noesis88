#!/bin/bash
NEOCORE_PATH="$HOME/NEOCORE"

# Colores para salida
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Mensaje de bienvenida
echo -e "${GREEN}Bienvenido a NEOCORE - IA Local para macOS${NC}"
echo -e "${CYAN}Cargando módulos...${NC}"

# Lanzar módulos en segundo plano
python3 "$NEOCORE_PATH/core/memory_manager.py" &
MEM_PID=$!
sleep 1
echo -e "${CYAN}✓ Memoria cargada (PID: $MEM_PID)${NC}"

python3 "$NEOCORE_PATH/core/brain.py" &
BRAIN_PID=$!
sleep 1
echo -e "${CYAN}✓ Módulo cerebral operativo (PID: $BRAIN_PID)${NC}"

python3 "$NEOCORE_PATH/core/action_executor.py" &
EXEC_PID=$!
sleep 1
echo -e "${CYAN}✓ Ejecutor de acciones activo (PID: $EXEC_PID)${NC}"

# Bucle principal de comandos
echo -e "${YELLOW}NEOCORE está listo. Escribe un comando o 'salir' para terminar.${NC}"
while true; do
    echo -n -e "${BLUE}Tú:${NC} "
    read -r input
    [[ "$input" == "salir" ]] && echo -e "${CYAN}Cerrando NEOCORE...${NC}" && kill $MEM_PID $BRAIN_PID $EXEC_PID 2>/dev/null && exit 0
    echo "$input" | ollama run llama3
    echo
done
