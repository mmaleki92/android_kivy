import os
import sys
import traceback
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.clock import Clock

# Set up better error reporting
os.environ['KIVY_NO_CONSOLELOG'] = '0'

# Try importing OpenCV with robust error handling
try:
    Logger.info("OpenCV: Attempting to import cv2...")
    import cv2
    Logger.info("OpenCV: Successfully imported cv2 version " + cv2.__version__)
    HAS_CV2 = True
except Exception as e:
    Logger.error("OpenCV: Failed to import cv2: " + str(e))
    Logger.error("OpenCV: " + traceback.format_exc())
    HAS_CV2 = False

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

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.log_messages = []
        
    def build(self):
        try:
            root = Builder.load_string(kv)
            # Add error log display
            self.log_label = Label(
                text='Log Messages Will Appear Here',
                size_hint=(1, 1),
                halign='left',
                valign='top',
                text_size=(None, None),
                color=(1, 1, 1, 1),
            )
            log_box = BoxLayout(orientation='vertical')
            log_box.add_widget(self.log_label)
            root.ids.content.add_widget(log_box)
            
            # Update OpenCV status
            if HAS_CV2:
                root.ids.status.text = f'OpenCV {cv2.__version__} loaded successfully'
                root.ids.status.color = (0, 1, 0, 1)
            else:
                root.ids.status.text = 'Error: OpenCV failed to load!'
                
            # Schedule log updates
            Clock.schedule_interval(self.update_log, 1)
            
            return root
        except Exception as e:
            Logger.error("App: Build error: " + str(e))
            Logger.error("App: " + traceback.format_exc())
            return BoxLayout()
    
    def update_log(self, dt):
        # Keep log up to date with any new messages
        self.log_label.text = '\n'.join(self.log_messages[-10:])
        
    def log(self, msg):
        Logger.info("App: " + msg)
        self.log_messages.append(msg)
        if len(self.log_messages) > 50:
            self.log_messages.pop(0)

    def on_start(self):
        # App startup
        self.log("Application started")
        if HAS_CV2:
            self.log(f"OpenCV {cv2.__version__} initialized")
            # List available cameras
            try:
                self.log("Checking camera availability...")
                if hasattr(cv2, 'getBuildInformation'):
                    self.log("OpenCV build: OK")
            except Exception as e:
                self.log(f"Camera check error: {str(e)}")
        else:
            self.log("OpenCV FAILED TO LOAD")

if __name__ == '__main__':
    try:
        Logger.info("App: Starting application")
        MainApp().run()
    except Exception as e:
        Logger.error("App: Fatal error: " + str(e))
        Logger.error("App: " + traceback.format_exc())