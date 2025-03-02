import math
from typing import List
import numpy as np


from idefix.robot_leg import RobotLeg
from idefix.servo_control import ServoControl
from idefix.robot_constants import *

class RobotDog:

    def __init__(self, body_length: float, body_width: float):
        self.body_length = body_length
        self.body_width = body_width
        self.legs = []
        self.current_position = [0.0, 0.0, 0.0]
        self.current_rotation = [0.0, 0.0, 0.0]
        self.sc = ServoControl()

        for i in range(4):
            try:
                leg = RobotLeg(i, UPPER_LEG_LENGTH, LOWER_LEG_LENGTH, HIP_TO_SHOULDER, LEG_IDS[i], LEGS_INTIAL_POSITIONS[i], self.sc)
                self.legs.append(leg)
                angles = leg.inverseKin(*LEGS_INTIAL_POSITIONS[i])
                if None not in angles:
                    leg.move(*angles)
                else:
                    print(f"Warning: Invalid initial position for leg {i}")
            except Exception as e:
                print(f"Error initializing leg {i}: {e}")

    def move_legs(self, targets: List[List[float]]):
        for i in range(4):
            try:
                #print(f"Current_position leg{self.legs[i].id}: {self.legs[i].current_position}")
                alpha, beta, gamma = self.legs[i].inverseKin(targets[i][0], targets[i][1], targets[i][2])
                if None not in (alpha, beta, gamma):
                    self.legs[i].move(alpha, beta, gamma)
                    self.legs[i].current_position = targets[i]
                else:
                    print(f"Warning: Invalid target position for leg {i}: {targets[i]}")
            except Exception as e:
                print(f"Error moving leg {i}: {e}")
                

    def roll(self, positions:List[List[float]], alpha: float, z:float):
        try:
            new_width = self.body_width * math.cos(alpha)
            height_diff = math.sqrt(self.body_width**2 - new_width**2)
            y_offset = self.body_width - new_width
            new_positions = []
            for i, position in enumerate(positions):
                x, y, z = position
                match i:
                    case 0:
                        height = z - height_diff
                    case 1:
                        y_offset = z + height_diff
                    case 2:
                        y_offset = z - height_diff
                    case 3:
                        y_offset *= z + height_diff
    
                new_Z = height * math.cos(alpha)
                from_foot_to_shoulder = math.sqrt(y_offset**2 + height**2)
                new_Y = math.sqrt(from_foot_to_shoulder**2 - new_Z**2)
                new_positions.append([x, new_Y, new_Z])
            self.move_legs(new_positions)
        except Exception as e:
            print(f"Error in roll movement: {e}")

    def pitch(self, alpha: float):
        try:
            delta_X = 0.5 * self.body_length - 0.5 * self.body_length * math.cos(alpha)
            delta_Z = math.sin(alpha) * 0.5 * self.body_width

            self.current_pitch_x = delta_X
            self.current_pitch_z = delta_Z
            
        except Exception as e:
            print(f"Error in pitch movement: {e}")

    def yaw(self, alpha: float):
        try:
            alpha = alpha * 4
            delta_X = math.sin(alpha) * self.body_width * 0.5
            delta_Y = (math.cos(alpha)-1) * self.body_length * 0.5

            
            # if (abs(delta_Y) < 0.1): 
            #     self.current_yaw_x = 0.0
            #     self.current_yaw_y = 0.0
            #     return
            if (alpha < 0):
                delta_Y *= -1
            print(delta_X)
            print(delta_Y)
            self.current_yaw_x = delta_X
            self.current_yaw_y = delta_Y 

        except Exception as e:
            print(f"Error in yaw movement: {e}")
