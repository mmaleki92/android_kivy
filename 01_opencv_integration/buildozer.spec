[app]
title = KivyOpenCVCamera
package.name = kivyopencvcamera
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1,numpy,opencv-python-headless

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
# Add gradle options
android.gradle_dependencies = androidx.core:core:1.6.0, androidx.multidex:multidex:2.0.1
android.gradle_hook = app/build.gradle:repositories:mavenCentral(); maven { url 'https://maven.google.com' }
android.enable_androidx = True
android.extra_build_options = -PbuildDir=build/gradle
android.gradle_path = /usr/local/bin/gradle

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

[buildozer]
log_level = 2
warn_on_root = 1