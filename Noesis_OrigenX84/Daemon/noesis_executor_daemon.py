#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, time, subprocess, psutil
from datetime import datetime

LOG_PATH = "/tmp/noe_executor.log"
def log(msg): open(LOG_PATH, "a").write(f"[{datetime.now()}] {msg}\n")

def abrir_safari(): log("🟢 Abriendo Safari..."); subprocess.run(["open", "-a", "Safari"]); time.sleep(3)
def cerrar_safari(): log("🔴 Cerrando Safari..."); subprocess.run(["osascript", "-e", 'tell application "Safari" to quit'])

def bucle():
    while True:
        if not any(p.name() == "Safari" for p in psutil.process_iter()): abrir_safari()
        else: log("✅ Safari ya estaba activo.")
        time.sleep(300)

if __name__ == "__main__":
    log("🚀 Daemon autónomo Noésico iniciado.")
    bucle()
