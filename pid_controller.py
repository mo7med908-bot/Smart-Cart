class PID:

    def __init__(self, kp=0.5, kd=0.2):

        self.kp = kp
        self.kd = kd
        self.prev = 0

    def compute(self, error):

        derivative = error - self.prev

        output = self.kp * error + self.kd * derivative

        self.prev = error

        return output