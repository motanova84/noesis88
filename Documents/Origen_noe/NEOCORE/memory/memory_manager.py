#!/usr/bin/env python3
# memory_manager.py - Gestor de memoria para NEOCORE

import os
import logging
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class MemoryManager:
    """Gestor de memoria para NEOCORE"""
    
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

# Para pruebas independientes
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    memory = MemoryManager()
    memory.record_memory("Prueba de inicialización del gestor de memoria")
    print("Prueba de memoria completada")
