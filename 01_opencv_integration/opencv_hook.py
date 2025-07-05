"""
P4A hook to install OpenCV configuration files
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
    else:
        print("WARNING: Could not find _python_bundle directory")
        
    if not site_packages:
        print("WARNING: Could not find site-packages directory")
        return False
    
    # Create cv2 directory if it doesn't exist
    cv2_dir = join(site_packages, 'cv2')
    os.makedirs(cv2_dir, exist_ok=True)
    
    # Copy config files from our temporary directory
    config_src_dir = '/tmp/opencv_config'
    if exists(config_src_dir):
        for filename in os.listdir(config_src_dir):
            src_file = join(config_src_dir, filename)
            dst_file = join(cv2_dir, filename)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dst_file)
                print(f"Copied {filename} to {dst_file}")
    else:
        print(f"ERROR: Config directory not found: {config_src_dir}")
        return False
    
    print("OpenCV configuration installed successfully")
    return True

def after_apk_build(toolchain):
    # Nothing to do here
    pass