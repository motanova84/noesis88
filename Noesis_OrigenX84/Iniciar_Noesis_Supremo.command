#!/bin/zsh
export PATH="/opt/homebrew/bin:$PATH"
cd /Users/josemanuelmota/Noesis_OrigenX84
pm2 start all
/opt/homebrew/bin/python3 noesis_commander_origen.py

