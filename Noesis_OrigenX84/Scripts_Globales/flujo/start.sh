#!/bin/bash

# Script de inicio para NEOCORE PRO

# Colores para una mejor visualización
GREEN="[0;32m"
BLUE="[0;34m"
PURPLE="[0;35m"
CYAN="[0;36m"
RED="[0;31m"
NC="[0m" # No Color

# Banner de inicio
echo -e "${PURPLE}"
echo "███╗   ██╗███████╗ ██████╗  ██████╗ ██████╗ ██████╗ ███████╗   ██████╗ ██████╗  ██████╗ "
echo "████╗  ██║██╔════╝██╔═══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝   ██╔══██╗██╔══██╗██╔═══██╗"
echo "██╔██╗ ██║█████╗  ██║   ██║██║     ██║   ██║██████╔╝█████╗     ██████╔╝██████╔╝██║   ██║"
echo "██║╚██╗██║██╔══╝  ██║   ██║██║     ██║   ██║██╔══██╗██╔══╝     ██╔═══╝ ██╔══██╗██║   ██║"
echo "██║ ╚████║███████╗╚██████╔╝╚██████╗╚██████╔╝██║  ██║███████╗   ██║     ██║  ██║╚██████╔╝"
echo "╚═╝  ╚═══╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝   ╚═╝     ╚═╝  ╚═╝ ╚═════╝ "
echo -e "${NC}"
echo -e "${CYAN}Sistema de IA Autónomo de Nivel Empresarial${NC}"
echo

# Verificar dependencias
echo -e "${BLUE}Verificando dependencias...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}⚠️  Python3 no está instalado.${NC}"
    echo "Por favor, instala Python 3.8 o superior."
    exit 1
fi

# Verificar e instalar paquetes necesarios
echo -e "${BLUE}Verificando paquetes de Python...${NC}"
python3 -m pip install --upgrade pip
python3 -m pip install numpy

echo -e "${GREEN}✓ Dependencias básicas verificadas${NC}"

echo -e "
${BLUE}Estado de NEOCORE PRO:${NC}"
echo "- Kernel Neuronal: Implementado"
echo "- Sistema de Memoria Vectorial: Implementado"
echo "- Otros módulos: En desarrollo"

echo -e "
${CYAN}NEOCORE PRO está en fase de implementación.${NC}"
echo "Puedes ejecutar módulos individuales para probarlos. Por ejemplo:"
echo "python3 ~/NEOCORE_PRO/core/neuralsystem/neural_kernel.py"

echo -e "
${GREEN}Preparación completada.${NC}"
