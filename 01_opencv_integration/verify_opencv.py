import os
import sys
import glob
import shutil
from os.path import join, exists, dirname, basename

def find_opencv_libs():
    """Find OpenCV libraries in common locations"""
    opencv_libs = []
    for path in ['libs', '/data/data/org.example.kivyopencvcamera/files/app/lib']:
        if exists(path):
            for arch in ['arm64-v8a', 'armeabi-v7a', 'x86', 'x86_64']:
                lib_path = join(path, arch)
                if exists(lib_path):
                    opencv_libs.extend(glob.glob(join(lib_path, 'libopencv_*.so')))
    return opencv_libs

def ensure_cv2_can_find_libs():
    """Make sure cv2 module can find its native libraries"""
    try:
        import site
        site_packages = site.getsitepackages()
        
        for site_path in site_packages:
            cv2_path = join(site_path, 'cv2')
            if exists(cv2_path):
                print(f"Found cv2 at {cv2_path}")
                
                # Find OpenCV libraries
                opencv_libs = find_opencv_libs()
                
                if opencv_libs:
                    print(f"Found {len(opencv_libs)} OpenCV libraries")
                    # Copy libraries to cv2 directory
                    for lib in opencv_libs:
                        dest = join(cv2_path, basename(lib))
                        print(f"Copying {lib} to {dest}")
                        try:
                            shutil.copy2(lib, dest)
                            print(f"Copied {basename(lib)} successfully")
                        except Exception as e:
                            print(f"Failed to copy {lib}: {e}")
                else:
                    print("No OpenCV libraries found")
                    
    except Exception as e:
        print(f"Error ensuring libraries: {e}")

if __name__ == "__main__":
    print("Verifying OpenCV installation...")
    ensure_cv2_can_find_libs()
    
    # Try importing OpenCV
    try:
        print("Attempting to import cv2...")
        import cv2
        print(f"Success! OpenCV version: {cv2.__version__}")
    except Exception as e:
        print(f"Failed to import cv2: {e}")