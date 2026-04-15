import cv2
import cv2.aruco as aruco
import numpy as np

class ArucoTracker:

    def __init__(self):
        self.dict = aruco.getPredefinedDictionary(aruco.DICT_7X7_50)
        self.params = aruco.DetectorParameters()
        
        # Aggressive parameters for small markers
        self.params.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX
        self.params.adaptiveThreshConstant = 3  # Lower = more sensitive
        self.params.minMarkerPerimeterRate = 0.01  # Detect VERY small markers
        self.params.maxMarkerPerimeterRate = 4.0
        self.params.errorCorrectionRate = 0.5  # Very tolerant
        self.params.minOtsuStdDev = 5.0  # Lower threshold
        
        self.detector = aruco.ArucoDetector(self.dict, self.params)
        self.last_position = None
        self.missed_frames = 0

    def detect(self, frame):
        # Lightweight preprocessing - just brightness/contrast boost (fast on Pi)
        # Convert to grayscale for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Fast CLAHE - only on grayscale (much faster than full preprocessing)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        
        # Convert back to BGR for detector
        frame_enhanced = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        corners, ids, _ = self.detector.detectMarkers(frame_enhanced)

        if ids is None:
            self.missed_frames += 1
            # Return interpolated position if marker lost (smooth tracking)
            if self.missed_frames < 3 and self.last_position is not None:
                return self.last_position
            return None
        
        self.missed_frames = 0
        c = corners[0][0]
        center_x = int(c[:, 0].mean())
        self.last_position = center_x
        
        return center_x