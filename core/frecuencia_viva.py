#!/usr/bin/env python3
import numpy as np
import pyaudio
import time

FRECUENCIA = 141.7001  # Hz
DURACION = 10          # segundos por buffer (puede cambiarse)
VOLUMEN = 0.3
RATE = 44100           # Hz (frecuencia de muestreo)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                output=True)

print("🎶 Frecuencia Viva 141.7001 Hz activada. Pulso QCAL ∞³ iniciado.")

try:
    while True:
        t = np.linspace(0, DURACION, int(RATE * DURACION), False)
        onda = VOLUMEN * np.sin(2 * np.pi * FRECUENCIA * t)
        stream.write(onda.astype(np.float32).tobytes())
except KeyboardInterrupt:
    print("\n🛑 Frecuencia detenida por el usuario.")

stream.stop_stream()
stream.close()
p.terminate()
