import os
import sys
import traceback
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import numpy as np

# Define the UI with error reporting
kv = '''
BoxLayout:
    orientation: 'vertical'
    padding: 10
    
    Label:
        text: 'Kivy OpenCV Camera App'
        size_hint_y: 0.1
    
    BoxLayout:
        id: content
        size_hint_y: 0.8
        
    Label:
        id: status
        text: 'OpenCV Status: Initializing...'
        size_hint_y: 0.1
        color: 1, 0, 0, 1
'''

class OpenCVImage(Image):
    def __init__(self, **kwargs):
        super(OpenCVImage, self).__init__(**kwargs)
        self.texture = None
    
    def display_opencv_image(self, cv_img):
        # Convert OpenCV image to Kivy texture
        try:
            # Convert BGR to RGB (OpenCV uses BGR by default)
            rgb_img = cv_img[:, :, [2, 1, 0]]
            
            # Create texture if not already created
            if self.texture is None:
                self.texture = Texture.create(size=(cv_img.shape[1], cv_img.shape[0]), colorfmt='rgb')
                self.texture_size = list(self.texture.size)
            
            # Flip image vertically (OpenCV images are upside down in Kivy)
            flipped_img = np.flip(rgb_img, 0)
            
            # Update texture
            self.texture.blit_buffer(flipped_img.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            
            # Set texture on image widget
            self.texture = self.texture
            return True
        except Exception as e:
            Logger.error(f"OpenCVImage: Failed to display image: {e}")
            return False

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.log_messages = []
        self.has_opencv = False
        
    def build(self):
        try:
            root = Builder.load_string(kv)
            
            # Add error log display
            self.log_label = Label(
                text='Log Messages Will Appear Here',
                size_hint=(1, 0.3),
                halign='left',
                valign='top',
                text_size=(None, None),
                color=(1, 1, 1, 1),
            )
            
            # Create OpenCV image display area
            self.cv_image = OpenCVImage(size_hint=(1, 0.7))
            
            # Add widgets to content area
            content_layout = BoxLayout(orientation='vertical')
            content_layout.add_widget(self.cv_image)
            content_layout.add_widget(self.log_label)
            root.ids.content.add_widget(content_layout)
            
            # Schedule log updates
            Clock.schedule_interval(self.update_log, 1)
            
            return root
        except Exception as e:
            Logger.error(f"App: Build error: {str(e)}")
            Logger.error(f"App: {traceback.format_exc()}")
            return BoxLayout()
    
    def update_log(self, dt):
        # Keep log up to date with any new messages
        self.log_label.text = '\n'.join(self.log_messages[-5:])
        
    def log(self, msg):
        Logger.info(f"App: {msg}")
        self.log_messages.append(msg)
        if len(self.log_messages) > 50:
            self.log_messages.pop(0)

    def on_start(self):
        # App startup
        self.log("Application started")
        
        # Log system information
        self.log(f"Python version: {sys.version}")
        self.log(f"System path: {sys.path}")
        
        # Try importing OpenCV
        try:
            import cv2
            self.log(f"OpenCV loaded successfully, version: {cv2.__version__}")
            self.has_opencv = True
            
            # Update status
            self.root.ids.status.text = f'OpenCV {cv2.__version__} loaded!'
            self.root.ids.status.color = (0, 1, 0, 1)
            
            # Create a test image
            self.log("Creating test image...")
            test_image = np.zeros((300, 300, 3), dtype=np.uint8)
            # Draw a green rectangle
            cv2.rectangle(test_image, (50, 50), (250, 250), (0, 255, 0), 5)
            # Draw some text
            cv2.putText(test_image, "OpenCV Works!", (60, 150), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Display the image
            self.cv_image.display_opencv_image(test_image)
            self.log("Test image displayed!")
            
        except Exception as e:
            self.log(f"Failed to load OpenCV: {str(e)}")
            self.log(f"Error details: {traceback.format_exc()}")
            
            # Update status
            self.root.ids.status.text = 'Error: OpenCV failed to load!'
            self.root.ids.status.color = (1, 0, 0, 1)

if __name__ == '__main__':
    try:
        Logger.info("App: Starting application")
        MainApp().run()
    except Exception as e:
        Logger.error(f"App: Fatal error: {str(e)}")
        Logger.error(f"App: {traceback.format_exc()}")