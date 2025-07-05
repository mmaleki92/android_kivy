import sys
import os
from pathlib import Path
import importlib.util

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QCheckBox, QGridLayout
)
from PySide6.QtGui import QPixmap, QFont

# Try importing OpenCV
try:
    from .opencv_utils import OpenCVUtils
    OPENCV_AVAILABLE = True
except ImportError:
    print("OpenCV not available, some features will be disabled")
    OPENCV_AVAILABLE = False

class OpenCVDemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set window title and size
        self.setWindowTitle("OpenCV Demo")
        self.resize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Header with title
        header = QLabel("OpenCV Demo App")
        header.setFont(QFont("Arial", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        # Status area
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Initializing...")
        status_layout.addWidget(self.status_label)
        main_layout.addLayout(status_layout)
        
        # Image display area with controls
        display_layout = QHBoxLayout()
        
        # Image display
        self.image_display = QLabel()
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setMinimumSize(640, 480)
        self.image_display.setStyleSheet("background-color: #222222; border: 1px solid #444444;")
        display_layout.addWidget(self.image_display, 3)
        
        # Control panel
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # Effect selection
        effect_layout = QGridLayout()
        effect_layout.addWidget(QLabel("Effect:"), 0, 0)
        self.effect_combo = QComboBox()
        self.effect_combo.addItems(["None", "Canny Edge", "Blur", "Grayscale"])
        effect_layout.addWidget(self.effect_combo, 0, 1)
        control_layout.addLayout(effect_layout)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh Image")
        self.refresh_button.clicked.connect(self.update_image)
        control_layout.addWidget(self.refresh_button)
        
        # Add stretch to push controls to top
        control_layout.addStretch()
        
        # Add control panel to display layout
        display_layout.addWidget(control_panel, 1)
        
        # Add display layout to main layout
        main_layout.addLayout(display_layout)
        
        # Footer with OpenCV info
        footer_layout = QHBoxLayout()
        if OPENCV_AVAILABLE:
            self.opencv_version = QLabel(f"OpenCV Version: {OpenCVUtils.get_opencv_version()}")
        else:
            self.opencv_version = QLabel("OpenCV not available")
        footer_layout.addWidget(self.opencv_version)
        main_layout.addLayout(footer_layout)
        
        # Initialize timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(1000)  # Update every 1000 ms
        
        # Initial image update
        self.update_image()
    
    def update_image(self):
        """Update the displayed image with selected effect"""
        if not OPENCV_AVAILABLE:
            self.status_label.setText("OpenCV not available")
            return
            
        try:
            # Create test image
            img = OpenCVUtils.create_test_image()
            
            # Apply selected effect
            effect = self.effect_combo.currentText()
            if effect == "Canny Edge":
                img = OpenCVUtils.apply_canny_edge_detection(img)
                self.status_label.setText("Applied Canny Edge Detection")
            elif effect == "Blur":
                img = cv2.GaussianBlur(img, (15, 15), 0)
                self.status_label.setText("Applied Gaussian Blur")
            elif effect == "Grayscale":
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
                self.status_label.setText("Converted to Grayscale")
            else:
                self.status_label.setText("No effect applied")
            
            # Convert to QPixmap and display
            pixmap = OpenCVUtils.convert_cv_to_pixmap(img)
            self.image_display.setPixmap(pixmap)
            
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    # Create the Qt Application
    app = QApplication(sys.argv)
    
    # Check OpenCV availability and system info
    if OPENCV_AVAILABLE:
        system_info = OpenCVUtils.get_system_info()
        print("System Information:")
        for key, value in system_info.items():
            print(f"  {key}: {value}")
    
    # Create and show the main window
    window = OpenCVDemoWindow()
    window.show()
    
    # Start the event loop
    return app.exec()