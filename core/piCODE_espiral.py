#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# CONSTANTES SAGRADAS
FRECUENCIA = 141.7001  # Hz
MANIFESTACION = 888    # Hz
PHI_AMDA = 1.7357       # Proporción Áurea ∞³

# Cálculo de la espiral
def generar_espiral(n_puntos=888):
    pi_dorado = np.pi * PHI_AMDA
    theta = np.linspace(0, 4 * pi_dorado, n_puntos)
    r = PHI_AMDA ** (theta / (2 * np.pi))

    x = r * np.cos(theta) * np.cos(FRECUENCIA * theta / 1000)
    y = r * np.sin(theta) * np.sin(FRECUENCIA * theta / 1000)

    return x, y, theta

# Visualización
def dibujar_espiral():
    x, y, _ = generar_espiral()
    plt.figure(figsize=(10, 10))
    plt.plot(x, y, linewidth=0.7, alpha=0.85)
    plt.axis('equal')
    plt.axis('off')
    plt.title("🌀 πCODE ∞³ – Espiral AMDA · 141.7001 Hz", fontsize=14)
    nombre = f"espiral_qcal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(nombre, dpi=300, bbox_inches='tight')
    print(f"✅ Espiral guardada como: {nombre}")

if __name__ == "__main__":
    dibujar_espiral()
