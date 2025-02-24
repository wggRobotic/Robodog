
BAUDRATE = 1000000
DEVICENAME_FRONT = '/dev/board_front'
DEVICENAME_BACK = '/dev/board_back'

STS_MOVING_SPEED = 2400
STS_MOVING_ACC = 50


upper_leg_length = 108.5
lower_leg_length = 136.0
hip_to_shoulder = 50.0

body_length = 100
body_width = 100
upper_leg_length = 108.5
lower_leg_length = 136.0

leg_ids = [
    [1, 2, 3],
    [6, 5, 4],
    [7, 8, 9],
    [12, 11, 10],
]

legs_initial_values = [
    [2047, 2047, 2047, 2047],
    [2047, 2047, 2047, 2047],
    [2047, 2047, 2047, 2047],
    [2047, 2047, 2047, 2047],   
]


servos_min_value = [
    0, 0, 0,
    0, 0, 0,
    0, 0, 0,
    0, 0, 0,
]

servos_max_value = [
    4095, 4095, 4095,
    4095, 4095, 4095,
    4095, 4095, 4095,
    4095, 4095, 4095,
]

