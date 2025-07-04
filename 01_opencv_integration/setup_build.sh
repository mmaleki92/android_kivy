#!/bin/bash
set -e

echo "Setting up environment for OpenCV on Android..."

# Make scripts executable
chmod +x download_opencv_libs.py

# Download OpenCV native libraries
echo "Downloading OpenCV native libraries..."
./download_opencv_libs.py

# Make sure opencv_hook.py is available
if [ ! -f opencv_hook.py ]; then
    echo "Error: opencv_hook.py not found!"
    exit 1
fi

echo "Setup complete! Now run:"
echo "docker-compose -f docker-compose.build.yml up --build"