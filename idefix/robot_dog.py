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
        angles = []
        
        for i in range(4):
            try:
                alpha, beta, gamma = self.legs[i].inverseKin(targets[i][0], targets[i][1], targets[i][2])
                if None in (alpha, beta, gamma):
                    print(f"Warning: Invalid target position for leg {i}: {targets[i]}")
                    return  
                angles.append((alpha, beta, gamma))
            except Exception as e:
                print(f"Error computing IK for leg {i}: {e}")
                return  
        
        for i in range(4):
            self.legs[i].move(*angles[i])
            self.legs[i].current_position = targets[i]



    def set_orientation(self):
        new_positions = []
        for i, leg in enumerate(self.legs):
            x,y,z = LEGS_INTIAL_POSITIONS[i]
            match leg.id:
                case 0:
                    new_x = x + self.current_pitch_x + self.current_yaw_x
                    new_y = y - self.current_roll_y + self.current_yaw_y
                    new_z = z - self.current_roll_z - self.current_pitch_z
                case 1:
                    new_x = x + self.current_pitch_x - self.current_yaw_x
                    new_y = y - self.current_roll_y + self.current_yaw_y
                    new_z = z + self.current_roll_z - self.current_pitch_z
                case 2:
                    new_x = x + self.current_pitch_x + self.current_yaw_x
                    new_y = y - self.current_roll_y - self.current_yaw_y
                    new_z = z - self.current_roll_z + self.current_pitch_z
                case 3:
                    new_x = x + self.current_pitch_x - self.current_yaw_x
                    new_y = y - self.current_roll_y - self.current_yaw_y
                    new_z = z + self.current_roll_z + self.current_pitch_z

            new_positions.append([new_x,new_y,new_z])
        self.move_legs(new_positions)
                

    def roll(self, alpha: float):
        try:
            delta_Y = 0.5 * self.body_width *( 1.0 - math.cos(alpha))
            delta_Z = math.sin(alpha) * 0.5 * self.body_width
            
            self.current_roll_y = delta_Y
            self.current_roll_z = delta_Z
            print(f"delta_Y:{delta_Y}, delta_Z: {delta_Z}")
        except Exception as e:
            print(f"Error in roll movement: {e}")

    def pitch(self, positions: List[List[float]], alpha: float):
        try:
            print(alpha/math.pi*180)
            new_length = self.body_length * math.cos(abs(alpha))
            height_diff = math.sqrt(self.body_length**2 - new_length**2)
            x_offset = self.body_length - new_length

            new_positions = []

            for i, position in enumerate(positions):
                x, y, z = position

                if i in [0, 1]:
                    height = z - height_diff if alpha > 0 else z + height_diff
                    world_X = x - x_offset 
                else:
                    height = z + height_diff if alpha > 0 else z - height_diff
                    world_X = x + x_offset

                new_Z = height * math.cos(abs(alpha))
                from_foot_to_shoulder = math.sqrt(max(0, (world_X)**2 + height**2))
                new_X = math.sqrt(max(0, from_foot_to_shoulder**2 - new_Z**2))
                new_positions.append([new_X, y, new_Z])
            return new_positions
            
        except Exception as e:
            print(f"Error in pitch movement: {e}")

    def yaw(self, alpha: float):
        try:
            alpha = alpha * 4
            delta_X = math.sin(alpha) * self.body_width * 0.5
            delta_Y = (math.cos(alpha)-1) * self.body_length * 0.5

            if (alpha < 0):
                delta_Y *= -1
            print(delta_X)
            print(delta_Y)
            self.current_yaw_x = delta_X
            self.current_yaw_y = delta_Y 

        except Exception as e:
            print(f"Error in yaw movement: {e}")
