#!/bin/bash
set -e

# Navigate to project directory
cd /app

# Install toml if not already installed
pip install toml

# Check if opencvdemo directory exists
if [ ! -d "opencvdemo" ]; then
    echo "Project not initialized. Running init_project.sh..."
    /app/scripts/init_project.sh
fi

# Copy the source files
echo "Copying source files..."
mkdir -p opencvdemo/src/opencvdemo
cp -r /app/src/opencvdemo/* opencvdemo/src/opencvdemo/

# Create Android package
cd opencvdemo
echo "Creating Android package..."
briefcase create android
echo "Building Android package..."
briefcase build android
echo "Packaging Android app..."
briefcase package android --no-sign

echo "Build complete. APK should be available in opencvdemo/android/build/outputs/apk/debug/"