BAUDRATE = 1000000
DEVICE_NAME_FRONT = "/dev/board_front"
DEVICE_NAME_BACK = "/dev/board_back"

STS_MOVING_SPEED = 2400
STS_MOVING_ACC = 50


UPPER_LEG_LENGTH = 95.0
LOWER_LEG_LENGTH = 115.0
HIP_TO_SHOULDER = 90.0
BODY_LENGTH = 260.0
BODY_WIDTH = 70.0

LEG_IDS = [
    [1, 2, 3],
    [6, 5, 4],
    [7, 8, 9],
    [12, 11, 10],
]


LEGS_INITIAL_POSITIONS = [
    [-20.0, HIP_TO_SHOULDER, 180.0],
    [-20.0, -HIP_TO_SHOULDER, 180.0],
    [0.0, HIP_TO_SHOULDER, 180.0],
    [0.0, -HIP_TO_SHOULDER, 180.0],
]


SERVOS_MIN_VALUE = [
    1237,
    0,
    1242,
    954,
    0,
    979,
    1539,
    0,
    847,
    1287,
    0,
    817,
]

SERVOS_MAX_VALUE = [
    3345,
    4095,
    3230,
    2881,
    4095,
    2612,
    3344,
    4095,
    2842,
    3161,
    4095,
    2598,
]
