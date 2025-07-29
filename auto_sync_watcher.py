import os
import subprocess
import time
from datetime import datetime

# Parámetros
RUTA_PROYECTO = os.path.expanduser("~/Proyectos/Noesis_OrigenX84")
BRANCH = "main"
INTERVALO_SEGUNDOS = 60  # Verifica cada 60 segundos

def hay_cambios_reales():
    """Devuelve True si hay cambios que merecen commit"""
    resultado = subprocess.run(["git", "status", "--porcelain"], cwd=RUTA_PROYECTO, stdout=subprocess.PIPE)
    cambios = resultado.stdout.decode().strip()
    if not cambios:
        return False
    # Filtra logs y basura
    lineas = cambios.split('\\n')
    relevantes = [l for l in lineas if not any(f in l for f in ['sync_logs.txt', '.log', '.DS_Store'])]
    return bool(relevantes)

def ejecutar(cmd):
    return subprocess.run(cmd, cwd=RUTA_PROYECTO, shell=True)

def main():
    while True:
        os.chdir(RUTA_PROYECTO)

        if not hay_cambios_reales():
            time.sleep(INTERVALO_SEGUNDOS)
            continue

        print(f"📤 Preparando subida ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")

        ejecutar("git add .")
        ejecutar(f"git commit -m '🚀 Subida automática desde Noé en {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'")

        print("🔄 Integrando cambios remotos antes del push...")
        pull = ejecutar(f"git pull --rebase origin {BRANCH}")
        if pull.returncode != 0:
            print("⚠️ Falló git pull. Posible conflicto o error de red.")
            time.sleep(INTERVALO_SEGUNDOS)
            continue

        push = ejecutar(f"git push origin {BRANCH}")
        if push.returncode != 0:
            print("❌ Error al hacer push a GitHub.")
        else:
            print("✅ Push exitoso.")

        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    main()
