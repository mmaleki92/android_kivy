#!/bin/bash
set -e

cd /app/opencvdemo

if [ "$1" == "emulator" ]; then
    echo "Running on emulator..."
    briefcase run android -d emulator
else
    echo "Running on connected device..."
    briefcase run android
fi