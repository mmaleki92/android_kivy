# Create a custom config.py file for OpenCV
import os
import sys

# Get the site-packages directory
site_packages = None
for p in sys.path:
    if p.endswith('site-packages'):
        site_packages = p
        break

if site_packages:
    # Create cv2 directory if it doesn't exist
    cv2_dir = os.path.join(site_packages, 'cv2')
    os.makedirs(cv2_dir, exist_ok=True)
    
    # Create the config.py file
    config_file = os.path.join(cv2_dir, 'config.py')
    with open(config_file, 'w') as f:
        f.write("""
# Auto-generated config.py for OpenCV on Android
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
    print(f"Created OpenCV config.py at {config_file}")