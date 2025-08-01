#!/usr/bin/env python3
import time

def main():
    print("[NOESIS | EXECUTOR] Módulo de acciones activo.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[NOESIS | EXECUTOR] Detenido por el usuario.")

if __name__ == "__main__":
    main()
