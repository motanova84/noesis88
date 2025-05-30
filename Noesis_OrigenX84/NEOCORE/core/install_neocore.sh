#!/bin/bash
# install.sh - Instalador completo de NEOCORE

# Colores para una mejor visualización
RED='\033[0;31m'
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
echo -e "${CYAN}Iniciando instalación...${NC}\n"

# Crear estructura de directorios
echo -e "${BLUE}[1/7]${NC} Creando estructura de directorios..."
mkdir -p ~/NEOCORE/{core,actions,memory,setup,config}
sleep 1
echo -e "${GREEN}✓ Estructura de directorios creada${NC}\n"

# Verificar e instalar dependencias
echo -e "${BLUE}[2/7]${NC} Verificando dependencias..."

if ! command -v brew &> /dev/null; then
    echo -e "${CYAN}Instalando Homebrew...${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${CYAN}Instalando Python...${NC}"
    brew install python
fi

if ! command -v ollama &> /dev/null; then
    echo -e "${CYAN}Instalando Ollama...${NC}"
    brew install ollama
fi

echo -e "${CYAN}Instalando paquetes de Python...${NC}"
pip3 install numpy pandas scikit-learn sentence-transformers sqlite3 psutil requests apscheduler
sleep 1
echo -e "${GREEN}✓ Dependencias instaladas${NC}\n"

# Descargar modelo de IA
echo -e "${BLUE}[3/7]${NC} Descargando modelo de IA (Llama3)..."
ollama pull llama3
sleep 1
echo -e "${GREEN}✓ Modelo de IA descargado${NC}\n"

# Configurar scripts del núcleo
echo -e "${BLUE}[4/7]${NC} Configurando núcleo del sistema..."

# Crear script principal de NEOCORE
echo -e "${CYAN}Creando script principal 'neocore.sh'...${NC}"
cat > ~/NEOCORE/core/neocore.sh << 'EOF'
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
EOF
chmod +x ~/NEOCORE/core/neocore.sh

# Finalización
echo -e "\n${GREEN}✓ Instalación completa.${NC}"
echo -e "${YELLOW}Para iniciar NEOCORE, ejecuta:${NC}"
echo -e "bash ~/NEOCORE/core/neocore.sh"

