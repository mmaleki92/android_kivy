#!/bin/bash
set -e

# Initialize the BeeWare project
cd /app
briefcase new \
  --template https://github.com/beeware/briefcase-PySide6-template \
  --app-name OpenCVDemo \
  --formal-name "OpenCV Demo" \
  --bundle-id org.example.opencvdemo \
  --author-email "user@example.com" \
  --author-name "Your Name" \
  --project-license "BSD" \
  --description "OpenCV Demo with BeeWare" \
  --url https://example.com/opencvdemo \
  --platforms android

# Add dependencies to pyproject.toml
cd /app/opencvdemo
python3 -c "
import toml
data = toml.load('pyproject.toml')
data['tool']['briefcase']['app']['opencvdemo']['requires'] = [
    'pyside6==6.5.2',
    'opencv-python-headless==4.5.5.64',
    'numpy'
]
with open('pyproject.toml', 'w') as f:
    toml.dump(data, f)
"

# Install required Python packages
pip install toml pyside6==6.5.2 opencv-python-headless==4.5.5.64 numpy