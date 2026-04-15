from camera_manager import CameraManager
from aruco_tracker import ArucoTracker
from pid_controller import PID
from serial_controller import SerialController
import cv2
import time

cam = CameraManager()
tracker = ArucoTracker()
pid = PID()
serial_ctrl = SerialController()
# Pre-check Arduino connection
if not SerialController.check_connection():
    print("Arduino not connected to serial port. Please check the connection and try again.")
    exit(1)

# Frame rate limiting - match camera FPS for best responsiveness
last_frame_time = 0
target_fps = 30  # Increased from 5 to match camera (30 FPS)
frame_skip = 0  # Process every frame for best responsiveness

while True:
    frame = cam.get_frame()
    h, w = frame.shape[:2]
    center = w // 2
    marker_x = tracker.detect(frame)

    if marker_x is not None:
        error = marker_x - center
        output = pid.compute(error)

        if abs(output) < 60:
            cmd = "FORWARD"
        elif output > 0:
            cmd = "RIGHT"
        else:
            cmd = "LEFT"

        print("CMD:", cmd, "ERROR:", error, "X:", marker_x)
        serial_ctrl.send_command(cmd)
    else:
        cmd = "STOP"
        print("CMD: STOP (no marker)")
        serial_ctrl.send_command(cmd)

    cv2.imshow("VISION MODE", frame)

    if cv2.waitKey(1) == 27:
        serial_ctrl.close()
        cam.release()
        cv2.destroyAllWindows()
        break