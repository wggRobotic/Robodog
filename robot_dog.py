import math
from typing import List

from robot_leg import RobotLeg
import robot_constants as rc

class RobotDog:

    #mobes the legs to the specified positions relative to each hip joint
    def move_legs(self, targets: List[List[float]]):
        for i in range(4):
            alpha, beta, gamma = self.legs[i].inverseKinematics(targets[i][0], targets[i][1], targets[i][2])
            if alpha != None:
                self.legs[i].move(alpha, beta, gamma)
                self.legs[i].current_position = [targets[i][0], targets[i][1], targets[i][2]]                 

    def __init__(self, body_length:float, body_width:float):
        self.body_length = body_length
        self.body_width = body_width
        self.legs = []

        for i in range(4):
            self.legs.append(RobotLeg(i, rc.upper_leg_length, rc.lower_leg_length, rc.hip_to_shoulder, rc.leg_channels[i], rc.legs_initial_positions[i]))
            self.legs[i].move(*self.legs[i].inverseKinematics(*rc.legs_initial_positions[i]))
        

    def turn_body_X(self, alpha: float):#roll
        delta_Y = 0.5 * self.body_width - 0.5 * self.body_width * math.cos(alpha)
        delta_Z = math.sin(alpha) * 0.5 * self.body_width
        #modify the position of the legs
        self.move_legs()


    def turn_body_Y(self,alpha: float):#pitch
        delta_X = 0.5 * self.body_length - 0.5 * self.body_length * math.cos(alpha)
        delta_Z = math.sin(alpha) * 0.5 * self.body_width
        #modify the position of the legs
        self.move_legs()
        
    def turn_body_Z(self,alpha: float):#yaw
        delta_X = math.sin(alpha) * 0.5 * self.body_width
        delta_Y = math.cos(alpha) * 0.5 * self.body_length
        #modify the position of the legs
        self.move_legs()
        