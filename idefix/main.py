import sys
import time
import curses
import math

sys.path.append("..")
from idefix.servo_control import ServoControl
from idefix.robot_leg import RobotLeg
from idefix.robot_dog import RobotDog
from idefix.robot_constants import *


def main():
    # i sneaked in :)
    sc = ServoControl()
    leg1 = RobotLeg(
        0,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[0],
        LEGS_INTIAL_VALUES[0],
        sc,
    )
    leg2 = RobotLeg(
        1,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[1],
        LEGS_INTIAL_VALUES[1],
        sc,
    )
    leg3 = RobotLeg(
        2,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[2],
        LEGS_INTIAL_VALUES[2],
        sc,
    )
    leg4 = RobotLeg(
        3,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[3],
        LEGS_INTIAL_VALUES[3],
        sc
    )

    x = 0.0
    y = HIP_TO_SHOULDER 
    z = 180.0

    alpha1, beta1, gamma1 = leg1.inverseKin3(x, y, z)
    leg1.move(2 * math.pi - alpha1, 1.5 * math.pi - beta1, 1.5 * math.pi - gamma1, 20)

    alpha2, beta2, gamma2 = leg2.inverseKin3(x, -y, z)
    leg2.move(alpha2,0.5* math.pi + beta2, 0.5 * math.pi + gamma2, 20)
    
    alpha3, beta3, gamma3 = leg3.inverseKin3(x, y, z)
    leg3.move(2 * math.pi - alpha3, 1.5 * math.pi - beta3, 0.5 * math.pi + gamma3, 20)

    alpha4, beta4, gamma4 = leg4.inverseKin3(x, -y, z)
    leg4.move(alpha4,0.5* math.pi +beta4, 1.5 * math.pi - gamma4, 20)


if __name__ == "__main__":
    main()
