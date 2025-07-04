[app]
title = KivyOpenCVCamera
package.name = kivyopencvcamera
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1,numpy,opencv-python-headless==4.8.0.76

# Android specific
android.permissions = CAMERA
android.api = 33
android.minapi = 21
android.ndk = 25.2.9519653
android.sdk = 33
android.sdk_path = /root/android-sdk
android.ndk_path = /root/android-sdk/ndk/25.2.9519653
android.arch = arm64-v8a
android.accept_sdk_license = True

# Important: Add these lines for OpenCV
android.enable_androidx = True
android.gradle_dependencies = androidx.core:core:1.8.0, androidx.multidex:multidex:2.0.1
android.add_libs_armeabi_v7a = libs/armeabi-v7a/*.so
android.add_libs_arm64_v8a = libs/arm64-v8a/*.so
android.add_libs_x86 = libs/x86/*.so
android.add_libs_x86_64 = libs/x86_64/*.so

# Debug and crash logging
android.logcat_filters = *:S python:D
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1