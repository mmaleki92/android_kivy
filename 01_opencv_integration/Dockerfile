FROM ubuntu:20.04

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME="/root/android-sdk"
ENV ANDROID_SDK_ROOT="/root/android-sdk"
ENV ANDROID_NDK_HOME="${ANDROID_HOME}/ndk/25.2.9519653"
ENV PATH="${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:${ANDROID_NDK_HOME}"

# Install Java 17 from PPA
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common && \
    add-apt-repository -y ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-17-jdk \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    build-essential \
    git \
    wget \
    unzip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    libltdl-dev \
    zip \
    curl \
    lbzip2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME for Java 17
ENV JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"

# Install buildozer and cython
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir buildozer==1.5.0 Cython==0.29.33

# Create app directory
WORKDIR /app

# Setup directories for OpenCV libraries and create placeholder files
RUN mkdir -p libs/arm64-v8a libs/armeabi-v7a libs/x86 libs/x86_64 && \
    touch libs/arm64-v8a/libopencv_core.so && \
    touch libs/arm64-v8a/libopencv_imgproc.so && \
    touch libs/arm64-v8a/libopencv_imgcodecs.so && \
    touch libs/arm64-v8a/libopencv_calib3d.so && \
    cp libs/arm64-v8a/* libs/armeabi-v7a/ && \
    cp libs/arm64-v8a/* libs/x86/ && \
    cp libs/arm64-v8a/* libs/x86_64/

# Create OpenCV config directory and file
RUN mkdir -p cv2_config && \
    echo '# OpenCV configuration file for Android' > cv2_config/config.py && \
    echo 'import os' >> cv2_config/config.py && \
    echo 'import sys' >> cv2_config/config.py && \
    echo '' >> cv2_config/config.py && \
    echo 'BINARIES_PATHS = []' >> cv2_config/config.py && \
    echo 'HEADLESS = True' >> cv2_config/config.py && \
    echo 'DEBUG = False' >> cv2_config/config.py && \
    echo 'LOADER_PYTHON_VERSION = "{}.{}.{}".format(*sys.version_info[:3])' >> cv2_config/config.py && \
    echo '' >> cv2_config/config.py && \
    echo '# Native libraries for Android' >> cv2_config/config.py && \
    echo 'if os.path.exists("/data/data/org.example.kivyopencvcamera/files/app/lib"):' >> cv2_config/config.py && \
    echo '    BINARIES_PATHS.append("/data/data/org.example.kivyopencvcamera/files/app/lib")' >> cv2_config/config.py && \
    echo 'if os.path.exists("/data/data/org.example.kivyopencvcamera/lib"):' >> cv2_config/config.py && \
    echo '    BINARIES_PATHS.append("/data/data/org.example.kivyopencvcamera/lib")' >> cv2_config/config.py && \
    echo '' >> cv2_config/config.py && \
    echo '# Tell OpenCV where to find its native libraries' >> cv2_config/config.py && \
    echo 'if hasattr(sys, "getandroidapilevel"):' >> cv2_config/config.py && \
    echo '    ANDROID = True' >> cv2_config/config.py && \
    echo 'else:' >> cv2_config/config.py && \
    echo '    ANDROID = False' >> cv2_config/config.py && \
    echo '# OpenCV config package' > cv2_config/__init__.py

# Android SDK setup - download commandline tools
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools && \
    cd ${ANDROID_HOME}/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-8092744_latest.zip -O commandlinetools.zip && \
    unzip -q commandlinetools.zip && \
    mkdir -p latest && \
    mv cmdline-tools/* latest/ || true && \
    rmdir cmdline-tools || true && \
    rm commandlinetools.zip

# Accept all licenses
RUN mkdir -p ${ANDROID_HOME}/licenses && \
    echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > ${ANDROID_HOME}/licenses/android-sdk-license && \
    echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> ${ANDROID_HOME}/licenses/android-sdk-license && \
    echo "8933bad161af4178b1185d1a37fbf41ea5269c55" >> ${ANDROID_HOME}/licenses/android-sdk-license && \
    echo "84831b9409646a918e30573bab4c9c91346d8abd" > ${ANDROID_HOME}/licenses/android-sdk-preview-license

# Install required Android SDK components and NDK (predownload to avoid timeout issues)
RUN cd ${ANDROID_HOME}/cmdline-tools/latest/bin && \
    ./sdkmanager --sdk_root=${ANDROID_HOME} --update && \
    yes | ./sdkmanager --sdk_root=${ANDROID_HOME} --licenses && \
    ./sdkmanager --sdk_root=${ANDROID_HOME} "platform-tools" "platforms;android-33" "build-tools;33.0.2" && \
    echo "Downloading NDK..." && \
    ./sdkmanager --sdk_root=${ANDROID_HOME} "ndk;25.2.9519653" && \
    echo "NDK downloaded to ${ANDROID_NDK_HOME}"

# For compatibility with buildozer, create the expected tools directory structure
RUN mkdir -p ${ANDROID_HOME}/tools/bin && \
    ln -sf ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager ${ANDROID_HOME}/tools/bin/sdkmanager && \
    ln -sf ${ANDROID_HOME}/cmdline-tools/latest/bin/avdmanager ${ANDROID_HOME}/tools/bin/avdmanager

# Create symbolic links for buildozer to find the NDK
RUN mkdir -p /root/.buildozer/android/platform && \
    ln -sf ${ANDROID_HOME} /root/.buildozer/android/platform/android-sdk && \
    ln -sf ${ANDROID_NDK_HOME} /root/.buildozer/android/platform/android-ndk-r25b

# Create custom OpenCV recipe directory and file
RUN mkdir -p /root/.buildozer/android/platform/python-for-android/recipes/opencv && \
    echo 'from pythonforandroid.recipe import PythonRecipe' > /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py && \
    echo '' >> /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py && \
    echo 'class OpenCVRecipe(PythonRecipe):' >> /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py && \
    echo '    version = "4.5.5.64"' >> /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py && \
    echo '    url = "https://pypi.org/project/opencv-python-headless/4.5.5.64/"' >> /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py && \
    echo '    depends = ["numpy"]' >> /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py && \
    echo '    site_packages_name = "cv2"' >> /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py && \
    echo '' >> /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py && \
    echo 'recipe = OpenCVRecipe()' >> /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py

# Create setup_hooks.py for P4A to use during build
RUN echo '# P4A hooks for OpenCV' > setup_hooks.py && \
    echo 'import os' >> setup_hooks.py && \
    echo 'import shutil' >> setup_hooks.py && \
    echo 'import glob' >> setup_hooks.py && \
    echo 'from os.path import join, exists, basename' >> setup_hooks.py && \
    echo '' >> setup_hooks.py && \
    echo 'def before_apk_build(context):' >> setup_hooks.py && \
    echo '    print("Running pre-build hook for OpenCV integration...")' >> setup_hooks.py && \
    echo '    # Check for OpenCV configuration' >> setup_hooks.py && \
    echo '    site_packages = context.site_packages_dir' >> setup_hooks.py && \
    echo '' >> setup_hooks.py && \
    echo '    # Create cv2 directory if needed' >> setup_hooks.py && \
    echo '    cv2_dir = os.path.join(site_packages, "cv2")' >> setup_hooks.py && \
    echo '    os.makedirs(cv2_dir, exist_ok=True)' >> setup_hooks.py && \
    echo '' >> setup_hooks.py && \
    echo '    # Copy config.py to cv2 directory' >> setup_hooks.py && \
    echo '    if os.path.exists("cv2_config/config.py"):' >> setup_hooks.py && \
    echo '        shutil.copy("cv2_config/config.py", os.path.join(cv2_dir, "config.py"))' >> setup_hooks.py && \
    echo '        print("Copied config.py to cv2 directory")' >> setup_hooks.py && \
    echo '    else:' >> setup_hooks.py && \
    echo '        print("Warning: config.py not found in cv2_config directory")' >> setup_hooks.py && \
    echo '' >> setup_hooks.py && \
    echo 'def after_apk_build(context):' >> setup_hooks.py && \
    echo '    print("Running post-build hook for OpenCV integration...")' >> setup_hooks.py && \
    echo '    # Nothing needed here for now' >> setup_hooks.py && \
    echo '    pass' >> setup_hooks.py

# Copy the patch script and run it
COPY patch_buildozer.py /tmp/patch_buildozer.py
RUN chmod +x /tmp/patch_buildozer.py && \
    python3 /tmp/patch_buildozer.py

# Create build script
RUN echo '#!/bin/bash' > /usr/local/bin/build_apk.sh && \
    echo 'export ANDROID_HOME=/root/android-sdk' >> /usr/local/bin/build_apk.sh && \
    echo 'export ANDROID_SDK_ROOT=/root/android-sdk' >> /usr/local/bin/build_apk.sh && \
    echo 'export ANDROID_NDK_HOME=/root/android-sdk/ndk/25.2.9519653' >> /usr/local/bin/build_apk.sh && \
    echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> /usr/local/bin/build_apk.sh && \
    echo 'export PATH=$PATH:/root/android-sdk/platform-tools:/root/android-sdk/cmdline-tools/latest/bin:$ANDROID_NDK_HOME' >> /usr/local/bin/build_apk.sh && \
    echo '' >> /usr/local/bin/build_apk.sh && \
    echo '# Configure gradle for Java 17' >> /usr/local/bin/build_apk.sh && \
    echo 'mkdir -p /root/.gradle' >> /usr/local/bin/build_apk.sh && \
    echo 'cat > /root/.gradle/gradle.properties << EOF' >> /usr/local/bin/build_apk.sh && \
    echo 'org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8' >> /usr/local/bin/build_apk.sh && \
    echo 'org.gradle.daemon=true' >> /usr/local/bin/build_apk.sh && \
    echo 'org.gradle.parallel=true' >> /usr/local/bin/build_apk.sh && \
    echo 'org.gradle.java.home=${JAVA_HOME}' >> /usr/local/bin/build_apk.sh && \
    echo 'android.useAndroidX=true' >> /usr/local/bin/build_apk.sh && \
    echo 'android.enableJetifier=true' >> /usr/local/bin/build_apk.sh && \
    echo 'EOF' >> /usr/local/bin/build_apk.sh && \
    echo '' >> /usr/local/bin/build_apk.sh && \
    echo '# Clean build if requested' >> /usr/local/bin/build_apk.sh && \
    echo 'if [ "$1" = "clean" ]; then' >> /usr/local/bin/build_apk.sh && \
    echo '    echo "Cleaning buildozer cache..."' >> /usr/local/bin/build_apk.sh && \
    echo '    rm -rf /app/.buildozer' >> /usr/local/bin/build_apk.sh && \
    echo 'fi' >> /usr/local/bin/build_apk.sh && \
    echo '' >> /usr/local/bin/build_apk.sh && \
    echo '# Ensure .buildozer directory exists with proper permissions' >> /usr/local/bin/build_apk.sh && \
    echo 'mkdir -p /app/.buildozer' >> /usr/local/bin/build_apk.sh && \
    echo 'chmod -R 777 /app/.buildozer' >> /usr/local/bin/build_apk.sh && \
    echo '' >> /usr/local/bin/build_apk.sh && \
    echo '# Run buildozer with debug output' >> /usr/local/bin/build_apk.sh && \
    echo 'cd /app' >> /usr/local/bin/build_apk.sh && \
    echo 'buildozer -v android debug' >> /usr/local/bin/build_apk.sh && \
    chmod +x /usr/local/bin/build_apk.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/build_apk.sh"]