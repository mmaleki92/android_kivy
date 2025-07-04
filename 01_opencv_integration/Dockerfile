# Base image for Android builds
FROM ubuntu:20.04

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.local/bin:/root/android-sdk/cmdline-tools/latest/bin:${PATH}"
ENV ANDROID_HOME="/root/android-sdk"
ENV ANDROID_SDK_ROOT="/root/android-sdk"

# Install required system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-dev \
    build-essential \
    git \
    wget \
    unzip \
    openjdk-11-jdk \
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

# Install buildozer
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir buildozer==1.5.0 Cython==0.29.33

# Create app directory
WORKDIR /app

# Install Android SDK manually (bypassing buildozer's installation)
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-8092744_latest.zip -O cmdline-tools.zip && \
    unzip cmdline-tools.zip -d ${ANDROID_HOME}/tmp && \
    mv ${ANDROID_HOME}/tmp/cmdline-tools ${ANDROID_HOME}/cmdline-tools/latest && \
    rm -rf ${ANDROID_HOME}/tmp cmdline-tools.zip

# Accept all licenses
RUN mkdir -p ${ANDROID_HOME}/licenses && \
    echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > ${ANDROID_HOME}/licenses/android-sdk-license && \
    echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> ${ANDROID_HOME}/licenses/android-sdk-license && \
    echo "8933bad161af4178b1185d1a37fbf41ea5269c55" >> ${ANDROID_HOME}/licenses/android-sdk-license && \
    echo "84831b9409646a918e30573bab4c9c91346d8abd" > ${ANDROID_HOME}/licenses/android-sdk-preview-license

# Install required Android SDK components
RUN yes | sdkmanager --licenses && \
    sdkmanager --update && \
    sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.2" "ndk;25.2.9519653"

# Create a script to build the APK
RUN echo '#!/bin/bash\n\
# Patch the buildozer script to disable root user check\n\
cat > /tmp/buildozer_patch.py << EOF\n\
#!/usr/bin/env python3\n\
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
EOF\n\
\n\
python3 /tmp/buildozer_patch.py\n\
\n\
# Make sure buildozer uses our pre-installed SDK\n\
export ANDROID_HOME=/root/android-sdk\n\
export ANDROID_SDK_ROOT=/root/android-sdk\n\
export PATH=$PATH:/root/android-sdk/platform-tools\n\
\n\
# Now run buildozer\n\
cd /app\n\
buildozer -v android debug\n\
' > /usr/local/bin/build_apk.sh && chmod +x /usr/local/bin/build_apk.sh

# Set the entrypoint
ENTRYPOINT ["/usr/local/bin/build_apk.sh"]