class MotorController:

    def __init__(self):
        self.last = None
        print("MotorController in SIMULATION mode")

    def send(self, cmd):

        if cmd == self.last:
            return

        print("SIM:", cmd)
        self.last = cmd