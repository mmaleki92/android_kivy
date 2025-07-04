"""
Custom __init__.py for cv2 package to avoid recursion issues on Android
"""
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