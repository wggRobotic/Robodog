import math
import servo_control
from robot_leg import RobotLeg
from robot_dog import RobotDog

def main():
    upper_leg_length = 108.5
    lower_leg_length = 136.0
    hip_to_shoulder = 50.0
    body_width: float = 100
    body_length: float = 100

    servos_from_legs = [
        [servo_control.ServoControl(1, 0, math.pi), servo_control.ServoControl(2, 0, math.pi), servo_control.ServoControl(3, 0, math.pi)],
        [servo_control.ServoControl(4, 0, math.pi), servo_control.ServoControl(5, 0, math.pi), servo_control.ServoControl(6, 0, math.pi)],
        [servo_control.ServoControl(7, 0, math.pi), servo_control.ServoControl(8, 0, math.pi), servo_control.ServoControl(9, 0, math.pi)],
        [servo_control.ServoControl(10, 0, math.pi), servo_control.ServoControl(11, 0, math.pi), servo_control.ServoControl(12, 0, math.pi)]
    ]
    startPosition = (10,25,30)   

    legs = []
    for i in range(1,5): 
        legs.append(RobotLeg(i, upper_leg_length, lower_leg_length, hip_to_shoulder, servos_from_legs[i-1], startPosition))

    dog = RobotDog(body_length,body_width,legs)

if __name__ == "__main__":
    main()
