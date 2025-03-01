import math
from typing import List

from idefix.robot_leg import RobotLeg
from idefix.servo_control import ServoControl
from idefix.robot_constants import *

class RobotDog:

    def __init__(self, body_length:float, body_width:float):
        self.body_length = body_length
        self.body_width = body_width
        self.legs = []
        self.sc = ServoControl()

        for i in range(4):
            self.legs.append(RobotLeg(i, UPPER_LEG_LENGTH, LOWER_LEG_LENGTH, HIP_TO_SHOULDER, LEG_IDS[i], LEGS_INTIAL_POSITIONS[i],self.sc))
            self.legs[i].move(*self.legs[i].inverseKin(*LEGS_INTIAL_POSITIONS[i]))
        
    # Moves the legs to the specified positions relative to each hip joint
    def move_legs(self, targets: List[List[float]]):
        for i in range(4):
            alpha, beta, gamma = self.legs[i].inverseKin(targets[i][0], targets[i][1], targets[i][2])
            if alpha is not None:
                self.legs[i].move(alpha, beta, gamma)
                self.legs[i].current_position = targets[i]  

    def roll(self, alpha: float):  
        delta_Y = 0.5 * self.body_width - 0.5 * self.body_width * math.cos(alpha)
        delta_Z = math.sin(alpha) * 0.5 * self.body_width
        new_positions = []

        for i, leg in enumerate(self.legs):
            x, y, z = leg.current_position
            if i in [0, 2]:  # left
                z -= delta_Z
            else:  # right
                z += delta_Z
            y += delta_Y
            new_positions.append([x, y, z])

        self.move_legs(new_positions)

    def pitch(self, alpha: float):  
        delta_X = 0.5 * self.body_length - 0.5 * self.body_length * math.cos(alpha)
        delta_Z = math.sin(alpha) * 0.5 * self.body_width
        new_positions = []

        for i, leg in enumerate(self.legs):
            x, y, z = leg.current_position
            if i in [0, 1]:  # front
                z -= delta_Z
            else:  # back
                z += delta_Z
            x += delta_X
            new_positions.append([x, y, z])

        self.move_legs(new_positions)

    def yaw(self, alpha: float): 
        # Transform alpha to ensure alpha=0 corresponds to the neutral position
        # and positive/negative values rotate counterclockwise/clockwise.
        alpha = 2*(alpha+math.pi/4) 
        delta_X = math.sin(alpha)  * self.body_width * 0.5
        delta_Y = math.cos(alpha) * self.body_length * 0.5
        print(f"delta_x:{delta_X}, delta_y:{delta_Y}")
        new_positions = []
        
        for i, leg in enumerate(self.legs):
            x, y, z = leg.current_position
            print(f"Old Position for leg{i} is x:{x}, y:{y}, z:{z}") 
            if(abs(delta_Y) >0.1):       
                match i:
                    case 0:
                        x -= delta_X
                        y += delta_Y
                    case 1:
                        x += delta_X
                        y += delta_Y
                    case 2:
                        x -= delta_X
                        y -= delta_Y
                    case 3:
                        x += delta_X
                        y -= delta_Y
            print(f"New Position for leg{i} is x:{x}, y:{y}, z:{z}")        
            new_positions.append([x, y, z])

        self.move_legs(new_positions)
        