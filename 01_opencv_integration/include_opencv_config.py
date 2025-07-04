"""
This script ensures that OpenCV's config.py is included in the APK
Run this before building the APK
"""
import os
import sys
import shutil
from pathlib import Path

def create_opencv_config():
    """Create a config.py file for OpenCV to use in the APK"""
    # Create directory for OpenCV config
    os.makedirs('cv2_config', exist_ok=True)
    
    # Create config.py file
    with open('cv2_config/config.py', 'w') as f:
        f.write("""
# OpenCV configuration file for Android
import os
import sys

BINARIES_PATHS = []
HEADLESS = True
DEBUG = False
LOADER_PYTHON_VERSION = '{}.{}.{}'.format(*sys.version_info[:3])

# Native libraries for Android
if os.path.exists('/data/data/org.example.kivyopencvcamera/files/app/lib'):
    BINARIES_PATHS.append('/data/data/org.example.kivyopencvcamera/files/app/lib')
if os.path.exists('/data/data/org.example.kivyopencvcamera/lib'):
    BINARIES_PATHS.append('/data/data/org.example.kivyopencvcamera/lib')

# Tell OpenCV where to find its native libraries
if hasattr(sys, 'getandroidapilevel'):
    ANDROID = True
else:
    ANDROID = False
""")

    print("Created OpenCV config.py in cv2_config directory")
    
    # Create an empty __init__.py to make it a proper package
    with open('cv2_config/__init__.py', 'w') as f:
        f.write("# OpenCV config package\n")

if __name__ == "__main__":
    create_opencv_config()
    print("OpenCV configuration files created successfully")