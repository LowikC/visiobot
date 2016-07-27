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

    def forward(self, speed=100, time_ms=1000):
        self.left_wheel.run_timed(duty_cycle_sp=-speed, time_sp=time_ms)
        self.right_wheel.run_timed(duty_cycle_sp=-speed, time_sp=time_ms)

    def head_move(self):
        speed = 70
        self.head.run_timed(duty_cycle_sp=-speed, time_sp=100)
        self.head.run_timed(duty_cycle_sp=speed, time_sp=100)

    def turn_360(self):
        speed = 100
        time_ms = 200000 / speed
        self.left_wheel.run_timed(duty_cycle_sp=-speed, time_sp=time_ms)
        self.right_wheel.run_timed(duty_cycle_sp=speed, time_sp=time_ms)

    def turn_180(self):
        speed = 50
        time_ms = 200000 / speed
        self.left_wheel.run_timed(duty_cycle_sp=-speed, time_sp=time_ms)
        self.right_wheel.run_timed(duty_cycle_sp=speed, time_sp=time_ms)

