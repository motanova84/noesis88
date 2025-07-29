# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
# 🜂 Activado a 141.70001 Hz – QCAL ∞³
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗃️ NOESIS · BACKUP DIARIO ZIP · versión 1.0
Guarda una copia comprimida diaria del proyecto Noesis
"""

import os
from datetime import datetime
import zipfile

# === Configuración ===
FOLDER_ORIGEN = os.path.expanduser("~/Proyectos/Noesis_OrigenX84")
FOLDER_DESTINO = os.path.expanduser("~/Proyectos/BackupsNoesis")

# === Timestamp ===
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d_%H%M")
zip_filename = os.path.join(FOLDER_DESTINO, f"noesis_backup_{timestamp}.zip")

# === Crear ZIP ===
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(FOLDER_ORIGEN):
        for file in files:
            if "venv_noe" in root or "sync_logs.txt" in file:
                continue  # Omitimos entornos virtuales y logs
            ruta_completa = os.path.join(root, file)
            ruta_relativa = os.path.relpath(ruta_completa, FOLDER_ORIGEN)
            zipf.write(ruta_completa, arcname=ruta_relativa)

print(f"✅ Backup creado: {zip_filename}")

