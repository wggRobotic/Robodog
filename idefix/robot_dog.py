import math
from typing import List

from idefix.robot_leg import RobotLeg
from idefix.robot_constants import *

class RobotDog:

    def __init__(self, body_length:float, body_width:float):
        self.body_length = body_length
        self.body_width = body_width
        self.legs = []

        for i in range(4):
            self.legs.append(RobotLeg(i, upper_leg_length, lower_leg_length, hip_to_shoulder, leg_ids[i], legs_initial_positions[i]))
            self.legs[i].move(*self.legs[i].inverseKinematics(*legs_initial_positions[i]))
        
    # Moves the legs to the specified positions relative to each hip joint
    def move_legs(self, targets: List[List[float]]):
        for i in range(4):
            alpha, beta, gamma = self.legs[i].inverseKinematics(targets[i][0], targets[i][1], targets[i][2])
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
        delta_X = math.sin(alpha) * 0.5 * self.body_width
        delta_Y = math.cos(alpha) * 0.5 * self.body_length
        new_positions = []

        for i, leg in enumerate(self.legs):
            x, y, z = leg.current_position
            if i in [0, 3]:  
                x += delta_X
                y += delta_Y
            else:   
                x -= delta_X
                y -= delta_Y
            new_positions.append([x, y, z])

        self.move_legs(new_positions)
        