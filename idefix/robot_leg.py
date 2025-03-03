import math
from typing import List
from idefix.servo_control import *

class RobotLeg:
    def __init__(self, id: int, upper_leg_length: float, lower_leg_length: float, hip_to_shoulder: float,
                 servo_ids: List[int], initial_position: List[float], sc: ServoControl):
        self.id = id
        self.upper_leg_length = upper_leg_length
        self.lower_leg_length = lower_leg_length
        self.hip_to_shoulder = hip_to_shoulder
        self.current_position = initial_position
        self.servo_ids = servo_ids
        self.sc = sc

    def inverseKin(self, x: float, y: float, z: float) -> List[float]:
        try:
            if not all(isinstance(val, (int, float)) for val in [x, y, z]):
                raise TypeError("All input values must be numeric.")
            if self.upper_leg_length <= 0 or self.lower_leg_length <= 0:
                raise ValueError("Leg segment lengths must be positive.")

            if (self.id % 2) != 0:
                y = -y

            shoulder_to_foot_squared = z**2 + y**2 - self.hip_to_shoulder**2
            if shoulder_to_foot_squared < 0:
                raise ValueError("Invalid square root calculation in shoulder_to_foot.")
            shoulder_to_foot = math.sqrt(shoulder_to_foot_squared)

            gamma1 = math.atan2(y, z)
            gamma2 = math.atan2(shoulder_to_foot, self.hip_to_shoulder)

            distance_squared = x**2 + shoulder_to_foot**2
            if distance_squared < 0:
                raise ValueError("Invalid square root calculation in distance.")
            distance = math.sqrt(distance_squared)
            delta_beta = math.atan2(x, shoulder_to_foot)

            acos_arg1 = (self.upper_leg_length**2 + self.lower_leg_length**2 - distance**2) / (2 * self.upper_leg_length * self.lower_leg_length)
            acos_arg2 = (self.upper_leg_length**2 - self.lower_leg_length**2 + distance**2) / (2 * self.upper_leg_length * distance)

            if not (-1 <= acos_arg1 <= 1):
                raise ValueError(f"Invalid acos argument for alpha: {acos_arg1} (Leg ID: {self.id})")
            if not (-1 <= acos_arg2 <= 1):
                raise ValueError(f"Invalid acos argument for beta: {acos_arg2} (Leg ID: {self.id})")

            alpha = math.acos(acos_arg1)
            beta = math.acos(acos_arg2) - delta_beta
            gamma = gamma1 + gamma2

            return [alpha, beta, gamma]

        except (ValueError, TypeError) as e:
            print(f"Error in inverse kinematics: {e} (Leg ID: {self.id})")
            return [None, None, None]
        except Exception as e:
            print(f"Unexpected error: {e} (Leg ID: {self.id})")
            return [None, None, None]


    def move(self, elbow_angle: float, shoulder_angle: float, hip_angle: float):
        try:
            if None in [elbow_angle, shoulder_angle, hip_angle]:
                raise ValueError("Received None values for angles.")
            
            match self.id:
                case 0:
                    elbow_angle = 2 * math.pi - elbow_angle
                    shoulder_angle = 1.5 * math.pi - shoulder_angle
                    hip_angle = 1.5 * math.pi - hip_angle
                case 1:
                    shoulder_angle += 0.5 * math.pi
                    hip_angle += 0.5 * math.pi
                case 2:
                    elbow_angle = 2 * math.pi - elbow_angle
                    shoulder_angle = 1.5 * math.pi - shoulder_angle
                    hip_angle += 0.5 * math.pi
                case 3:
                    shoulder_angle += 0.5 * math.pi
                    hip_angle = 1.5 * math.pi - hip_angle
                
            for servo_id, angle in zip(self.servo_ids, [elbow_angle, shoulder_angle, hip_angle]):
                if not (0 <= angle <= 2 * math.pi):
                    raise ValueError(f"Angle out of range: {angle} (Leg ID: {self.id})")
                self.sc.set_pos(servo_id, angle)
            
            self.sc.move_positions()
        except ValueError as e:
            print(f"Error in move: {e} (Leg ID: {self.id})")
        except Exception as e:
            print(f"Unexpected error in move: {e} (Leg ID: {self.id})")