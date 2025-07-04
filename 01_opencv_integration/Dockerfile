# Base image for Android builds
FROM ubuntu:20.04

# Environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/root/.local/bin:${PATH}"

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

# Create app directory
WORKDIR /app

# Install buildozer
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir buildozer==1.5.0 Cython==0.29.33

# Copy the application files
COPY main.py .
COPY buildozer.spec .

# Accept Android licenses
RUN mkdir -p /root/.android && \
    echo '24333f8a63b6825ea9c5514f83c2829b004d1fee' > /root/.android/repositories.cfg && \
    mkdir -p /root/.buildozer/android/platform/licenses && \
    echo "\n8933bad161af4178b1185d1a37fbf41ea5269c55\n24333f8a63b6825ea9c5514f83c2829b004d1fee\nd56f5187479451eabf01fb78af6dfcb131a6481e" > /root/.buildozer/android/platform/licenses/android-sdk-license

# Pre-download Android SDK and NDK (this is the key part for self-containment)
RUN cd /app && \
    buildozer android p4a -- --help && \
    buildozer android update

# Create a build script
RUN echo '#!/bin/bash\ncd /app && buildozer android debug' > /app/build_apk.sh && \
    chmod +x /app/build_apk.sh

# Set the entrypoint
ENTRYPOINT ["/app/build_apk.sh"]