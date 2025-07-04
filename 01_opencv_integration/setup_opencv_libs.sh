#!/bin/bash
set -e  # Exit on error

echo "Setting up OpenCV native libraries..."

# Create directories for native libraries
mkdir -p libs/arm64-v8a
mkdir -p libs/armeabi-v7a
mkdir -p libs/x86
mkdir -p libs/x86_64

# Download OpenCV Android SDK - use version 4.5.5 to match the Python package
echo "Downloading OpenCV Android SDK..."
wget -O opencv.zip https://github.com/opencv/opencv/releases/download/4.5.5/opencv-4.5.5-android-sdk.zip
unzip -q opencv.zip

# Use a version of OpenCV that matches our Python package (4.5.5)
echo "Copying native libraries..."
cp -v opencv-4.5.5-android-sdk/sdk/native/libs/arm64-v8a/*.so libs/arm64-v8a/
cp -v opencv-4.5.5-android-sdk/sdk/native/libs/armeabi-v7a/*.so libs/armeabi-v7a/
cp -v opencv-4.5.5-android-sdk/sdk/native/libs/x86/*.so libs/x86/
cp -v opencv-4.5.5-android-sdk/sdk/native/libs/x86_64/*.so libs/x86_64/

# Also create a simple opencv_libs directory that can be included in the APK
mkdir -p opencv_libs
cp -v opencv-4.5.5-android-sdk/sdk/native/libs/arm64-v8a/*.so opencv_libs/

# For debugging purposes, list all libraries that were copied
echo "Libraries copied to libs/arm64-v8a:"
ls -la libs/arm64-v8a/

# Clean up
rm -rf opencv.zip opencv-4.5.5-android-sdk

echo "OpenCV native libraries installed successfully"