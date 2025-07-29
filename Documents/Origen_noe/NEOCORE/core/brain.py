# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
#!/usr/bin/env python3
# brain.py - Cerebro central para NEOCORE

import os
import json
import time
import datetime
import subprocess
import threading
import logging
import sys
import re
from pathlib import Path

# Configurar logging
log_dir = os.path.expanduser("~/NEOCORE/logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "brain.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("NeoBrain")

# Añadir NEOCORE al path para importaciones
sys.path.append(os.path.expanduser("~/NEOCORE"))

# Importar módulos NEOCORE
try:
    from memory.memory_manager import MemoryManager
    from actions.action_executor import ActionExecutor
except ImportError as e:
    logger.critical(f"Error crítico importando módulos: {e}")
    logger.critical("Verifica que los archivos estén en las ubicaciones correctas")
    sys.exit(1)

class NeoBrain:
    """
    Núcleo cognitivo central del sistema NEOCORE.
    Coordina memoria, acciones y procesamiento de IA.
    """
    
    def __init__(self):
        logger.info("Iniciando NeoBrain...")
        
        # Inicializar componentes clave
        self.memory = MemoryManager()
        self.executor = ActionExecutor()
        
        # Estado del cerebro
        self.estado = "activo"
        self.ultima_interaccion = None
        self.contexto_actual = {}
        self.historial_interacciones = []
        
        # Cargar configuración del cerebro
        self.config = self._load_config()
        
        # Controlar si Ollama está disponible
        self.ollama_available = self._check_ollama()
        
        logger.info(f"NeoBrain iniciado correctamente. Ollama disponible: {self.ollama_available}")
    
    def _load_config(self):
        """Carga la configuración del cerebro o crea una por defecto"""
        config_path = os.path.expanduser("~/NEOCORE/config/brain_config.json")
        
        # Configuración por defecto
        default_config = {
            "version": "1.0",
            "modelo_ia": "llama3",
            "temperatura": 0.7,
            "max_tokens": 500,
            "modo_respuesta": "conciso",
            "seguridad": True,
            "comandos_permitidos": ["abrir_app", "crear_nota", "buscar_archivo", 
                                    "obtener_estado", "captura_pantalla"]
        }
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.info("Configuración cargada correctamente")
                return config
            else:
                # Crear configuración predeterminada
                os.makedirs(os.path.dirname(config_path), exist_ok=True)
                with open(config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                logger.info("Configuración predeterminada creada")
                return default_config
        except Exception as e:
            logger.error(f"Error cargando configuración: {e}")
            return default_config
    
    def _check_ollama(self):
        """Verifica si Ollama está instalado y disponible"""
        try:
            subprocess.run(["ollama", "--version"], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE,
                          check=True)
            return True
        except:
            logger.warning("Ollama no está disponible. Funcionamiento limitado.")
            return False
    
    def process(self, input_text):
        """
        Procesa la entrada del usuario y genera una respuesta
        Este es el método principal que maneja toda la lógica
        """
        start_time = time.time()
        self.ultima_interaccion = datetime.datetime.now()
        
        # Registrar la interacción en el historial local
        self.historial_interacciones.append({
            "timestamp": self.ultima_interaccion.isoformat(),
            "input": input_text,
            "response": None
        })
        
        # Analizar la entrada para detectar comandos
        action_result = self._detect_and_execute_action(input_text)
        
        # Si se detectó y ejecutó una acción, usar su resultado
        if action_result:
            response = action_result
        else:
            # Si no hay acción, procesar con IA
            response = self._generate_ai_response(input_text)
        
        # Actualizar la respuesta en el historial
        self.historial_interacciones[-1]["response"] = response
        
        # Registrar en el sistema de memoria
        self.memory.record_interaction(input_text, response)
        
        # Actualizar contexto actual
        self._update_context(input_text, response)
        
        # Calcular tiempo de respuesta
        processing_time = time.time() - start_time
        logger.info(f"Respuesta generada en {processing_time:.2f} segundos")
        
        return response
    
    def _detect_and_execute_action(self, text):
        """Detecta si el texto contiene una acción para ejecutar"""
        
        # Patrones de acción (simplificados)
        action_patterns = [
            (r'\b(abre|abrir|ejecuta|ejecutar|lanza|lanzar)\s+(?:la\s+)?(?:app|aplicación)?\s+([a-zA-Z0-9 ]+)', 
             lambda m: self.executor.execute_action("abrir_app", m.group(2).strip())),
            
            (r'\b(crea|crear|guarda|guardar|nueva|nuevo)\s+(?:una\s+)?nota\s+(?:que\s+diga\s+)?["\']?([^"\']+)["\']?', 
             lambda m: self.executor.execute_action("crear_nota", m.group(2).strip())),
            
            (r'\b(busca|buscar|encuentra|encontrar)\s+(?:el\s+)?(?:archivo|fichero)s?\s+([a-zA-Z0-9 ]+)', 
             lambda m: self.executor.execute_action("buscar_archivo", m.group(2).strip())),
            
            (r'\b(estado|status)\s+(?:del\s+)?sistema', 
             lambda m: self.executor.execute_action("obtener_estado")),
            
            (r'\b(captura|screenshot|pantallazo|tomar\s+foto)\b', 
             lambda m: self.executor.execute_action("captura_pantalla")),
            
            (r'\b(recordatorio|recuérdame|recuerdame)\s+(?:en\s+)?(\d+)?\s*(?:minutos?)?\s+([^,\.]+)', 
             lambda m: self.executor.execute_action("establecer_recordatorio", 
                                                   m.group(3).strip(), 
                                                   int(m.group(2)) if m.group(2) else 5))
        ]
        
        # Verificar cada patrón
        for pattern, action_function in action_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    result = action_function(match)
                    logger.info(f"Acción ejecutada: {pattern}")
                    return f"✓ {result}"
                except Exception as e:
                    logger.error(f"Error ejecutando acción: {e}")
                    return f"Error ejecutando la acción: {e}"
        
        return None
    
    def _generate_ai_response(self, input_text):
        """Genera una respuesta usando IA local (Ollama)"""
        if not self.ollama_available:
            return "No puedo generar una respuesta inteligente porque Ollama no está disponible. Por favor instala Ollama para habilitar la IA local."
        
        try:
            # Mejorar el prompt con contexto
            if len(self.historial_interacciones) > 1:
                prompt = self._create_contextualized_prompt(input_text)
            else:
                prompt = f"Eres NEOCORE, un asistente IA local en un Mac. Responde de forma concisa a: {input_text}"
            
            # Enviar a Ollama
            modelo = self.config.get("modelo_ia", "llama3")
            comando = ["ollama", "run", modelo, prompt]
            
            result = subprocess.run(comando, 
                                   capture_output=True, 
                                   text=True, 
                                   timeout=10)
            
            if result.returncode != 0:
                logger.error(f"Error de Ollama: {result.stderr}")
                return "Lo siento, hubo un error generando la respuesta."
            
            return result.stdout.strip()
            
        except subprocess.TimeoutExpired:
            logger.warning("Timeout esperando respuesta de Ollama")
            return "La generación de respuesta tomó demasiado tiempo. Por favor intenta de nuevo."
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            return f"Error al procesar la consulta: {str(e)}"
    
    def _create_contextualized_prompt(self, input_text):
        """Crea un prompt contextualizado con historia reciente"""
        history_context = ""
        
        # Añadir hasta 3 interacciones recientes para contexto
        recent_history = self.historial_interacciones[-4:-1]  # Excluye la actual
        for item in recent_history:
            history_context += f"Usuario: {item['input']}\n"
            if item['response']:
                history_context += f"NEOCORE: {item['response']}\n"
        
        # Construir el prompt completo
        prompt = f"""Eres NEOCORE, un asistente IA local que funciona en un Mac.
Contexto de conversación reciente:
{history_context}

Usuario: {input_text}
NEOCORE:"""
        
        return prompt
    
    def _update_context(self, input_text, response):
        """Actualiza el contexto actual basado en la interacción"""
        # Simplemente guardamos algunos datos básicos por ahora
        self.contexto_actual = {
            "ultima_entrada": input_text,
            "ultima_respuesta": response,
            "timestamp": datetime.datetime.now().isoformat(),
            "num_interacciones": len(self.historial_interacciones)
        }

# Para ejecución directa
if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════╗")
    print("║  NEOCORE - Sistema IA Local para macOS   ║")
    print("╚══════════════════════════════════════════╝\n")
    
    brain = NeoBrain()
    print("NeoBrain inicializado. Escribe 'salir' para terminar.\n")
    
    while True:
        try:
            user_input = input("👤 Tú: ")
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("Cerrando NEOCORE...")
                break
                
            response = brain.process(user_input)
            print(f"🤖 NEO: {response}\n")
            
        except KeyboardInterrupt:
            print("\nSesión terminada por el usuario.")
            break
        except Exception as e:
            print(f"Error: {e}")
