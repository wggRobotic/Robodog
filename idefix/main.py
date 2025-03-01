import sys
import time
import curses
import math

sys.path.append("..")
from idefix.servo_control import ServoControl
from idefix.robot_leg import RobotLeg
from idefix.robot_dog import RobotDog
from idefix.xbox_controller import XboxController
from idefix.robot_constants import *


def main():
    sc = ServoControl()
    controller = XboxController()
    leg0 = RobotLeg(
        0,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[0],
        LEGS_INTIAL_POSITIONS[0],
        sc,
    )
    leg1 = RobotLeg(
        1,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[1],
        LEGS_INTIAL_POSITIONS[1],
        sc,
    )
    leg2 = RobotLeg(
        2,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[2],
        LEGS_INTIAL_POSITIONS[2],
        sc,
    )
    leg3 = RobotLeg(
        3,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[3],
        LEGS_INTIAL_POSITIONS[3],
        sc
    )

    dog = RobotDog(BODY_LENGTH,BODY_WIDTH)
    # dog.move_legs(
    #     [
    #         [0.0,HIP_TO_SHOULDER  ,160.0],#0
    #         [0.0,HIP_TO_SHOULDER + 60.0 ,160.0],#1
    #         [0.0,-HIP_TO_SHOULDER - 60.0 ,160.0],#2
    #         [0.0,-HIP_TO_SHOULDER,160.0],#3
    #     ]
    # )
    #dog.pitch(27/180*math.pi)
    #dog.pitch(27/180*math.pi)

    #dog.roll(27/180*math.pi)
    #dog.roll(27/180*math.pi)

    # dog.yaw(27/180*math.pi)
    # dog.yaw(27/180*math.pi)



    #while True:
        # Read controller input for the left joystick Y-axis
        # ly_raw = controller.get_axis('ABS_Y')
        # ly = ServoControl.map_value(ly_raw, 0, 65535,-1 , 1)

        # # Apply a deadzone to ignore small movements
        # if abs(ly) < 0.2:
        #     ly = 0.0
        
    dog.pitch(math.pi/3)
    
   


        
        

   


if __name__ == "__main__":
    main()
