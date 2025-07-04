#!/usr/bin/env python3
import fileinput
import sys
import os

# First patch - disable root user check
filename = "/usr/local/lib/python3.8/dist-packages/buildozer/__init__.py"
with fileinput.FileInput(filename, inplace=True) as file:
    for line in file:
        if "def check_root(self):" in line:
            print(line, end="")
            print("        # Root check disabled for Docker")
            print("        return")
            continue
        print(line, end="")

# Second patch - use pre-downloaded NDK
filename = "/usr/local/lib/python3.8/dist-packages/buildozer/targets/android.py"
with fileinput.FileInput(filename, inplace=True) as file:
    for line in file:
        if "def _install_android_ndk(self):" in line:
            print(line, end="")
            print("        # Skip downloading NDK - use pre-downloaded version")
            print("        ndk_dir = self.android_ndk_dir")
            print("        self.buildozer.info('Android NDK found at {}'.format(ndk_dir))")
            print("        return")
            continue
        print(line, end="")