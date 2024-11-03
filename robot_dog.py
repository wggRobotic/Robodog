import math
from typing import List, Tuple

import servo_control
import robot_leg

class RobotDog:
    def __init__(self, leg1:robot_leg, leg2:robot_leg, leg3:robot_leg, leg4:robot_leg, startPositions: List[Tuple[float, float, float]]):
        self.legs = [leg1, leg2, leg3, leg4]
        self.startPositions = startPositions
    
    def start(self):
        for i in range(4):
            self.legs[i].move_leg(self.startPositions[i])


        
    def move_legs(self,targets: List[Tuple[float, float, float]],steps:int):
        for i in range(steps):
            for j in range(4):
                x,y,z = targets[j]
                self.legs[j].move_leg(x*(i/steps),y*(i/steps),z*(i/steps))
    
    
def main():
    # Define leg dimensions
    upper_leg_length = 108.5
    lower_leg_length = 136.0
    hip_to_shoulder = 50.0
    
    servos_from_leg1=[
        servo_control.ServoControl(1,0,math.pi),# Hip
        servo_control.ServoControl(2,0,math.pi),# Shoulder
        servo_control.ServoControl(3,0,math.pi),# Knee
    ]

    servos_from_leg2=[
        servo_control.ServoControl(4,0,math.pi),# Hip
        servo_control.ServoControl(5,0,math.pi),# Shoulder
        servo_control.ServoControl(6,0,math.pi),# Knee
    ]

    servos_from_leg3=[
        servo_control.ServoControl(7,0,math.pi),# Hip
        servo_control.ServoControl(8,0,math.pi),# Shoulder
        servo_control.ServoControl(9,0,math.pi),# Knee
    ]
    
    servos_from_leg4=[
        servo_control.ServoControl(10,0,math.pi),# Hip
        servo_control.ServoControl(11,0,math.pi),# Shoulder
        servo_control.ServoControl(12,0,math.pi),# Knee
    ]
    
    startPositions = [
        (10, 25, 50),  # Target for leg 1
        (10, -25, 50), # Target for leg 2
        (10, 25, 50), # Target for leg 3
        (10, -25, 50) # Target for leg 4
    ]
    
    #Create 4 RobotLegs
    leg1=robot_leg.RobotLeg(1,upper_leg_length,lower_leg_length,hip_to_shoulder,servos_from_leg1)
    leg2=robot_leg.RobotLeg(2,upper_leg_length,lower_leg_length,hip_to_shoulder,servos_from_leg2)
    leg3=robot_leg.RobotLeg(3,upper_leg_length,lower_leg_length,hip_to_shoulder,servos_from_leg3)
    leg4=robot_leg.RobotLeg(4,upper_leg_length,lower_leg_length,hip_to_shoulder,servos_from_leg4)
    # Create an instance of the robot_dog class

    dog = RobotDog(leg1,leg2,leg3,leg4)
    
    # Define target positions for each leg (x, y, z)
    targets = [
        (10, 25, 30),  # Target for leg 1
        (10, -25, 30), # Target for leg 2
        (10, 25, 30), # Target for leg 3
        (10, -25, 30) # Target for leg 4
    ]

    # Move all legs in parallel towards the targets in 10 steps
    dog.start()
    dog.move_legs(targets, steps=10)

if __name__ == "__main__":
    main()
