[app]
title = KivyOpenCVCamera
package.name = kivyopencvcamera
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,so
version = 0.1
# Use a specific version of opencv-python-headless that is known to work better on Android
requirements = python3,kivy==2.2.1,numpy==1.22.4,opencv-python-headless==4.5.5.64

# Android specific
android.permissions = CAMERA
android.api = 33
android.minapi = 21
android.ndk_path = /root/android-sdk/ndk/25.2.9519653
android.sdk_path = /root/android-sdk
android.arch = arm64-v8a
android.accept_sdk_license = True

# Critical: Include the OpenCV .so files properly
android.enable_androidx = True
android.add_libs_armeabi_v7a = libs/armeabi-v7a/*.so
android.add_libs_arm64_v8a = libs/arm64-v8a/*.so
android.add_libs_x86 = libs/x86/*.so
android.add_libs_x86_64 = libs/x86_64/*.so

# Explicitly add OpenCV dependencies
android.gradle_dependencies = androidx.core:core:1.8.0, androidx.multidex:multidex:2.0.1

# Use p4a hooks to copy config files during build
p4a.hook = opencv_hook.py
p4a.bootstrap = sdl2

# Debug and crash logging
android.logcat_filters = *:S python:D
android.debug_build = True

[buildozer]
log_level = 2
warn_on_root = 1