import os
import sys
import time
import numpy as np
import cv2
from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PySide6.QtGui import QImage, QPixmap

class OpenCVUtils:
    @staticmethod
    def get_opencv_version():
        return cv2.__version__
    
    @staticmethod
    def create_test_image(width=640, height=480):
        """Create a test image with OpenCV"""
        # Create a black image
        img = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Draw a green rectangle
        cv2.rectangle(img, (width//4, height//4), 
                     (3*width//4, 3*height//4), (0, 255, 0), 3)
        
        # Add text
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, f'OpenCV {cv2.__version__}', 
                   (width//4 + 10, height//2), 
                   font, 1, (0, 0, 255), 2)
        
        # Add timestamp
        cv2.putText(img, f'Time: {time.strftime("%H:%M:%S")}', 
                   (width//4 + 10, height//2 + 40), 
                   font, 0.7, (255, 255, 255), 2)
        
        return img
    
    @staticmethod
    def apply_canny_edge_detection(img):
        """Apply Canny edge detection to an image"""
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
            
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply Canny edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Convert back to BGR for consistency
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    @staticmethod
    def convert_cv_to_pixmap(cv_img):
        """Convert an OpenCV image to a Qt QPixmap"""
        # Convert the image from BGR to RGB format
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        
        # Create QImage from the numpy array
        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width
        q_img = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # Convert QImage to QPixmap
        return QPixmap.fromImage(q_img)
    
    @staticmethod
    def get_system_info():
        """Return information about the system"""
        return {
            "opencv_version": cv2.__version__,
            "numpy_version": np.__version__,
            "python_version": sys.version,
            "platform": sys.platform,
            "path": sys.path,
            "executable": sys.executable,
        }