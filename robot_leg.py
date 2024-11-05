import math
from typing import List
import servo_control

class RobotLeg:
    def __init__(self, id: int, upper_leg_length: float, lower_leg_length: float, hip_to_shoulder: float,
                 servos: List[servo_control.Servo, servo_control.Servo, servo_control.Servo], 
                 start_position: List[float, float, float]):
        self.id = id
        self.upper_leg_length = upper_leg_length
        self.lower_leg_length = lower_leg_length
        self.hip_to_shoulder = hip_to_shoulder
        self.servos = servos
        self.current_position = start_position

    def inverseKin1D(self, z: float) -> List[float, float]:
        try:
            if z > (self.upper_leg_length + self.lower_leg_length) or z < abs(self.upper_leg_length - self.lower_leg_length):
                raise ValueError("Invalid length for inverseKin1D: does not satisfy triangle inequality.")

            cos_alpha = (self.upper_leg_length**2 + self.lower_leg_length**2 - z**2) / (2 * self.upper_leg_length * self.lower_leg_length)
            cos_beta = (z**2 + self.lower_leg_length**2 - self.upper_leg_length**2) / (2 * z * self.lower_leg_length)

            if not (-1 <= cos_alpha <= 1):
                raise ValueError(f"Invalid cos_alpha value: {cos_alpha}")
            if not (-1 <= cos_beta <= 1):
                raise ValueError(f"Invalid cos_beta value: {cos_beta}")

            alpha = math.acos(cos_alpha)
            beta = math.acos(cos_beta)
            return alpha, beta

        except ValueError as e:
            print(f"Error in inverseKin1D: {e}")
            return None, None

    def inverseKin2D(self, x: float, z: float) -> List[float, float]:
        try:
            distance = math.sqrt(z**2 + x**2)
            alpha, beta = self.inverseKin1D(distance)
            if alpha is None or beta is None:
                return None, None

            beta += math.atan2(x, z)
            return alpha, beta
        except Exception as e:
            print(f"Error in inverseKin2D: {e}")
            return None, None

    def inverseKin3D(self, x: float, y: float, z: float) -> List[float, float, float]:
        try:
            distance = math.sqrt((y - self.hip_to_shoulder) ** 2 + z ** 2)
            alpha, beta = self.inverseKin2D(x, distance)
            if alpha is None or beta is None:
                return None, None, None

            gamma = math.atan2(y - self.hip_to_shoulder, x)
            if self.id % 2 == 0:
                alpha = math.pi - alpha
                beta = math.pi - beta
                gamma = math.pi - gamma

            return alpha, beta, gamma
        except Exception as e:
            print(f"Error in inverseKin3D: {e}")
            return None, None, None

    def move_leg(self, x: float, y: float, z: float):
        try:
            alpha, beta, gamma = self.inverseKin3D(x, y, z)
            if alpha is None or beta is None or gamma is None:
                raise ValueError("Failed to calculate angles. Leg movement aborted.")

            self.servos[0].move_to_angle(gamma)
            self.servos[1].move_to_angle(beta)
            self.servos[2].move_to_angle(alpha)
            self.current_position = (x, y, z)
        except Exception as e:
            print(f"Error in move_leg for leg {self.id}: {e}")

