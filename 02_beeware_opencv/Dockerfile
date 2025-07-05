# Base image with Java, Android SDK, and other dependencies
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV ANDROID_NDK_HOME=/opt/android-sdk/ndk/25.2.9519653
ENV PATH=${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl unzip git \
    python3 python3-pip python3-dev \
    openjdk-11-jdk \
    build-essential \
    libssl-dev libffi-dev \
    libgtk-3-dev libcairo2-dev libgirepository1.0-dev \
    libpq-dev pkg-config \
    libjpeg-dev libpng-dev \
    software-properties-common \
    cmake ninja-build \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Android SDK
RUN mkdir -p ${ANDROID_HOME}/cmdline-tools && \
    cd ${ANDROID_HOME}/cmdline-tools && \
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-8092744_latest.zip && \
    unzip -q commandlinetools-linux-8092744_latest.zip && \
    mkdir -p latest && \
    mv cmdline-tools/* latest/ || true && \
    rmdir cmdline-tools || true && \
    rm commandlinetools-linux-8092744_latest.zip

# Accept licenses and install Android components
RUN mkdir -p ${ANDROID_HOME}/licenses && \
    echo "24333f8a63b6825ea9c5514f83c2829b004d1fee" > ${ANDROID_HOME}/licenses/android-sdk-license && \
    echo "d56f5187479451eabf01fb78af6dfcb131a6481e" >> ${ANDROID_HOME}/licenses/android-sdk-license && \
    ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager --sdk_root=${ANDROID_HOME} "platform-tools" "platforms;android-33" "build-tools;33.0.2" "ndk;25.2.9519653"

# Install Python packages
RUN pip3 install --upgrade pip && \
    pip3 install briefcase opencv-python-headless numpy pyside6

# Create app directory
WORKDIR /app

# Set environment variable to avoid SDL error
ENV SDL_VIDEODRIVER=dummy

# Create a non-root user to build and run the app (helps with permissions)
RUN useradd -ms /bin/bash beeuser && \
    chown -R beeuser:beeuser /app

# Setup for OpenCV with Android
RUN mkdir -p /opt/opencv_android && \
    cd /opt/opencv_android && \
    wget -q https://github.com/opencv/opencv/releases/download/4.5.5/opencv-4.5.5-android-sdk.zip && \
    unzip -q opencv-4.5.5-android-sdk.zip && \
    rm opencv-4.5.5-android-sdk.zip && \
    ln -s /opt/opencv_android/OpenCV-android-sdk /opt/opencv

# Switch to non-root user for safer execution
USER beeuser

# Command to run when container starts
CMD ["/bin/bash"]