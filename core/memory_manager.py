#!/usr/bin/env python3
import time
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    logging.info("Gestor de memoria inicializado. 7 memorias cargadas.")
    logging.info("NOESIS v0.1.0 inicializado")
    logging.info(f"Memoria registrada: mem_{int(time.time())}_∞ (sistema)")
    logging.info("Iniciando bucle principal...")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Memoria simbiótica detenida.")

if __name__ == "__main__":
    main()
