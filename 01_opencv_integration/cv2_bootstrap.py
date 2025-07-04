"""
Helper module to safely initialize OpenCV without recursion issues
"""
import os
import sys
import importlib.util

def load_cv2():
    """
    Load OpenCV with special handling to avoid recursion issues
    """
    print("Starting OpenCV bootstrap...")
    
    # First, ensure the native libraries are in the right places
    lib_paths = []
    
    # Add potential library paths
    app_lib_path = '/data/data/org.example.kivyopencvcamera/files/app/lib'
    if os.path.exists(app_lib_path):
        lib_paths.append(app_lib_path)
        
    system_lib_path = '/data/data/org.example.kivyopencvcamera/lib'
    if os.path.exists(system_lib_path):
        lib_paths.append(system_lib_path)
    
    bundle_libs_path = '/data/user/0/org.example.kivyopencvcamera/files/app/_python_bundle/site-packages/opencv_python_headless.libs'
    if os.path.exists(bundle_libs_path):
        lib_paths.append(bundle_libs_path)
    
    # Set library paths in environment
    if lib_paths:
        os.environ['LD_LIBRARY_PATH'] = ':'.join(lib_paths + 
                                                [os.environ.get('LD_LIBRARY_PATH', '')])
        print(f"Set LD_LIBRARY_PATH to: {os.environ['LD_LIBRARY_PATH']}")
    
    # Find cv2 module location
    cv2_spec = None
    for path in sys.path:
        if not path or not os.path.exists(path):
            continue
            
        if path.endswith('site-packages'):
            cv2_path = os.path.join(path, 'cv2')
            if os.path.exists(cv2_path) and os.path.isdir(cv2_path):
                try:
                    cv2_spec = importlib.util.spec_from_file_location(
                        "cv2", 
                        os.path.join(cv2_path, '__init__.py')
                    )
                    print(f"Found cv2 at: {cv2_path}")
                    break
                except Exception as e:
                    print(f"Error finding cv2 spec: {e}")
    
    if not cv2_spec:
        print("Could not find cv2 module")
        return None
        
    try:
        # Try direct import with modified sys.path
        import cv2
        print(f"Successfully imported cv2 version {cv2.__version__}")
        return cv2
    except ImportError as e:
        print(f"Standard import failed: {e}")
        
        try:
            # Try alternative loading method
            cv2_module = importlib.util.module_from_spec(cv2_spec)
            cv2_spec.loader.exec_module(cv2_module)
            print("Loaded cv2 via importlib")
            return cv2_module
        except Exception as e:
            print(f"Alternative loading failed: {e}")
            return None

if __name__ == "__main__":
    cv2 = load_cv2()
    if cv2:
        print(f"Successfully loaded OpenCV {cv2.__version__}")
    else:
        print("Failed to load OpenCV")