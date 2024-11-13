#servo lines have to be uncommented on execution machine but will give errors otherwise because of obviously unavailable i2c libraries

import math
#from adafruit_servokit import ServoKit

kit = None

servo_base_positions = [
    8200, 3000, 4200, 6666,
    2600, 6700, 5400, 6666, 
    6300, 3600, 4600, 6666, 
    4200, 7100, 5300, 6666,
]

servo_ranges = [
    -3300, 3400, -3000, 3333,
    3500, -3600, 3600, 3333, 
    -3300, 3400, -3000, 3333, 
    3500, -3500, 3200, 3333
]


def servo_control_init():
    global kit
    #kit = ServoKit(channels = 16)

def servo_move(channel: int, angle: float):
    1==1
    #kit.servo[channel]._pwm_out.duty_cycle = int(servo_base_positions[channel] + servo_ranges[channel] * angle * 2 / math.pi)