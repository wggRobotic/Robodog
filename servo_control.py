import math
#from adafruit_servokit import ServoKit

kit = None

servo_base_positions = [
    6000, 6000, 6000, 6000,
    6000, 6000, 6000,
    6000, 6000, 6000,
    6000, 6000, 6000, 
    5800, 2650, 6100,
]

servo_ranges = [
    3400, 3400, 3400,
    3400, 3400, 3400,
    3400, 3400, 3400,
    3400, 3400, 3400,
    -3400, 3450, -3500
]


def servo_control_init():
    global kit
    #kit = ServoKit(channels = 16)

def servo_move(channel: int, angle: float):
    1==1
    #kit.servo[channel]._pwm_out.duty_cycle = int(servo_base_positions[0] + servo_ranges[0] * angle * 2 / math.pi)