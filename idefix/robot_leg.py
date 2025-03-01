import math
from typing import List
import numpy as np

from idefix.servo_control import*


class RobotLeg:
    def __init__(self, id: int, upper_leg_length: float, lower_leg_length: float, hip_to_shoulder: float,
                 servo_ids: List[int],
                 initial_position: List[float],sc: ServoControl):
        self.id = id
        self.upper_leg_length = upper_leg_length
        self.lower_leg_length = lower_leg_length
        self.hip_to_shoulder = hip_to_shoulder
        self.current_position = initial_position
        self.servo_ids = servo_ids
        self.sc = sc

    #angle calculations and actual moving functions are separated so cases where some legs are out of bounds can be handled
    #self.current_position has to be set manually
    
    def inverseKin(self, x: float, y: float, z: float) -> List[float]:
        try:
            # Validate that input values are numeric
            if not all(isinstance(val, (int, float)) for val in [x, y, z]):
                raise ValueError("All input values must be numeric.")

            # Mirror the y-coordinate based on the ID
            if (self.id % 2) != 0:
                y = -y

            # Calculate the distance from the shoulder to the foot
            shoulder_to_foot_squared = z**2 + y**2 - self.hip_to_shoulder**2
            if shoulder_to_foot_squared < 0:
                raise ValueError("The combination of y, z, and hip_to_shoulder results in an invalid square root calculation.")

            shoulder_to_foot = math.sqrt(shoulder_to_foot_squared)

            # Calculate angles gamma1 and gamma2
            gamma1 = math.atan2(y, z)
            gamma2 = math.atan2(shoulder_to_foot, self.hip_to_shoulder)

            # Calculate the distance and angle delta_beta
            distance_squared = x**2 + shoulder_to_foot**2
            if distance_squared < 0:
                raise ValueError("The combination of x and shoulder_to_foot results in an invalid square root calculation.")

            distance = math.sqrt(distance_squared)
            delta_beta = math.atan2(x, shoulder_to_foot)

            # Validate arguments for math.acos
            acos_arg1 = (self.upper_leg_length**2 + self.lower_leg_length**2 - distance**2) / (2 * self.upper_leg_length * self.lower_leg_length)
            acos_arg2 = (self.upper_leg_length**2 - self.lower_leg_length**2 + distance**2) / (2 * self.upper_leg_length * distance)

            if not (-1 <= acos_arg1 <= 1):
                raise ValueError("Invalid argument for math.acos in the calculation of alpha. leg_id:{self.id}")
            if not (-1 <= acos_arg2 <= 1):
                raise ValueError("Invalid argument for math.acos in the calculation of beta. leg_id:{self.id}")

            # Calculate angles alpha, beta, and gamma
            alpha = math.acos(acos_arg1)
            beta = math.acos(acos_arg2) - delta_beta
            gamma = gamma1 + gamma2

            return [alpha, beta, gamma]

        except ValueError as e:
            print(f"Error in inverse kinematics calculation: {e} leg_id:{self.id}")
            return [None, None, None]
        except Exception as e:
            print(f"An unexpected error occurred: {e} leg_id:{self.id}")
            return [None, None, None]
        

    def move(self, ellbow_angle: float, shoulder_angle: float, hip_angle: float):
            match self.id:
                case 0: 
                    ellbow_angle = 2 * math.pi - ellbow_angle
                    shoulder_angle = 1.5 * math.pi - shoulder_angle
                    hip_angle = 1.5 * math.pi - hip_angle
                case 1:
                    ellbow_angle = ellbow_angle
                    shoulder_angle = 0.5 * math.pi + shoulder_angle
                    hip_angle = 0.5 * math.pi + hip_angle
                case 2:
                    ellbow_angle = 2 * math.pi - ellbow_angle
                    shoulder_angle = 1.5 * math.pi - shoulder_angle
                    hip_angle = 0.5 * math.pi + hip_angle
                case 3:
                    ellbow_angle = ellbow_angle
                    shoulder_angle = 0.5 * math.pi + shoulder_angle
                    hip_angle = 1.5 * math.pi - hip_angle

            self.sc.set_pos(self.servo_ids[0], ellbow_angle)
            self.sc.set_pos(self.servo_ids[1], shoulder_angle)
            self.sc.set_pos(self.servo_ids[2], hip_angle)
            self.sc.move_positions()