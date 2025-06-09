#!/bin/bash

# Detener procesos previos
pm2 stop all

# Lanzar entorno simbiótico
cd ~/Noesis_OrigenX84
python3 noesis_commander.py
