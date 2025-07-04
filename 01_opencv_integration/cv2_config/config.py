# OpenCV configuration file for Android
import os
import sys

BINARIES_PATHS = []
HEADLESS = True
DEBUG = False
LOADER_PYTHON_VERSION = "{}.{}.{}".format(*sys.version_info[:3])

# Native libraries for Android
if os.path.exists('/data/data/org.example.kivyopencvcamera/files/app/lib'):
    BINARIES_PATHS.append('/data/data/org.example.kivyopencvcamera/files/app/lib')
if os.path.exists('/data/data/org.example.kivyopencvcamera/lib'):
    BINARIES_PATHS.append('/data/data/org.example.kivyopencvcamera/lib')

# Tell OpenCV where to find its native libraries
if hasattr(sys, 'getandroidapilevel'):
    ANDROID = True
else:
    ANDROID = False