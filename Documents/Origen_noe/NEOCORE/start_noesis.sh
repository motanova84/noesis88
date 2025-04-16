#!/bin/bash
# Script de inicio para NOESIS/NEOCORE

# Colores para salida
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==============================================${NC}"
echo -e "${BLUE}           INICIANDO SISTEMA NOESIS          ${NC}"
echo -e "${BLUE}==============================================${NC}"

# Verificar estructura de directorios
BASE_DIR=~/NEOCORE
MODULES=("core" "memory" "agents" "interface" "logs")

echo -e "${YELLOW}Verificando estructura de directorios...${NC}"

for module in "${MODULES[@]}"; do
    if [ ! -d "$BASE_DIR/$module" ]; then
        echo -e "${YELLOW}Creando directorio $module...${NC}"
        mkdir -p "$BASE_DIR/$module"
    fi
done

# Verificar archivo de memoria
if [ ! -f "$BASE_DIR/memory/memory_manager.py" ]; then
    echo -e "${YELLOW}Creando módulo de gestión de memoria...${NC}"
    
    # Crear módulo de memoria
    cat > "$BASE_DIR/memory/memory_manager.py" << 'EOL'
#!/usr/bin/env python3
# memory_manager.py - Gestor de memoria para NOESIS

import os
import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class MemoryManager:
    """Gestor de memoria para NOESIS"""
    
    def __init__(self, memory_dir: str = None):
        # Configurar directorio de memoria
        self.memory_dir = memory_dir or os.path.join(os.path.expanduser("~/NEOCORE"), "memory", "data")
        os.makedirs(self.memory_dir, exist_ok=True)
        
        # Inicializar logger
        self.logger = logging.getLogger("MemoryManager")
        
        # Cargar memorias existentes
        self.memories = self._load_memories()
        
        self.logger.info(f"Gestor de memoria inicializado. {len(self.memories)} memorias cargadas.")
    
    def _load_memories(self) -> Dict[str, Any]:
        """Carga memorias existentes desde disco"""
        memories = {}
        
        try:
            memory_index_path = os.path.join(self.memory_dir, "memory_index.json")
            if os.path.exists(memory_index_path):
                with open(memory_index_path, "r") as f:
                    memories = json.load(f)
        except Exception as e:
            self.logger.error(f"Error cargando memorias: {e}")
            # Crear índice vacío
            self._save_memory_index({})
        
        return memories
    
    def _save_memory_index(self, memories: Dict[str, Any] = None) -> None:
        """Guarda índice de memorias en disco"""
        if memories is None:
            memories = self.memories
            
        try:
            memory_index_path = os.path.join(self.memory_dir, "memory_index.json")
            with open(memory_index_path, "w") as f:
                json.dump(memories, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error guardando índice de memorias: {e}")
    
    def record_memory(self, content: str, category: str = "general", 
                     importance: float = 0.5, metadata: Dict[str, Any] = None) -> str:
        """Registra una nueva memoria"""
        # Generar ID único
        memory_id = f"mem_{int(time.time())}_{hash(content) % 10000}"
        
        # Crear entrada de memoria
        memory = {
            "id": memory_id,
            "content": content,
            "category": category,
            "importance": importance,
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "metadata": metadata or {},
            "access_count": 0,
            "last_access": None
        }
        
        # Guardar en índice
        self.memories[memory_id] = memory
        
        # Guardar índice actualizado
        self._save_memory_index()
        
        # Guardar contenido completo si es largo
        if len(content) > 500:
            self._save_memory_content(memory_id, content)
            # Truncar para el índice
            self.memories[memory_id]["content"] = content[:500] + "..."
            
        self.logger.info(f"Memoria registrada: {memory_id} ({category})")
        return memory_id
    
    def _save_memory_content(self, memory_id: str, content: str) -> None:
        """Guarda contenido completo de una memoria"""
        try:
            memory_path = os.path.join(self.memory_dir, f"{memory_id}.json")
            with open(memory_path, "w") as f:
                json.dump({"id": memory_id, "content": content}, f)
        except Exception as e:
            self.logger.error(f"Error guardando contenido de memoria {memory_id}: {e}")
    
    def retrieve_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """Recupera una memoria por su ID"""
        if memory_id not in self.memories:
            return None
            
        memory = self.memories[memory_id].copy()
        
        # Actualizar estadísticas de acceso
        self.memories[memory_id]["access_count"] += 1
        self.memories[memory_id]["last_access"] = time.time()
        
        # Cargar contenido completo si está truncado
        if memory["content"].endswith("..."):
            try:
                memory_path = os.path.join(self.memory_dir, f"{memory_id}.json")
                if os.path.exists(memory_path):
                    with open(memory_path, "r") as f:
                        full_content = json.load(f)
                        memory["content"] = full_content["content"]
            except Exception as e:
                self.logger.error(f"Error cargando contenido completo de {memory_id}: {e}")
        
        return memory
    
    def search_memories(self, query: str, category: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Busca memorias por contenido y categoría"""
        results = []
        
        for memory_id, memory in self.memories.items():
            # Filtrar por categoría si se especifica
            if category and memory["category"] != category:
                continue
                
            # Búsqueda simple por coincidencia de texto
            if query.lower() in memory["content"].lower():
                results.append(memory.copy())
        
        # Ordenar por importancia y fecha
        results.sort(key=lambda x: (x["importance"], x["timestamp"]), reverse=True)
        
        return results[:limit]
    
    def record_interaction(self, input_text: str, output_text: str, 
                         metadata: Dict[str, Any] = None) -> str:
        """Registra una interacción con el usuario"""
        content = f"Usuario: {input_text}\nSistema: {output_text}"
        return self.record_memory(content, category="interacción", 
                                metadata=metadata)
    
    def _calculate_memory_priority(self, text, categoria=None):
        """Calcula la prioridad (1-10) de una memoria"""
        # Prioridad base por categoría
        priority_map = {
            "sistema": 7,
            "acción": 8,
            "consulta": 5,
            "personal": 6,
            "general": 5
        }

        if categoria and categoria in priority_map:
            return priority_map[categoria]
        return 5

# Para pruebas independientes
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    memory = MemoryManager()
    memory.record_interaction("Hola, ¿cómo estás?", "Estoy bien, ¿en qué puedo ayudarte?")
    print("Prueba de memoria completada")
EOL
    
    # Crear archivo __init__.py en el directorio memory
    touch "$BASE_DIR/memory/__init__.py"
    
    echo -e "${GREEN}✓ Módulo de memoria creado${NC}"
fi

# Verificar archivo cerebro
if [ ! -f "$BASE_DIR/core/brain.py" ]; then
    echo -e "${YELLOW}Archivo cerebro no encontrado. Creando...${NC}"
    
    # Crear módulo cerebro
    cat > "$BASE_DIR/core/brain.py" << 'EOL'
#!/usr/bin/env python3
# brain.py - Cerebro central para NOESIS/NEOCORE

import os
import sys
import time
import logging
import json
from datetime import datetime
import asyncio
from typing import Dict, List, Any, Optional

# Configurar logging
log_dir = os.path.expanduser("~/NEOCORE/logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "noesis.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("NeoBrain")

# Añadir directorio principal al path
sys.path.insert(0, os.path.expanduser("~/NEOCORE"))

# Importar módulos
try:
    from memory.memory_manager import MemoryManager
    # Importar otros módulos cuando estén disponibles
    # from agents.agent_manager import AgentManager
    # from interface.cli import CommandLineInterface
except ImportError as e:
    logger.critical(f"Error crítico importando módulos: {e}")
    logger.critical("Verifica que los archivos estén en las ubicaciones correctas")
    sys.exit(1)

class NeoBrain:
    """Cerebro central de NOESIS/NEOCORE"""
    
    def __init__(self):
        self.name = "NOESIS"
        self.version = "0.1.0"
        self.start_time = datetime.now()
        self.active = False
        
        # Inicializar componentes
        self.memory = MemoryManager()
        # self.agents = AgentManager()
        # self.interface = CommandLineInterface(self)
        
        logger.info(f"{self.name} v{self.version} inicializado")
        
    async def start(self):
        """Inicia el sistema"""
        if self.active:
            logger.warning("El sistema ya está activo")
            return
            
        self.active = True
        self.memory.record_memory(
            f"Inicio del sistema {self.name} v{self.version}",
            category="sistema",
            importance=0.9
        )
        
        # Iniciar bucle principal
        await self._main_loop()
        
    async def stop(self):
        """Detiene el sistema"""
        if not self.active:
            logger.warning("El sistema no está activo")
            return
            
        self.active = False
        self.memory.record_memory(
            f"Detención del sistema {self.name} v{self.version}",
            category="sistema",
            importance=0.8
        )
        
        logger.info(f"{self.name} detenido correctamente")
        
    async def _main_loop(self):
        """Bucle principal de ejecución"""
        logger.info("Iniciando bucle principal...")
        
        try:
            while self.active:
                # Aquí irá la lógica principal cuando se implementen más componentes
                await self._process_cli()
                await asyncio.sleep(0.1)
        except KeyboardInterrupt:
            logger.info("Interrupción de teclado detectada")
        except Exception as e:
            logger.error(f"Error en bucle principal: {e}")
        finally:
            self.active = False
    
    async def _process_cli(self):
        """Procesa interacción por línea de comandos"""
        # Implementación simple para pruebas
        command = input("NOESIS> ")
        
        if command.lower() in ["salir", "exit", "quit"]:
            await self.stop()
            return
            
        if command.lower() == "ayuda":
            self._show_help()
            return
            
        if command.lower() == "status":
            await self._show_status()
            return
            
        if command.lower().startswith("tarea "):
            await self._create_task(command[6:])
            return
            
        print(f"*** Unknown syntax: {command}")
    
    def _show_help(self):
        """Muestra ayuda del sistema"""
        print("\nComandos disponibles:\n")
        print("status - Muestra el estado actual del sistema")
        print("iniciar [componente] - Inicia un componente (base, task, orchestrator)")
        print("detener [componente] - Detiene un componente (orchestrator)")
        print("tarea \"título\" \"descripción\" [prioridad] - Crea una nueva tarea")
        print("ayuda - Muestra esta ayuda")
        print("salir - Salir de NEOCORE CLI")
    
    async def _show_status(self):
        """Muestra estado del sistema"""
        uptime = datetime.now() - self.start_time
        hours, remainder = divmod(uptime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        print("\nEstado del sistema:")
        print(f"Nombre: {self.name}")
        print(f"Versión: {self.version}")
        print(f"Tiempo activo: {int(hours)}h {int(minutes)}m {int(seconds)}s")
        print(f"Memorias almacenadas: {len(self.memory.memories)}")
        print(f"Estado: {'Activo' if self.active else 'Inactivo'}")
    
    async def _create_task(self, task_str: str):
        """Crea una nueva tarea"""
        try:
            # Parsear: tarea "título" "descripción" [prioridad]
            parts = task_str.split('"')
            if len(parts) < 5:
                print("Error: Formato incorrecto. Uso: tarea \"título\" \"descripción\" [prioridad]")
                return
                
            title = parts[1]
            description = parts[3]
            
            # Parsear prioridad si existe
            priority = 5.0  # Valor por defecto
            if len(parts) > 4 and parts[4].strip():
                try:
                    priority_str = parts[4].strip()
                    priority = float(priority_str)
                except ValueError:
                    pass
            
            # Generar ID único
            task_id = f"task_{int(time.time())}_{hash(title) % 10000}"
            
            # Registrar tarea
            self.memory.record_memory(
                f"Tarea: {title}\nDescripción: {description}",
                category="tarea",
                importance=priority / 10.0,
                metadata={
                    "task_id": task_id,
                    "title": title,
                    "priority": priority,
                    "status": "pending"
                }
            )
            
            print(f"✓ Tarea creada: {task_id}")
            print(f"Título: {title}")
            print(f"Descripción: {description}")
            print(f"Prioridad: {priority}")
            
        except Exception as e:
            print(f"Error al crear tarea: {e}")

# Entrada principal
if __name__ == "__main__":
    try:
        brain = NeoBrain()
        asyncio.run(brain.start())
    except KeyboardInterrupt:
        print("\nSistema detenido por usuario")
    except Exception as e:
        logger.error(f"Error fatal: {e}")
EOL
    
    # Crear archivo __init__.py en el directorio core
    touch "$BASE_DIR/core/__init__.py"
    
    echo -e "${GREEN}✓ Módulo cerebro creado${NC}"
fi

# Ejecutar cerebro
echo -e "${BLUE}Iniciando sistema NOESIS...${NC}"
cd "$BASE_DIR" && python3 core/brain.py

exit 0
