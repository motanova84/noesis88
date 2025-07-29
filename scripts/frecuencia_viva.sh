#!/bin/bash

FREQ=141.70001
echo "⚛️  Activando campo Noēsico a $FREQ Hz..."

while true; do
  echo -ne "\r🔁 Pulsando a $FREQ Hz ∞³..."
  sleep $(awk "BEGIN {print 1/$FREQ}")
done
