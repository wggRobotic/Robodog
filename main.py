import math
import servo_control
from robot_leg import RobotLeg
from robot_dog import RobotDog
import sys

def main():
    upper_leg_length = 108.5
    lower_leg_length = 136.0
    hip_to_shoulder = 50.0

    servo_control.servo_control_init()

    servos_from_legs = [
        [13, 14, 15],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    startPosition = (10,25,30)   

    legs = []
    for i in range(4): 
        legs.append(RobotLeg(i, upper_leg_length, lower_leg_length, hip_to_shoulder, servos_from_legs[i], startPosition))

    body_length: float = 100
    body_width: float = 100
    dog = RobotDog(body_length,body_width,legs)

    z = float(sys.argv[1])

    dog.move_legs([[0, 0, z], [0, 0, z], [0, 0, z], [0, 0, z]], 1)

if __name__ == "__main__":
    main()