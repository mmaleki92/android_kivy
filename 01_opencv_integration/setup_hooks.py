# P4A hooks for OpenCV
import os
import shutil
import glob
from os.path import join, exists, basename

def before_apk_build(toolchain):
    print("Running pre-build hook for OpenCV integration...")
    
    # Get the distribution directory
    dist_dir = toolchain.dist_dir if hasattr(toolchain, 'dist_dir') else None
    if not dist_dir and hasattr(toolchain, 'args'):
        dist_name = getattr(toolchain.args, 'dist_name', 'kivyopencvcamera')
        arch = getattr(toolchain.args, 'arch', 'arm64-v8a')
        dist_dir = join(toolchain.ctx.dist_dir, dist_name)
    
    if not dist_dir or not exists(dist_dir):
        print("Warning: Could not find distribution directory")
        # Create cv2_config directory if it doesn't exist
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
        return
    
    # Find the site-packages directory in the Python installation
    python_install_dir = join(dist_dir, 'python-installs', 'python3')
    if not exists(python_install_dir):
        print(f"Warning: Python installation dir not found at {python_install_dir}")
        return
    
    site_packages = None
    for path in os.listdir(python_install_dir):
        if path.endswith('-packages'):
            site_packages = join(python_install_dir, path)
            break
    
    if site_packages is None:
        print("Warning: Could not find site-packages directory")
        return
    
    # Create cv2 directory if needed
    cv2_dir = os.path.join(site_packages, "cv2")
    os.makedirs(cv2_dir, exist_ok=True)
    print(f"Created/Verified cv2 directory at {cv2_dir}")
    
    # Copy config.py to cv2 directory
    if os.path.exists("cv2_config/config.py"):
        shutil.copy("cv2_config/config.py", os.path.join(cv2_dir, "config.py"))
        print(f"Copied config.py to {os.path.join(cv2_dir, 'config.py')}")
    else:
        print("Warning: config.py not found in cv2_config directory")
        # Create config.py file directly in cv2 directory
        with open(os.path.join(cv2_dir, 'config.py'), 'w') as f:
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
            print("Generated new config.py file directly in cv2 directory")
            
    # Create an empty __init__.py in the cv2 directory if it doesn't exist
    init_file = os.path.join(cv2_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# CV2 package\n')
        print("Created __init__.py in cv2 directory")

def after_apk_build(toolchain):
    print("Running post-build hook for OpenCV integration...")
    # Nothing needed here for now
    pass