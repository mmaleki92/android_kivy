"""
P4A hook to create and install OpenCV configuration files
"""
import os
import shutil
from os.path import join, exists

def before_apk_build(toolchain):
    print("Running OpenCV configuration hook...")
    
    # Get the correct distribution path
    dist_name = getattr(toolchain.args, 'dist_name', 'kivyopencvcamera')
    dist_dir = join(toolchain.ctx.dist_dir, dist_name)
    
    # Find Python bundle directory
    python_bundle_dir = None
    for root, dirs, files in os.walk(dist_dir):
        if '_python_bundle' in dirs:
            python_bundle_dir = join(root, '_python_bundle')
            break
    
    # Find site-packages directory
    site_packages = None
    if python_bundle_dir:
        site_packages = join(python_bundle_dir, 'site-packages')
        print(f"Found site-packages at: {site_packages}")
    else:
        print("WARNING: Could not find _python_bundle directory")
        
    if not site_packages:
        print("WARNING: Could not find site-packages directory")
        return False
    
    # Create cv2 directory if it doesn't exist
    cv2_dir = join(site_packages, 'cv2')
    os.makedirs(cv2_dir, exist_ok=True)
    
    # Generate config file content
    config_content = """
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
"""
    
    # Write the config files directly
    # Main config file
    with open(join(cv2_dir, 'config.py'), 'w') as f:
        f.write(config_content)
    print(f"Created {join(cv2_dir, 'config.py')}")
    
    # Version-specific config files
    with open(join(cv2_dir, 'config-3.py'), 'w') as f:
        f.write(config_content)
    print(f"Created {join(cv2_dir, 'config-3.py')}")
    
    with open(join(cv2_dir, 'config-3.11.py'), 'w') as f:
        f.write(config_content)
    print(f"Created {join(cv2_dir, 'config-3.11.py')}")
    
    # Create empty __init__.py
    with open(join(cv2_dir, '__init__.py'), 'w') as f:
        f.write("# OpenCV package init\n")
    print(f"Created {join(cv2_dir, '__init__.py')}")
    
    print("OpenCV configuration setup completed successfully")
    return True

def after_apk_build(toolchain):
    # Nothing to do here
    pass