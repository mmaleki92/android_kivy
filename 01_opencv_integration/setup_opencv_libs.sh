#!/bin/bash

# Create directories for native libraries
mkdir -p libs/arm64-v8a
mkdir -p libs/armeabi-v7a
mkdir -p libs/x86
mkdir -p libs/x86_64

# Download OpenCV Android SDK
wget -O opencv.zip https://github.com/opencv/opencv/releases/download/4.8.0/opencv-4.8.0-android-sdk.zip
unzip -q opencv.zip

# Copy the native libraries
cp -a opencv-4.8.0-android-sdk/sdk/native/libs/arm64-v8a/*.so libs/arm64-v8a/
cp -a opencv-4.8.0-android-sdk/sdk/native/libs/armeabi-v7a/*.so libs/armeabi-v7a/
cp -a opencv-4.8.0-android-sdk/sdk/native/libs/x86/*.so libs/x86/
cp -a opencv-4.8.0-android-sdk/sdk/native/libs/x86_64/*.so libs/x86_64/

# Create symbolic links if needed for easier finding
mkdir -p app/libs
ln -sf ../../libs/arm64-v8a app/libs/arm64-v8a
ln -sf ../../libs/armeabi-v7a app/libs/armeabi-v7a
ln -sf ../../libs/x86 app/libs/x86
ln -sf ../../libs/x86_64 app/libs/x86_64

# For debugging purposes, list all libraries that were copied
echo "Libraries copied to libs/arm64-v8a:"
ls -la libs/arm64-v8a/

echo "Libraries copied to libs/armeabi-v7a:"
ls -la libs/armeabi-v7a/

# Clean up
rm -rf opencv.zip opencv-4.8.0-android-sdk

echo "OpenCV native libraries installed successfully"   