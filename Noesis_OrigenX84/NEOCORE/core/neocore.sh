#!/bin/bash

# NEOCORE - Sistema IA Local para macOS
# Script de inicio principal

# Colores para una mejor visualización
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner de inicio
echo -e "${PURPLE}"
echo "███╗   ██╗███████╗ ██████╗  ██████╗ ██████╗ ██████╗ ███████╗"
echo "████╗  ██║██╔════╝██╔═══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝"
echo "██╔██╗ ██║█████╗  ██║   ██║██║     ██║   ██║██████╔╝█████╗  "
echo "██║╚██╗██║██╔══╝  ██║   ██║██║     ██║   ██║██╔══██╗██╔══╝  "
echo "██║ ╚████║███████╗╚██████╔╝╚██████╗╚██████╔╝██║  ██║███████╗"
echo "╚═╝  ╚═══╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"
echo -e "${NC}"
echo -e "${CYAN}Sistema Autónomo de IA para macOS${NC}"
echo

# Verificar Ollama
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}⚠️  Ollama no está instalado en el sistema.${NC}"
    echo "Puedes instalarlo con: brew install ollama"
    echo "La funcionalidad de IA estará limitada sin Ollama."
    echo
fi

# Verificar si el modelo está descargado
if command -v ollama &> /dev/null; then
    echo -e "${BLUE}Verificando modelo de IA...${NC}"
    if ! ollama list | grep -q "llama3"; then
        echo -e "${CYAN}Descargando modelo Llama3 (esto puede tardar varios minutos)...${NC}"
        ollama pull llama3
    else
        echo -e "${GREEN}✓ Modelo llama3 ya está disponible${NC}"
    fi
fi

# Verificar Python y dependencias
echo -e "${BLUE}Verificando instalación de Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}⚠️  Python3 no está instalado.${NC}"
    echo "Puedes instalarlo con: brew install python"
    exit 1
else
    echo -e "${GREEN}✓ Python3 está instalado${NC}"
fi

# Iniciar NEOCORE
echo -e "\n${BLUE}Iniciando NEOCORE...${NC}"
cd ~/NEOCORE
python3 ~/NEOCORE/core/brain.py

# El script terminará cuando el usuario salga del cerebro
echo -e "\n${GREEN}NEOCORE cerrado correctamente.${NC}"
