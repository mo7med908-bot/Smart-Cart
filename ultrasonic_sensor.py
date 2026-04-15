import time
import RPi.GPIO as GPIO

class Ultrasonic:

    def __init__(self, trig=23, echo=24):

        self.trig = trig
        self.echo = echo

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(trig, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)

    def distance(self):

        GPIO.output(self.trig, False)
        time.sleep(0.01)

        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        start = time.time()
        stop = time.time()

        while GPIO.input(self.echo) == 0:
            start = time.time()

        while GPIO.input(self.echo) == 1:
            stop = time.time()

        duration = stop - start

        distance = duration * 17150

        return distance