#!/usr/bin/env python3
import os
import shutil
import urllib.request
import zipfile
import sys

def download_opencv_android():
    """Download and extract OpenCV Android SDK"""
    print("Downloading OpenCV Android SDK...")
    
    # Create directories for native libraries
    os.makedirs('libs/arm64-v8a', exist_ok=True)
    os.makedirs('libs/armeabi-v7a', exist_ok=True)
    os.makedirs('libs/x86', exist_ok=True)
    os.makedirs('libs/x86_64', exist_ok=True)
    
    # Download OpenCV Android SDK version 4.5.5 to match the Python package
    opencv_url = "https://github.com/opencv/opencv/releases/download/4.5.5/opencv-4.5.5-android-sdk.zip"
    zip_file = "opencv-android-sdk.zip"
    
    try:
        # Download the file if it doesn't exist
        if not os.path.exists(zip_file):
            print(f"Downloading from {opencv_url}...")
            urllib.request.urlretrieve(opencv_url, zip_file)
        
        # Extract the ZIP file
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall("opencv-android-temp")
        
        # Copy the .so files to the libs directory
        sdk_path = "opencv-android-temp/OpenCV-android-sdk/sdk/native/libs"
        for arch in ['arm64-v8a', 'armeabi-v7a', 'x86', 'x86_64']:
            src_dir = os.path.join(sdk_path, arch)
            dst_dir = os.path.join('libs', arch)
            
            if os.path.exists(src_dir):
                for file in os.listdir(src_dir):
                    if file.endswith('.so'):
                        src_file = os.path.join(src_dir, file)
                        dst_file = os.path.join(dst_dir, file)
                        shutil.copy2(src_file, dst_file)
                        print(f"Copied {src_file} to {dst_file}")
        
        # Create a special wrapper for cv2.so
        for arch in ['arm64-v8a', 'armeabi-v7a', 'x86', 'x86_64']:
            # Create a symbolic link or copy libopencv_java4.so to cv2.so
            src_file = os.path.join('libs', arch, 'libopencv_java4.so')
            if os.path.exists(src_file):
                dst_file = os.path.join('libs', arch, 'cv2.so')
                shutil.copy2(src_file, dst_file)
                print(f"Created cv2.so for {arch}")
            
        print("OpenCV native libraries installed successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if download_opencv_android():
        print("Success!")
    else:
        print("Failed to download OpenCV libraries")
        sys.exit(1)