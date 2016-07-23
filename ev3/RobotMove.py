import ev3dev.ev3 as ev3
import time

class RobotMove(object):

    def __init__(self):
        self.left_wheel = ev3.Motor(ev3.OUTPUT_C)
        self.right_wheel = ev3.Motor(ev3.OUTPUT_B)
        self.head = ev3.Motor(ev3.OUTPUT_A)
        self.left_wheel.reset()
        self.right_wheel.reset()
        self.head.reset()

    def forward(self, speed, distance_m):
        run_for_s = 1.0
        self.left_wheel.run_forever(duty_cycle_sp=-speed)
        self.right_wheel.run_forever(duty_cycle_sp=-speed)
        time.sleep(run_for_s)
        self.left_wheel.stop()
        self.right_wheel.stop()