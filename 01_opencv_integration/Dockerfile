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
        # Create the config file directly\n\
        with open(os.path.join(cv2_dir, "config.py"), "w") as f:\n\
            f.write("""\n\
# Auto-generated config.py for OpenCV on Android\n\
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
""")\n\
            print("Created config.py file directly in cv2 directory")\n\
\n\
def after_apk_build(context):\n\
    print("Running post-build hook for OpenCV integration...")\n\
    # Nothing needed here for now\n\
    pass\n\
' > setup_hooks.py

# Create simplified opencv_recipe.py
RUN echo 'from pythonforandroid.recipe import PythonRecipe\n\
\n\
class OpenCVRecipe(PythonRecipe):\n\
    version = "4.5.5.64"\n\
    url = "https://pypi.org/project/opencv-python-headless/4.5.5.64/"\n\
    depends = ["numpy"]\n\
    site_packages_name = "cv2"\n\
\n\
recipe = OpenCVRecipe()\n\
' > /root/.buildozer/android/platform/python-for-android/recipes/opencv/__init__.py

# Patch buildozer to disable root user check and fix NDK path
RUN echo '#!/usr/bin/env python3\n\
import fileinput\n\
import sys\n\
import os\n\
\n\
# First patch - disable root user check\n\
filename = "/usr/local/lib/python3.8/dist-packages/buildozer/__init__.py"\n\
with fileinput.FileInput(filename, inplace=True) as file:\n\
    for line in file:\n\
        if "def check_root(self):" in line:\n\
            print(line, end="")\n\
            print("        # Root check disabled for Docker")\n\
            print("        return")\n\
            continue\n\
        print(line, end="")\n\
\n\
# Second patch - use pre-downloaded NDK\n\
filename = "/usr/local/lib/python3.8/dist-packages/buildozer/targets/android.py"\n\
with fileinput.FileInput(filename, inplace=True) as file:\n\
    for line in file:\n\
        if "def _install_android_ndk(self):" in line:\n\
            print(line, end="")\n\
            print("        # Skip downloading NDK - use pre-downloaded version")\n\
            print("        ndk_dir = self.android_ndk_dir")\n\
            print("        self.buildozer.info(\'Android NDK found at {}\'.format(ndk_dir))")\n\
            print("        return")\n\
            continue\n\
        print(line, end="")\n\
' > /tmp/patch_buildozer.py && \
    python3 /tmp/patch_buildozer.py

# Create build script
RUN echo '#!/bin/bash\n\
export ANDROID_HOME=/root/android-sdk\n\
export ANDROID_SDK_ROOT=/root/android-sdk\n\
export ANDROID_NDK_HOME=/root/android-sdk/ndk/25.2.9519653\n\
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64\n\
export PATH=$PATH:/root/android-sdk/platform-tools:/root/android-sdk/cmdline-tools/latest/bin:$ANDROID_NDK_HOME\n\
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
# Ensure .buildozer directory exists with proper permissions\n\
mkdir -p /app/.buildozer\n\
chmod -R 777 /app/.buildozer\n\
\n\
# Create buildozer.spec if it doesn\'t exist\n\
if [ ! -f "/app/buildozer.spec" ]; then\n\
    echo "Creating default buildozer.spec..."\n\
    buildozer init\n\
fi\n\
\n\
# Create important directories\n\
mkdir -p /app/libs/arm64-v8a\n\
mkdir -p /app/libs/armeabi-v7a\n\
mkdir -p /app/libs/x86\n\
mkdir -p /app/libs/x86_64\n\
mkdir -p /app/cv2_config\n\
\n\
# Create OpenCV config if it doesn\'t exist\n\
if [ ! -f "/app/cv2_config/config.py" ]; then\n\
    echo "Creating OpenCV config..."\n\
    cat > /app/cv2_config/config.py << EOF\n\
# OpenCV configuration file for Android\n\
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
EOF\n\
    echo "# OpenCV config package" > /app/cv2_config/__init__.py\n\
fi\n\
\n\
# Copy setup hooks\n\
cp /app/setup_hooks.py /app/\n\
\n\
# Run buildozer with debug output\n\
cd /app\n\
buildozer -v android debug\n\
' > /usr/local/bin/build_apk.sh && chmod +x /usr/local/bin/build_apk.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/build_apk.sh"]