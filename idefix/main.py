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
    #i sneaked in :)
    sc = ServoControl()
    leg1 = RobotLeg(0,UPPER_LEG_LENGTH,LOWER_LEG_LENGTH,HIP_TO_SHOULDER,LEG_IDS[0],LEGS_INTIAL_VALUES[0],sc)
    leg2 = RobotLeg(0,UPPER_LEG_LENGTH,LOWER_LEG_LENGTH,HIP_TO_SHOULDER,LEG_IDS[2],LEGS_INTIAL_VALUES[2],sc)
    
    
    # alpha, beta = leg1.inverseKin1(140.0)
    # leg1.move(2*math.pi - alpha, math.pi + math.pi/2 -beta, math.pi)
    
    # alpha, beta = leg1.inverseKin2(150.0,0.0)
    # leg1.move(2*math.pi - alpha, math.pi + math.pi/2 -beta, math.pi)
    
    alpha1, beta1, gamma1 = leg1.inverseKin3(10.0,HIP_TO_SHOULDER + 100.0,100.0)
    leg1.move(2*math.pi - alpha1, math.pi + math.pi/2 -beta1,math.pi+math.pi/2 -gamma1)

    alpha2, beta2, gamma2 = leg2.inverseKin3(10.0,HIP_TO_SHOULDER + 100.0,100.0)
    leg2.move(2*math.pi - alpha2, math.pi + math.pi/2 -beta2,math.pi/2+gamma2)
    
    
    
    

if __name__ == "__main__":
    main()
