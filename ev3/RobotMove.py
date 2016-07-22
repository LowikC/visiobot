import ev3dev.ev3 as ev3

class RobotMove(object):

    def __init__(self):
        self.left_wheel = ev3.Motor(ev3.OUTPUT_C)
        self.right_wheel = ev3.Motor(ev3.OUTPUT_B)
        self.head = ev3.Motor(ev3.OUTPUT_A)

    def forward(self, speed, distance_m):
        time = 1.0
        self.left_wheel.run_forever(duty_cycle_sp=speed)
        self.right_wheel.run_forever(duty_cycle_sp=speed)
        time.sleep(time)
        self.left_wheel.stop()
        self.right_wheel.stop()