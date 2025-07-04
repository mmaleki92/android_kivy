"""
Special hook to fix OpenCV import recursion issues on Android
"""
import os
import shutil

def before_apk_build(toolchain):
    print("Running OpenCV fix hook...")
    
    # Directory where the cv2 module will be installed
    site_packages = os.path.join(
        toolchain.dist_dir, 
        toolchain.bootstrap.distribution.name, 
        "_python_bundle", 
        "site-packages"
    )
    cv2_dir = os.path.join(site_packages, "cv2")
    
    # Create the directory if it doesn't exist
    os.makedirs(cv2_dir, exist_ok=True)
    
    # Copy our custom __init__.py to the cv2 package
    with open(os.path.join("cv2_init.py"), "r") as f:
        init_content = f.read()
        
    with open(os.path.join(cv2_dir, "__init__.py"), "w") as f:
        f.write(init_content)
    
    print(f"Installed custom OpenCV __init__.py to {cv2_dir}")
    
    return True