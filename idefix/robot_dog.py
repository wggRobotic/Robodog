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
        self.sc = ServoControl()

        for i in range(4):
            try:
                leg = RobotLeg(
                    i,
                    UPPER_LEG_LENGTH,
                    LOWER_LEG_LENGTH,
                    HIP_TO_SHOULDER,
                    LEG_IDS[i],
                    LEGS_INITIAL_POSITIONS[i],
                    self.sc,
                )
                self.legs.append(leg)
                angles = leg.inverseKin(*LEGS_INITIAL_POSITIONS[i])
                if None not in angles:
                    leg.move(*angles)
                else:
                    print(f"Warning: Invalid initial position for leg {i}")
            except Exception as e:
                print(f"Error initializing leg {i}: {e}")
                
    def calculate_delta_x(self,leg_id,position:List[float]):
        match leg_id:
            case 0:
                return self.body_length / 2 + position[0]
            case 1:
                return self.body_length / 2 + position[0] 
            case 2:
                return -1*self.body_length / 2 + position[0]
            case 3:
                return -1*self.body_length / 2 + position[0]
            
    def calculate_delta_y(self,leg_id,position:List[float]):
        match leg_id:
            case 0:
                return self.body_width / 2 + position[1]
            case 1:
                return -1*self.body_width / 2 + position[1]
            case 2:
                return self.body_width / 2 + position[1]
            case 3:
                return -1*self.body_width / 2 + position[1]

    def move_legs(self, targets: List[List[float]]):
        angles = []

        for i in range(4):
            try:
                # current_alpha,current_beta,current_gamma = self.legs[i].inverseKin(*self.legs[i].current_position)
                alpha, beta, gamma = self.legs[i].inverseKin(
                    targets[i][0], targets[i][1], targets[i][2]
                )
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

    def get_leg_positions(self) -> List[List[float]]:
        leg_positions = []
        for leg in self.legs:
            leg_positions.append(leg.current_position)
        return leg_positions

    def roll(self, alpha, position: List[List[float]]) -> List[List[float]]:
        delta_z = math.sin(alpha) * self.body_width / 2
        roll_positions = []
        # print(f"delata_z: {delta_z}, roll_positions: {roll_positions}")
        for i, leg in enumerate(self.legs):
            x, y, z = position[i]
            # print(f"Input_X: {x}, Input_Y: {y}, Input_Z: {z}")
            world_z1 = z - delta_z
            world_z2 = z + delta_z
            # print(f"worldZ1: {world_z1}, worldZ2: {world_z2}")
            match leg.id:
                case 0:
                    y_distance_world = self.body_width / 2 + y
                    # print(f"y_distance: {y_distance_world}")
                    g = y_distance_world - math.cos(alpha) * (self.body_width / 2)
                    # print(f"g: {g}")
                    d2 = math.sqrt(world_z2**2 + g**2)
                    # print(f"d2: {d2}")
                    beta2 = math.atan(g / world_z2)
                    # print(f"beta2: {beta2/math.pi*180}")
                    z = math.cos(alpha - beta2) * d2
                    y = -math.sin(alpha - beta2) * d2
                    roll_positions.append([x, y, z])
                case 1:
                    y_distance_world = self.body_width / 2 - y
                    # print(f"y_distance: {y_distance_world}")
                    g = y_distance_world - math.cos(alpha) * self.body_width / 2
                    # print(f"g: {g}")
                    d1 = math.sqrt(world_z1**2 + g**2)
                    # print(f"d1: {d1}")
                    beta1 = math.atan(g / world_z1)
                    # print(f"beta1: {beta1/math.pi*180}")
                    z = math.cos(alpha + beta1) * d1
                    y = -math.sin(alpha + beta1) * d1
                    roll_positions.append([x, y, z])
                case 2:
                    y_distance_world = self.body_width / 2 + y
                    g = y_distance_world - math.cos(alpha) * self.body_width / 2
                    d2 = math.sqrt(world_z2**2 + g**2)
                    beta2 = math.atan(g / world_z2)
                    z = math.cos(alpha - beta2) * d2
                    y = -math.sin(alpha - beta2) * d2
                    roll_positions.append([x, y, z])
                case 3:
                    y_distance_world = self.body_width / 2 - y
                    g = y_distance_world - math.cos(alpha) * self.body_width / 2
                    d1 = math.sqrt(world_z1**2 + g**2)
                    beta1 = math.atan(g / world_z1)
                    z = math.cos(alpha + beta1) * d1
                    y = -math.sin(alpha + beta1) * d1
                    roll_positions.append([x, y, z])

        return roll_positions

    def pitch(self, alpha, position: List[List[float]]) -> List[List[float]]:
        delta_z = math.sin(alpha) * self.body_length / 2
        pitch_positions = []
        # print(f"delta_z: {delta_z}, roll_positions: {pitch_positions}")
        for i, leg in enumerate(self.legs):
            x, y, z = position[i]
            # print(f"Input_X: {x}, Input_Y: {y}, Input_Z: {z}")
            world_z1 = z - delta_z
            world_z2 = z + delta_z
            # print(f"worldZ1: {world_z1}, worldZ2: {world_z2}")
            match leg.id:
                case 0:
                    x_distance_world = self.body_length / 2 + x
                    # print(f"y_distance: {x_distance_world}")
                    g = x_distance_world - math.cos(alpha) * (self.body_length / 2)
                    # print(f"g: {g}")
                    d2 = math.sqrt(world_z2**2 + g**2)
                    # print(f"d2: {d2}")
                    beta2 = math.atan(g / world_z2)
                    # print(f"beta2: {beta2/math.pi*180}")
                    z = math.cos(alpha - beta2) * d2
                    x = -math.sin(alpha - beta2) * d2
                    pitch_positions.append([x, y, z])
                case 2:
                    x_distance_world = self.body_length / 2 - x
                    # print(f"y_distance: {x_distance_world}")
                    g = x_distance_world - math.cos(alpha) * self.body_length / 2
                    # print(f"g: {g}")
                    d1 = math.sqrt(world_z1**2 + g**2)
                    # print(f"d1: {d1}")
                    beta1 = math.atan(g / world_z1)
                    # print(f"beta1: {beta1/math.pi*180}")
                    z = math.cos(alpha + beta1) * d1
                    x = -math.sin(alpha + beta1) * d1
                    pitch_positions.append([x, y, z])
                case 1:
                    x_distance_world = self.body_length / 2 + x
                    g = x_distance_world - math.cos(alpha) * self.body_length / 2
                    d2 = math.sqrt(world_z2**2 + g**2)
                    beta2 = math.atan(g / world_z2)
                    z = math.cos(alpha - beta2) * d2
                    x = -math.sin(alpha - beta2) * d2
                    pitch_positions.append([x, y, z])
                case 3:
                    x_distance_world = self.body_length / 2 - x
                    g = x_distance_world - math.cos(alpha) * self.body_length / 2
                    d1 = math.sqrt(world_z1**2 + g**2)
                    beta1 = math.atan(g / world_z1)
                    z = math.cos(alpha + beta1) * d1
                    x = -math.sin(alpha + beta1) * d1
                    pitch_positions.append([x, y, z])

        return pitch_positions

    def yaw(self, alpha, position: List[List[float]]) -> List[List[float]]:
        yaw_positions = []
        for i, leg in enumerate(self.legs):
            yaw_positions.append(self.yaw_just_one_single_leg(alpha,position[i],i))
        return yaw_positions
    
    def yaw_just_one_single_leg(self, alpha, position: List[float], leg_id:int) -> List[float]:
        x, y, z = position
        match leg_id:
                case 0:
                    x_distance = self.body_length / 2 + x
                    y_distance = self.body_width / 2 + y
                    yaw_angle1 = math.atan2(y_distance, x_distance)
                    radius = math.sqrt(x_distance**2 + y_distance**2)
                    yaw_angle2 = yaw_angle1 + alpha
                    new_x = radius * math.cos(yaw_angle2) - self.body_length / 2
                    new_y = radius * math.sin(yaw_angle2) - self.body_width / 2
                    return [new_x, new_y, z]
                case 1:
                    x_distance = self.body_length / 2 + x
                    y_distance = self.body_width / 2 - y
                    yaw_angle1 = math.atan2(y_distance, x_distance)
                    radius = math.sqrt(x_distance**2 + y_distance**2)
                    yaw_angle2 = yaw_angle1 - alpha
                    new_x = radius * math.cos(yaw_angle2) - self.body_length / 2
                    new_y = radius * math.sin(yaw_angle2) * -1 + self.body_width / 2
                    return [new_x, new_y, z]
                case 2:
                    x_distance = self.body_length / 2 - x
                    y_distance = self.body_width / 2 + y
                    yaw_angle1 = math.atan2(y_distance, x_distance)
                    radius = math.sqrt(x_distance**2 + y_distance**2)
                    yaw_angle2 = yaw_angle1 - alpha
                    new_x = radius * math.cos(yaw_angle2) * -1 + self.body_length / 2
                    new_y = radius * math.sin(yaw_angle2) - self.body_width / 2
                    return [new_x, new_y, z]

                case 3:
                    x_distance = self.body_length / 2 - x
                    y_distance = self.body_width / 2 - y
                    yaw_angle1 = math.atan2(y_distance, x_distance)
                    radius = math.sqrt(x_distance**2 + y_distance**2)
                    yaw_angle2 = yaw_angle1 + alpha
                    new_x = radius * math.cos(yaw_angle2) * -1 + self.body_length / 2
                    new_y = radius * math.sin(yaw_angle2) * -1 + self.body_width / 2
                    return [new_x, new_y, z]
    
    def translation(self, x_offset, y_offset, z_offset, positions:List[List[float]]) -> List[List[float]]:
        new_positions = []
        for i, leg in enumerate(self.legs):
            x, y, z = positions[i]
            new_positions.append([x + x_offset, y + y_offset, z + z_offset])
        return new_positions
        
