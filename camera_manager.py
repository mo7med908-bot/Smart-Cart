from picamera2 import Picamera2
import numpy as np

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
CAMERA_FPS = 30

class CameraManager:
    def __init__(self):
        try:
            self.picam2 = Picamera2()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize ArduCAM with picamera2: {e}")
        
        # Configure camera with specified resolution and FPS
        config = self.picam2.create_preview_configuration(
            main={"format": "RGB888", "size": (CAMERA_WIDTH, CAMERA_HEIGHT)}
        )
        self.picam2.configure(config)
        self.picam2.set_controls({"FrameRate": CAMERA_FPS})
        self.picam2.start()

    def get_frame(self):
        """Capture and return a frame from the ArduCAM"""
        try:
            frame = self.picam2.capture_array()
            if frame is None:
                raise RuntimeError("Failed to capture frame from ArduCAM")
            # Convert from RGB to BGR for OpenCV compatibility
            frame = frame[:, :, ::-1]
            return frame
        except Exception as e:
            raise RuntimeError(f"Error capturing frame: {e}")
    
    def release(self):
        """Release the camera resource"""
        try:
            self.picam2.stop()
            self.picam2.close()
        except Exception as e:
            print(f"Warning: Error releasing camera: {e}")