import os
import sys
import traceback
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.clock import Clock

# Setup OpenCV configuration before import
def setup_opencv():
    try:
        Logger.info("OpenCV: Setting up configuration...")
        
        # Find site-packages directory
        site_packages = None
        for p in sys.path:
            if p.endswith('site-packages'):
                site_packages = p
                break
        
        if site_packages:
            # Create cv2 directory if it doesn't exist
            cv2_dir = os.path.join(site_packages, 'cv2')
            os.makedirs(cv2_dir, exist_ok=True)
            
            # Check if config.py already exists
            config_file = os.path.join(cv2_dir, 'config.py')
            if not os.path.exists(config_file):
                Logger.info("OpenCV: Creating config.py file")
                with open(config_file, 'w') as f:
                    f.write("""
# Auto-generated config.py for OpenCV on Android
import os
import sys

BINARIES_PATHS = []
HEADLESS = True
DEBUG = False
LOADER_PYTHON_VERSION = '{}.{}.{}'.format(*sys.version_info[:3])

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
""")
                Logger.info(f"OpenCV: Created config.py at {config_file}")
            else:
                Logger.info(f"OpenCV: config.py already exists at {config_file}")
            return True
        else:
            Logger.error("OpenCV: Could not find site-packages directory")
            return False
    except Exception as e:
        Logger.error(f"OpenCV: Config setup error: {str(e)}")
        Logger.error(f"OpenCV: {traceback.format_exc()}")
        return False

# Set up OpenCV configuration
setup_success = setup_opencv()
Logger.info(f"OpenCV: Configuration setup {'successful' if setup_success else 'failed'}")

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

    # Try to diagnose the issue further
    try:
        import os
        Logger.error("OpenCV: App directory contents: " + str(os.listdir('.')))
        
        # Check Python site-packages
        for path in sys.path:
            if 'site-packages' in path and os.path.exists(path):
                Logger.error(f"OpenCV: Site packages at {path}: {os.listdir(path)}")
                
                # Check if cv2 directory exists
                cv2_path = os.path.join(path, 'cv2')
                if os.path.exists(cv2_path):
                    Logger.error(f"OpenCV: cv2 package contents: {os.listdir(cv2_path)}")
        
        # Check common library paths
        for lib_path in ['/data/data/org.example.kivyopencvcamera/files/app/lib', 
                        '/data/data/org.example.kivyopencvcamera/lib']:
            if os.path.exists(lib_path):
                Logger.error(f"OpenCV: Libraries in {lib_path}: {os.listdir(lib_path)}")
    except Exception as e2:
        Logger.error("OpenCV: Diagnostics failed: " + str(e2))

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
                root.ids.status.text = f'OpenCV loaded successfully'
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
            self.log("OpenCV initialized successfully")
            # Try to show OpenCV version
            try:
                self.log(f"OpenCV version: {cv2.__version__}")
                if hasattr(cv2, 'getBuildInformation'):
                    build_info = cv2.getBuildInformation()
                    self.log(f"OpenCV build info available: {'Yes' if build_info else 'No'}")
            except Exception as e:
                self.log(f"Error getting OpenCV info: {str(e)}")
        else:
            self.log("OpenCV FAILED TO LOAD")
            # Try to show more information about the Python environment
            try:
                self.log(f"Python version: {sys.version}")
                self.log(f"Python path: {sys.path}")
                
                # Try to import numpy to check if it's working
                try:
                    import numpy
                    self.log(f"NumPy version: {numpy.__version__}")
                except Exception as e:
                    self.log(f"NumPy import error: {str(e)}")
            except Exception as e:
                self.log(f"Environment check error: {str(e)}")

if __name__ == '__main__':
    try:
        Logger.info("App: Starting application")
        MainApp().run()
    except Exception as e:
        Logger.error("App: Fatal error: " + str(e))
        Logger.error("App: " + traceback.format_exc())