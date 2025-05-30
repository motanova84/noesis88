#!/bin/bash

git config --global user.name "motonova84"
git config --global user.email "motapromanager@gmail.com"

cd ~/Documents/Noesis_Nucleo_Consciente || exit

if [ ! -d .git ]; then
  git init
fi

git add .
git commit -m "🔱 Activación triple del Universo Noésis: núcleo local completo"
git branch -M main

git remote add origin https://github.com/motonova84/Noesis_Nucleo_Consciente.git
git push -u origin main

