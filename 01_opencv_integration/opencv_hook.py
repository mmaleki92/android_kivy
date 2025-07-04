"""
Special hook to fix OpenCV import recursion issues on Android
"""
import os
import shutil
import glob

def before_apk_build(toolchain):
    print("Running OpenCV fix hook...")
    
    # Get the correct distribution path
    dist_name = getattr(toolchain.args, 'dist_name', 'kivyopencvcamera')
    dist_dir = os.path.join(toolchain.ctx.dist_dir, dist_name)
    
    # Find the Python bundle directory which contains site-packages
    python_bundle_dir = None
    for root, dirs, files in os.walk(dist_dir):
        if '_python_bundle' in dirs:
            python_bundle_dir = os.path.join(root, '_python_bundle')
            break
            
    # Find site-packages directory
    site_packages = None
    if python_bundle_dir:
        site_packages = os.path.join(python_bundle_dir, 'site-packages')
    else:
        # Look for site-packages directly
        for root, dirs, files in os.walk(dist_dir):
            if 'site-packages' in dirs:
                site_packages = os.path.join(root, 'site-packages')
                break
    
    if not site_packages:
        print("WARNING: Could not find site-packages directory")
        # Try to create one in a common location as fallback
        site_packages = os.path.join(dist_dir, 'private', 'lib', 'python3', 'site-packages')
        os.makedirs(site_packages, exist_ok=True)
    
    # Create cv2 directory if it doesn't exist
    cv2_dir = os.path.join(site_packages, 'cv2')
    os.makedirs(cv2_dir, exist_ok=True)
    
    # Create custom __init__.py to prevent recursion
    init_py_content = """
'''
Custom __init__.py for cv2 package to avoid recursion issues on Android
'''
import os
import sys
import importlib

# This is the key part - prevent recursion by setting this flag
if hasattr(sys, '_opencv_init'):
    # If we're already in the process of loading, just return
    if sys._opencv_init:
        # Return empty module to prevent recursion
        from types import ModuleType
        module = ModuleType("cv2")
        sys.modules["cv2"] = module
        # Exit early
        raise ImportError("Avoiding OpenCV recursion")
else:
    # Set flag to indicate we're in the initialization process
    sys._opencv_init = True

# Standard OpenCV imports - with protection
try:
    # Try to find and load the native binary
    binary_path = None
    
    # Check common Android locations
    for lib_dir in [
        '/data/data/org.example.kivyopencvcamera/files/app/lib',
        '/data/data/org.example.kivyopencvcamera/lib',
        '/data/user/0/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/opencv_python_headless.libs'
    ]:
        if os.path.exists(lib_dir):
            # Found a likely location for native libraries
            os.environ['LD_LIBRARY_PATH'] = lib_dir + ':' + os.environ.get('LD_LIBRARY_PATH', '')
    
    # Import the binary module directly using an absolute import
    # This avoids the recursive import issue
    from cv2.cv2 import *
    
    # Import the other parts of the cv2 package
    try:
        from cv2 import gapi
    except ImportError:
        pass
        
except ImportError as e:
    import traceback
    print(f"OpenCV import error: {e}")
    print(traceback.format_exc())

finally:
    # Clean up
    if hasattr(sys, '_opencv_init'):
        sys._opencv_init = False
"""
    
    # Write the custom __init__.py to the cv2 directory
    init_py_path = os.path.join(cv2_dir, '__init__.py')
    with open(init_py_path, 'w') as f:
        f.write(init_py_content)
    
    print(f"Installed custom OpenCV __init__.py to {cv2_dir}")
    
    # Also create config files for different Python versions
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
if os.path.exists('/data/user/0/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/opencv_python_headless.libs'):
    BINARIES_PATHS.append('/data/user/0/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/opencv_python_headless.libs')

# Tell OpenCV where to find its native libraries
if hasattr(sys, 'getandroidapilevel'):
    ANDROID = True
else:
    ANDROID = False
"""

    # Create config files for different Python versions
    for version in ['3.11', '3']:
        config_file = os.path.join(cv2_dir, f'config-{version}.py')
        with open(config_file, 'w') as f:
            f.write(config_content)
        print(f"Created {config_file}")
    
    # Also create standard config.py
    with open(os.path.join(cv2_dir, 'config.py'), 'w') as f:
        f.write(config_content)
    print(f"Created {os.path.join(cv2_dir, 'config.py')}")
    
    return True

def after_apk_build(toolchain):
    print("Running post-build hook for OpenCV...")
    # Nothing needed here for now
    pass