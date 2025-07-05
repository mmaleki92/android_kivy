#!/bin/bash
set -e

echo "Setting up OpenCV configuration for the build..."

# Create directory for the config files
mkdir -p /tmp/opencv_config

# Generate the config files
cat > /tmp/opencv_config/config.py << 'EOF'
# OpenCV configuration file for Android
import os
import sys

# Platform detection
ANDROID = hasattr(sys, 'getandroidapilevel')

# Libraries setup
BINARIES_PATHS = []
HEADLESS = True
DEBUG = False
LOADER_PYTHON_VERSION = "{}.{}.{}".format(*sys.version_info[:3])

# Add paths to native libraries
if ANDROID:
    app_lib_path = '/data/data/org.example.kivyopencvcamera/files/app/lib'
    if os.path.exists(app_lib_path):
        BINARIES_PATHS.append(app_lib_path)
        
    usr_lib_path = '/data/user/0/org.example.kivyopencvcamera/files/app/lib'
    if os.path.exists(usr_lib_path):
        BINARIES_PATHS.append(usr_lib_path)
    
    bundle_path = '/data/user/0/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/cv2/libs'
    if os.path.exists(bundle_path):
        BINARIES_PATHS.append(bundle_path)
EOF

# Create version-specific config files
cp /tmp/opencv_config/config.py /tmp/opencv_config/config-3.py
cp /tmp/opencv_config/config.py /tmp/opencv_config/config-3.11.py

# Create empty __init__.py to make it a proper package
touch /tmp/opencv_config/__init__.py

echo "OpenCV configuration files created successfully"