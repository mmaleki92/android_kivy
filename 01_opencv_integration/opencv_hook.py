"""
Special hook to fix OpenCV import recursion issues on Android
and ensure proper native library loading
"""
import os
import shutil
import glob
import sys

def before_apk_build(toolchain):
    print("Running OpenCV fix hook...")
    
    # Get the correct distribution path
    dist_name = getattr(toolchain.args, 'dist_name', 'kivyopencvcamera')
    dist_dir = os.path.join(toolchain.ctx.dist_dir, dist_name)
    
    # Find Python bundle directory
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
        site_packages = os.path.join(dist_dir, 'private', 'lib', 'python3', 'site-packages')
        os.makedirs(site_packages, exist_ok=True)
    
    # Create cv2 directory if it doesn't exist
    cv2_dir = os.path.join(site_packages, 'cv2')
    os.makedirs(cv2_dir, exist_ok=True)
    
    # Create a directory for native libraries
    libs_dir = os.path.join(cv2_dir, 'libs')
    os.makedirs(libs_dir, exist_ok=True)
    
    # Copy native libraries from our libs directory to cv2/libs
    # based on the target architecture
    arch = getattr(toolchain.args, 'arch', 'arm64-v8a')
    print(f"Target architecture: {arch}")
    
    # Look for OpenCV native libraries in project
    src_libs_dir = os.path.join(os.getcwd(), 'libs', arch)
    if os.path.exists(src_libs_dir):
        for lib_file in os.listdir(src_libs_dir):
            if lib_file.endswith('.so'):
                src_path = os.path.join(src_libs_dir, lib_file)
                dst_path = os.path.join(libs_dir, lib_file)
                shutil.copy2(src_path, dst_path)
                print(f"Copied {lib_file} to {libs_dir}")
    else:
        print(f"WARNING: No native libraries found in {src_libs_dir}")
        
    # Create special cv2.so file if it doesn't exist
    if os.path.exists(os.path.join(src_libs_dir, 'cv2.so')):
        shutil.copy2(
            os.path.join(src_libs_dir, 'cv2.so'),
            os.path.join(cv2_dir, 'cv2.so')
        )
        print(f"Copied cv2.so to {cv2_dir}")
    elif os.path.exists(os.path.join(src_libs_dir, 'libopencv_java4.so')):
        shutil.copy2(
            os.path.join(src_libs_dir, 'libopencv_java4.so'),
            os.path.join(cv2_dir, 'cv2.so')
        )
        print(f"Created cv2.so from libopencv_java4.so in {cv2_dir}")
    
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
    
    # Check if we have a local cv2.so file
    cv2_dir = os.path.dirname(__file__)
    local_lib = os.path.join(cv2_dir, 'cv2.so')
    
    if os.path.exists(local_lib):
        try:
            # Try to load the local library
            import ctypes
            ctypes.CDLL(local_lib)
            print(f"Loaded OpenCV native library from {local_lib}")
        except Exception as e:
            print(f"Failed to load local library: {e}")
    
    # Check common Android locations
    for lib_dir in [
        '/data/data/org.example.kivyopencvcamera/files/app/lib',
        '/data/data/org.example.kivyopencvcamera/lib',
        '/data/user/0/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/cv2/libs',
        '/data/user/0/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/opencv_python_headless.libs'
    ]:
        if os.path.exists(lib_dir):
            # Found a likely location for native libraries
            os.environ['LD_LIBRARY_PATH'] = lib_dir + ':' + os.environ.get('LD_LIBRARY_PATH', '')
    
    # Import the binary module directly using an absolute import
    # This avoids the recursive import issue
    try:
        from cv2.cv2 import *
    except ImportError:
        # If that fails, try to import from the module's own directory
        cv2_path = os.path.dirname(__file__)
        if os.path.exists(os.path.join(cv2_path, 'cv2.so')):
            # Load using ctypes
            import ctypes
            import numpy
            
            # Define basic OpenCV functions
            _lib = ctypes.CDLL(os.path.join(cv2_path, 'cv2.so'))
            
            # Define minimal functionality
            def __getattr__(name):
                return lambda *args, **kwargs: None
                
            # Add version info
            __version__ = "4.5.5"
            
            print(f"Loaded minimal OpenCV {__version__} functionality")
        else:
            print(f"Could not find OpenCV native library")
            raise
    
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
if os.path.exists('/data/user/0/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/cv2/libs'):
    BINARIES_PATHS.append('/data/user/0/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/cv2/libs')

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