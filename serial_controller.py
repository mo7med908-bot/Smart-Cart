from queue import Queue
import serial
import threading
import time

PORT = "/dev/ttyACM0"  # Configure your Arduino port here
BAUDRATE = 115200

class SerialController:
    @staticmethod
    def check_connection(port=PORT):
        """
        Pre-check if the serial port is available and accessible.
        
        Args:
            port (str): The serial port to check.
        
        Returns:
            bool: True if the port can be opened, False otherwise.
        """
        try:
            ser = serial.Serial(port, BAUDRATE, timeout=1)
            ser.close()
            return True
        except serial.SerialException:
            return False
    
    def __init__(self, port=PORT, baudrate=BAUDRATE):
        """
        Initialize serial connection to Arduino.
        
        Args:
            port (str): Serial port (e.g., '/dev/ttyUSB0')
            baudrate (int): Baud rate (default: 9600)
            
        Raises:
            serial.SerialException: If the port cannot be opened.
        """
        try:
            self.ser = serial.Serial(port, baudrate, timeout=1)
            time.sleep(2)  # Allow Arduino to reset
            print(f"Connected to Arduino on {port} at {baudrate} baud.")
            
            # Setup background thread for serial writes (non-blocking)
            self.cmd_queue = Queue(maxsize=1)
            self.running = True
            self.write_thread = threading.Thread(target=self._serial_writer_thread, daemon=True)
            self.write_thread.start()
        except serial.SerialException as e:
            raise RuntimeError(f"Failed to connect to Arduino: {e}")
    
    def _serial_writer_thread(self):
        """Background thread that writes queued commands to serial port"""
        while self.running:
            try:
                cmd = self.cmd_queue.get(timeout=0.1)
                self.ser.write((cmd + '\n').encode())
            except:
                pass  # Queue timeout is normal
    
    def send_command(self, cmd):
        """
        Sends a command string to the Arduino (non-blocking via background thread).
        
        Args:
            cmd (str): The command to send (e.g., 'FORWARD', 'LEFT').
        """
        try:
            # Non-blocking queue put - discards old commands if queue full
            self.cmd_queue.put_nowait(cmd)
            print(f"Queued command: {cmd}")
        except Exception as e:
            print(f"Error queueing command: {e}")
    
    def close(self):
        """Close serial connection and stop background thread"""
        self.running = False
        if self.ser.is_open:
            self.ser.close()
        print("Serial connection closed.")