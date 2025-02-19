verbosity = True

upper_leg_length = 108.5
lower_leg_length = 136.0
hip_to_shoulder = 50.0

leg_ids = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [9, 10, 11]
]

legs_initial_positions = [
    [0.0, 0.0, 150.0],
    [0.0, 0.0, 150.0],
    [0.0, 0.0, 150.0],
    [0.0, 0.0, 150.0],
]

BAUDRATE1                    = 1000000           # STServo default baudrate : 1000000
BAUDRATE2                    = 1000000           # STServo default baudrate : 1000000
DEVICENAME1                  = 'COM11'    # Check which port is being used on your controller
DEVICENAME2                  = 'COM12'    # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

STS_MINIMUM_POSITION_VALUE  = 0             # SCServo will rotate between this value
STS_MAXIMUM_POSITION_VALUE  = 4095
STS_MOVING_SPEED            = 2400          # SCServo moving speed
STS_MOVING_ACC              = 50            # SCServo moving acc
