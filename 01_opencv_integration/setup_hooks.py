# P4A hooks for OpenCV
import os
import shutil
import sys
import glob
from os.path import join, exists, basename

def before_apk_build(toolchain):
    print("Running pre-build hook for OpenCV integration...")
    
    # Create cv2_config directory if it doesn't exist
    os.makedirs('cv2_config', exist_ok=True)
    
    # Generate multiple config files with different names for different Python versions
    # OpenCV looks for config-{major}.{minor}.py or config-{major}.py
    
    config_content = """
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
if os.path.exists('/data/data/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/opencv_python_headless.libs'):
    BINARIES_PATHS.append('/data/data/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/opencv_python_headless.libs')

# Tell OpenCV where to find its native libraries
if hasattr(sys, 'getandroidapilevel'):
    ANDROID = True
else:
    ANDROID = False
"""

    # Create config files for different Python versions
    for version in ['3.11', '3']:
        config_file = f'cv2_config/config-{version}.py'
        with open(config_file, 'w') as f:
            f.write(config_content)
        print(f"Created {config_file}")
    
    # Also create standard config.py
    with open('cv2_config/config.py', 'w') as f:
        f.write(config_content)
    print("Created cv2_config/config.py")
    
    # Create an empty __init__.py to make it a proper package
    with open('cv2_config/__init__.py', 'w') as f:
        f.write("# OpenCV config package\n")
    
    # Now try to get the distribution directory and site-packages if possible
    try:
        # Get the distribution directory
        dist_dir = None
        if hasattr(toolchain, 'dist_dir'):
            dist_dir = toolchain.dist_dir
        elif hasattr(toolchain, 'ctx') and hasattr(toolchain, 'args'):
            dist_name = getattr(toolchain.args, 'dist_name', 'kivyopencvcamera')
            dist_dir = join(toolchain.ctx.dist_dir, dist_name)
        
        if dist_dir and exists(dist_dir):
            # Find the Python installation directory
            python_install_dir = join(dist_dir, 'python-installs', 'python3')
            if exists(python_install_dir):
                # Find site-packages
                for path in os.listdir(python_install_dir):
                    if path.endswith('-packages'):
                        site_packages = join(python_install_dir, path)
                        
                        # Create cv2 directory if needed
                        cv2_dir = join(site_packages, 'cv2')
                        os.makedirs(cv2_dir, exist_ok=True)
                        
                        # Copy all the config files to cv2 directory
                        for config_file in glob.glob('cv2_config/*.py'):
                            dest = join(cv2_dir, basename(config_file))
                            shutil.copy(config_file, dest)
                            print(f"Copied {config_file} to {dest}")
                        
                        break
    except Exception as e:
        print(f"Error while setting up OpenCV configs in site-packages: {str(e)}")
        import traceback
        print(traceback.format_exc())

def after_apk_build(toolchain):
    print("Running post-build hook for OpenCV integration...")
    # Nothing needed here for now
    pass