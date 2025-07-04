FROM ubuntu:20.04

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME="/root/android-sdk"
ENV ANDROID_SDK_ROOT="/root/android-sdk"
ENV PATH="${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools"

# Add repository for Java 17
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    apt-transport-https \
    ca-certificates \
    gnupg \
    software-properties-common && \
    mkdir -p /etc/apt/keyrings && \
    wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - && \
    add-apt-repository 'deb https://packages.adoptium.net/artifactory/deb $(UBUNTU_CODENAME) main'

# Install required system packages including Java 17
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    build-essential \
    git \
    unzip \
    temurin-17-jdk \
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
ENV JAVA_HOME="/usr/lib/jvm/temurin-17-jdk-amd64"

# Install buildozer
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir buildozer==1.5.0 Cython==0.29.33

# Create app directory
WORKDIR /app

# Download and install Android SDK command-line tools using the correct directory structure
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

# Patch the buildozer script to disable root user check
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

# Create a script to build the APK with Gradle 8.0 and Java 17
RUN echo '#!/bin/bash\n\
export ANDROID_HOME=/root/android-sdk\n\
export ANDROID_SDK_ROOT=/root/android-sdk\n\
export JAVA_HOME=/usr/lib/jvm/temurin-17-jdk-amd64\n\
export PATH=$PATH:/root/android-sdk/platform-tools:/root/android-sdk/cmdline-tools/latest/bin\n\
\n\
# If the gradle wrapper already exists, update it to use Gradle 8.0\n\
if [ -d "/app/.buildozer/android/platform/build-arm64-v8a/dists/kivyopencvcamera" ]; then\n\
    mkdir -p /app/.buildozer/android/platform/build-arm64-v8a/dists/kivyopencvcamera/gradle/wrapper\n\
    echo "distributionBase=GRADLE_USER_HOME" > /app/.buildozer/android/platform/build-arm64-v8a/dists/kivyopencvcamera/gradle/wrapper/gradle-wrapper.properties\n\
    echo "distributionPath=wrapper/dists" >> /app/.buildozer/android/platform/build-arm64-v8a/dists/kivyopencvcamera/gradle/wrapper/gradle-wrapper.properties\n\
    echo "distributionUrl=https\\://services.gradle.org/distributions/gradle-8.0-bin.zip" >> /app/.buildozer/android/platform/build-arm64-v8a/dists/kivyopencvcamera/gradle/wrapper/gradle-wrapper.properties\n\
    echo "zipStoreBase=GRADLE_USER_HOME" >> /app/.buildozer/android/platform/build-arm64-v8a/dists/kivyopencvcamera/gradle/wrapper/gradle-wrapper.properties\n\
    echo "zipStorePath=wrapper/dists" >> /app/.buildozer/android/platform/build-arm64-v8a/dists/kivyopencvcamera/gradle/wrapper/gradle-wrapper.properties\n\
fi\n\
\n\
# Create a custom global gradle.properties with Gradle 8.0 compatibility\n\
mkdir -p /root/.gradle\n\
cat > /root/.gradle/gradle.properties << EOF\n\
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8\n\
org.gradle.daemon=true\n\
org.gradle.parallel=true\n\
org.gradle.configureondemand=true\n\
org.gradle.java.home=${JAVA_HOME}\n\
android.useAndroidX=true\n\
android.enableJetifier=true\n\
EOF\n\
\n\
# Clean buildozer cache if needed\n\
if [ "$1" = "clean" ]; then\n\
    echo "Cleaning buildozer cache..."\n\
    rm -rf /app/.buildozer\n\
fi\n\
\n\
# Run buildozer with proper configuration\n\
cd /app\n\
buildozer -v android debug\n\
' > /usr/local/bin/build_apk.sh && chmod +x /usr/local/bin/build_apk.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/build_apk.sh"]