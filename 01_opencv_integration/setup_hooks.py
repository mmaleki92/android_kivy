# P4A hooks for OpenCV
import os
import shutil
import glob
from os.path import join, exists, basename

def before_apk_build(context):
    print("Running pre-build hook for OpenCV integration...")
    # Check for OpenCV configuration
    site_packages = context.site_packages_dir
    
    # Create cv2 directory if needed
    cv2_dir = os.path.join(site_packages, "cv2")
    os.makedirs(cv2_dir, exist_ok=True)
    
    # Copy config.py to cv2 directory
    if os.path.exists("cv2_config/config.py"):
        shutil.copy("cv2_config/config.py", os.path.join(cv2_dir, "config.py"))
        print("Copied config.py to cv2 directory")
    else:
        print("Warning: config.py not found in cv2_config directory")

def after_apk_build(context):
    print("Running post-build hook for OpenCV integration...")
    # Nothing needed here for now
    pass