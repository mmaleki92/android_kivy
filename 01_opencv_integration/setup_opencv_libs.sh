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

# Clean up
rm -rf opencv.zip opencv-4.8.0-android-sdk

echo "OpenCV native libraries installed successfully"