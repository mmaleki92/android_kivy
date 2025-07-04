from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
import numpy as np


class CameraCV(Image):
    def __init__(self, **kwargs):
        super(CameraCV, self).__init__(**kwargs)
        self.capture = None
        self.processing_mode = 'normal'

    def start(self):
        """Start the camera capture"""
        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            print("Error: Could not open camera.")
            return
        
        # Schedule the update
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS

    def stop(self):
        """Stop the camera capture"""
        if self.capture:
            Clock.unschedule(self.update)
            self.capture.release()
            self.capture = None

    def update(self, dt):
        """Update the camera feed with OpenCV processing"""
        if self.capture is None:
            return
            
        ret, frame = self.capture.read()
        if ret:
            # OpenCV processing based on mode
            if self.processing_mode == 'grayscale':
                # Convert to grayscale
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # Convert back for display
            elif self.processing_mode == 'edges':
                # Edge detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            elif self.processing_mode == 'blur':
                # Apply Gaussian blur
                frame = cv2.GaussianBlur(frame, (15, 15), 0)
            
            # Flip the frame (mirror effect)
            frame = cv2.flip(frame, 1)
            
            # Convert to texture
            buf = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            
            # Display the image from the texture
            self.texture = texture


class CameraApp(App):
    def build(self):
        # Main layout
        layout = BoxLayout(orientation='vertical')
        
        # Camera display
        self.camera = CameraCV()
        layout.add_widget(self.camera)
        
        # Buttons layout
        button_layout = BoxLayout(size_hint=(1, 0.1))
        
        # Start button
        btn_start = Button(text='Start Camera')
        btn_start.bind(on_press=self.start_camera)
        button_layout.add_widget(btn_start)
        
        # Stop button
        btn_stop = Button(text='Stop Camera')
        btn_stop.bind(on_press=self.stop_camera)
        button_layout.add_widget(btn_stop)
        
        # Image processing buttons
        btn_normal = Button(text='Normal')
        btn_normal.bind(on_press=self.set_normal)
        button_layout.add_widget(btn_normal)
        
        btn_gray = Button(text='Grayscale')
        btn_gray.bind(on_press=self.set_grayscale)
        button_layout.add_widget(btn_gray)
        
        btn_edges = Button(text='Edge Detection')
        btn_edges.bind(on_press=self.set_edges)
        button_layout.add_widget(btn_edges)
        
        btn_blur = Button(text='Blur')
        btn_blur.bind(on_press=self.set_blur)
        button_layout.add_widget(btn_blur)
        
        # Add button layout to main layout
        layout.add_widget(button_layout)
        
        return layout
    
    def start_camera(self, instance):
        self.camera.start()
        
    def stop_camera(self, instance):
        self.camera.stop()
    
    def set_normal(self, instance):
        self.camera.processing_mode = 'normal'
    
    def set_grayscale(self, instance):
        self.camera.processing_mode = 'grayscale'
        
    def set_edges(self, instance):
        self.camera.processing_mode = 'edges'
        
    def set_blur(self, instance):
        self.camera.processing_mode = 'blur'

    def on_stop(self):
        self.camera.stop()


if __name__ == '__main__':
    CameraApp().run()