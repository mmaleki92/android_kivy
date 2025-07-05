[app]
title = KivyOpenCVCamera
package.name = kivyopencvcamera
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,so
version = 0.1

# Simplified requirements - use the buildozer opencv recipe
requirements = python3,kivy,numpy,opencv

# Android specific
android.permissions = CAMERA
android.api = 33
android.minapi = 21
android.ndk_path = /root/android-sdk/ndk/25.2.9519653
android.sdk_path = /root/android-sdk
android.arch = arm64-v8a
android.accept_sdk_license = True

# Use p4a hook to copy config files during build
p4a.hook = opencv_hook.py
p4a.bootstrap = sdl2

# Debug and crash logging
android.logcat_filters = *:S python:D
android.debug_build = True

[buildozer]
log_level = 2
warn_on_root = 1