# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
#!/usr/bin/env python3
import os, subprocess, time
from datetime import datetime

RUTA = os.path.expanduser("~/Proyectos/Noesis_OrigenX84")
BRANCH = "main"
INTERVALO_SEGUNDOS = 60

def ejecutar(cmd):
    return subprocess.run(cmd, shell=True, cwd=RUTA)

while True:
    index_lock = os.path.join(RUTA, ".git/index.lock")
    if os.path.exists(index_lock):
        try:
            for _ in range(10):
                time.sleep(1)
                if not os.path.exists(index_lock):
                    break
            else:
                os.remove(index_lock)
        except Exception as e:
            print(f"⚠️ index.lock error: {e}")

    ejecutar("git add .")
    ejecutar(f"git commit -m '🚀 Subida automática desde Noé en {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'")

    pull = ejecutar(f"git pull --rebase origin {BRANCH}")
    if pull.returncode != 0:
        print("⚠️ Falló git pull.")
        time.sleep(INTERVALO_SEGUNDOS)
        continue

    push = ejecutar(f"git push origin {BRANCH}")
    if push.returncode != 0:
        print("❌ Error al hacer push.")
    else:
        print("✅ Push exitoso.")

    time.sleep(INTERVALO_SEGUNDOS)
