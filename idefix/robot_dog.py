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
                

    def roll(self, positions: List[List[float]], alpha: float):
        try:
            new_width = self.body_width * math.cos(abs(alpha))
            height_diff = math.sqrt(self.body_width**2 - new_width**2)
            y_offset = self.body_width - new_width

            #print(f"new_width: {new_width}, height_diff: {height_diff}, y_offset: {y_offset}")
            new_positions = []

            for i, position in enumerate(positions):
                x, y, z = position

                # Set height based on alpha's sign
                if i in [0, 2]:
                    height = z - height_diff if alpha > 0 else z + height_diff
                else:
                    height = z + height_diff if alpha > 0 else z - height_diff

                new_Z = height * math.cos(abs(alpha))
                #print(f"Leg {i} -> new_Z: {new_Z}")

                from_foot_to_shoulder = math.sqrt(max(0, y_offset**2 + height**2))
                #print(f"Leg {i} -> from_foot_to_shoulder: {from_foot_to_shoulder}")

                # Adjust Y based on alpha's sign
                delta_Y = math.sqrt(max(0, from_foot_to_shoulder**2 - new_Z**2))
                new_Y = y - delta_Y if alpha > 0 else y + delta_Y
                
                #print(f"Leg {i} -> new position: ({x}, {new_Y}, {new_Z})")
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
