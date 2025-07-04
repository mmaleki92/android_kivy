FROM ubuntu:20.04

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME="/root/android-sdk"
ENV ANDROID_SDK_ROOT="/root/android-sdk"
ENV PATH="${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools"

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

# Setup OpenCV native libraries - embedded in the Dockerfile with improved diagnostics
RUN mkdir -p libs/arm64-v8a libs/armeabi-v7a libs/x86 libs/x86_64 && \
    wget -O opencv.zip https://github.com/opencv/opencv/releases/download/4.5.5/opencv-4.5.5-android-sdk.zip && \
    unzip -q opencv.zip && \
    # Explore directory structure to find the .so files
    find opencv-4.5.5-android-sdk -name "*.so" | grep -v "jni" > opencv_libs_paths.txt && \
    # Check the actual structure of the downloaded archive
    ls -la opencv-4.5.5-android-sdk/ && \
    # Most likely location based on recent OpenCV releases
    mkdir -p opencv-4.5.5-android-sdk/sdk/native/libs && \
    # Create a script to find and copy the libraries
    echo '#!/bin/bash' > copy_libs.sh && \
    echo 'set -x' >> copy_libs.sh && \
    echo 'find opencv-4.5.5-android-sdk -name "*.so" -exec cp {} libs/arm64-v8a/ \;' >> copy_libs.sh && \
    chmod +x copy_libs.sh && \
    ./copy_libs.sh && \
    # Make sure we have libraries in the destination directories
    cp -r libs/arm64-v8a/* libs/armeabi-v7a/ && \
    cp -r libs/arm64-v8a/* libs/x86/ && \
    cp -r libs/arm64-v8a/* libs/x86_64/ && \
    # Clean up
    rm -rf opencv.zip opencv-4.5.5-android-sdk copy_libs.sh opencv_libs_paths.txt

# Create OpenCV config file
RUN mkdir -p cv2_config && \
    echo '# OpenCV configuration file for Android\n\
import os\n\
import sys\n\
\n\
BINARIES_PATHS = []\n\
HEADLESS = True\n\
DEBUG = False\n\
LOADER_PYTHON_VERSION = "{}.{}.{}".format(*sys.version_info[:3])\n\
\n\
# Native libraries for Android\n\
if os.path.exists("/data/data/org.example.kivyopencvcamera/files/app/lib"):\n\
    BINARIES_PATHS.append("/data/data/org.example.kivyopencvcamera/files/app/lib")\n\
if os.path.exists("/data/data/org.example.kivyopencvcamera/lib"):\n\
    BINARIES_PATHS.append("/data/data/org.example.kivyopencvcamera/lib")\n\
\n\
# Tell OpenCV where to find its native libraries\n\
if hasattr(sys, "getandroidapilevel"):\n\
    ANDROID = True\n\
else:\n\
    ANDROID = False\n\
' > cv2_config/config.py && \
    echo '# OpenCV config package' > cv2_config/__init__.py

# Android SDK setup
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

# Install required Android SDK components
RUN cd ${ANDROID_HOME}/cmdline-tools/latest/bin && \
    ./sdkmanager --sdk_root=${ANDROID_HOME} --update && \
    yes | ./sdkmanager --sdk_root=${ANDROID_HOME} --licenses && \
    ./sdkmanager --sdk_root=${ANDROID_HOME} "platform-tools" "platforms;android-33" "build-tools;33.0.2" "ndk;25.2.9519653"

# For compatibility with buildozer, create the expected tools directory structure
RUN mkdir -p ${ANDROID_HOME}/tools/bin && \
    ln -sf ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager ${ANDROID_HOME}/tools/bin/sdkmanager && \
    ln -sf ${ANDROID_HOME}/cmdline-tools/latest/bin/avdmanager ${ANDROID_HOME}/tools/bin/avdmanager

# Create custom OpenCV recipe directory
RUN mkdir -p /root/.buildozer/android/platform/python-for-android/recipes/opencv

# Create setup_hooks.py for P4A to use during build
RUN echo 'import os\n\
import shutil\n\
import glob\n\
from os.path import join, exists, basename\n\
\n\
def before_apk_build(context):\n\
    print("Running pre-build hook for OpenCV integration...")\n\
    # Check for OpenCV configuration\n\
    site_packages = context.site_packages_dir\n\
    \n\
    # Create cv2 directory if needed\n\
    cv2_dir = os.path.join(site_packages, "cv2")\n\
    os.makedirs(cv2_dir, exist_ok=True)\n\
    \n\
    # Copy config.py to cv2 directory\n\
    if os.path.exists("cv2_config/config.py"):\n\
        shutil.copy("cv2_config/config.py", os.path.join(cv2_dir, "config.py"))\n\
        print("Copied config.py to cv2 directory")\n\
    else:\n\
        print("Warning: config.py not found in cv2_config directory")\n\
\n\
def after_apk_build(context):\n\
    print("Running post-build hook for OpenCV integration...")\n\
    # Nothing needed here for now\n\
    pass\n\
' > setup_hooks.py

# Copy the custom OpenCV recipe
COPY opencv_recipe.py /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py

# Patch buildozer to disable root user check
RUN echo '#!/usr/bin/env python3\n\
import fileinput\n\
import sys\n\
\n\
filename = "/usr/local/lib/python3.8/dist-packages/buildozer/__init__.py"\n\
with fileinput.FileInput(filename, inplace=True) as file:\n\
    for line in file:\n\
        if "def check_root(self):" in line:\n\
            print(line, end="")\n\
            print("        # Root check disabled for Docker")\n\
            print("        return")\n\
            continue\n\
        print(line, end="")\n\
' > /tmp/patch_buildozer.py && \
    python3 /tmp/patch_buildozer.py

# Create build script
RUN echo '#!/bin/bash\n\
export ANDROID_HOME=/root/android-sdk\n\
export ANDROID_SDK_ROOT=/root/android-sdk\n\
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64\n\
export PATH=$PATH:/root/android-sdk/platform-tools:/root/android-sdk/cmdline-tools/latest/bin\n\
\n\
# Configure gradle for Java 17\n\
mkdir -p /root/.gradle\n\
cat > /root/.gradle/gradle.properties << EOF\n\
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8\n\
org.gradle.daemon=true\n\
org.gradle.parallel=true\n\
org.gradle.java.home=${JAVA_HOME}\n\
android.useAndroidX=true\n\
android.enableJetifier=true\n\
EOF\n\
\n\
# Clean build if requested\n\
if [ "$1" = "clean" ]; then\n\
    echo "Cleaning buildozer cache..."\n\
    rm -rf /app/.buildozer\n\
fi\n\
\n\
# Copy OpenCV libraries if they don\'t exist in the app directory\n\
if [ ! -d "/app/libs" ]; then\n\
    echo "Copying OpenCV libraries to app directory..."\n\
    cp -r /app/libs /app/\n\
fi\n\
\n\
# Copy OpenCV config if it doesn\'t exist\n\
if [ ! -d "/app/cv2_config" ]; then\n\
    echo "Copying OpenCV config to app directory..."\n\
    cp -r /app/cv2_config /app/\n\
fi\n\
\n\
# Run buildozer with debug output\n\
cd /app\n\
buildozer -v android debug\n\
' > /usr/local/bin/build_apk.sh && chmod +x /usr/local/bin/build_apk.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/build_apk.sh"]