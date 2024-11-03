import math
import servo_control
from robot_leg import RobotLeg
from robot_dog import RobotDog

def main():
    upper_leg_length = 108.5
    lower_leg_length = 136.0
    hip_to_shoulder = 50.0

    servos_from_leg1 = [
        servo_control.ServoControl(1, 0, math.pi),
        servo_control.ServoControl(2, 0, math.pi),
        servo_control.ServoControl(3, 0, math.pi),
    ]
    servos_from_leg2 = [
        servo_control.ServoControl(4, 0, math.pi),
        servo_control.ServoControl(5, 0, math.pi),
        servo_control.ServoControl(6, 0, math.pi),
    ]
    servos_from_leg3 = [
        servo_control.ServoControl(7, 0, math.pi),
        servo_control.ServoControl(8, 0, math.pi),
        servo_control.ServoControl(9, 0, math.pi),
    ]
    servos_from_leg4 = [
        servo_control.ServoControl(10, 0, math.pi),
        servo_control.ServoControl(11, 0, math.pi),
        servo_control.ServoControl(12, 0, math.pi),
    ]

    startPositions = [
        (10, 25, 30), (10, -25, 30), (10, 25, 30), (10, -25, 30)
    ]

    leg1 = RobotLeg(1, upper_leg_length, lower_leg_length, hip_to_shoulder, servos_from_leg1)
    leg2 = RobotLeg(2, upper_leg_length, lower_leg_length, hip_to_shoulder, servos_from_leg2)
    leg3 = RobotLeg(3, upper_leg_length, lower_leg_length, hip_to_shoulder, servos_from_leg3)
    leg4 = RobotLeg(4, upper_leg_length, lower_leg_length, hip_to_shoulder, servos_from_leg4)

    dog = RobotDog(leg1, leg2, leg3, leg4, startPositions)

    targets = [
        (10, 25, 30), (10, -25, 30), (10, 25, 30), (10, -25, 30)
    ]

    dog.start()
    dog.move_legs(targets, steps=10)


if __name__ == "__main__":
    main()
