import math
from typing import Tuple

import servo_control

class RobotLeg:
    def __init__(self, id:int, upper_leg_length: int, lower_leg_length: int, hip_to_shoulder: int, servos: Tuple[servo_control.Servo, servo_control.Servo, servo_control.Servo]):
        self.id = id
        self.upper_leg_length = upper_leg_length
        self.lower_leg_length = lower_leg_length
        self.hip_to_shoulder = hip_to_shoulder
        self.servos = servos

    def inverseKin1D(self, z: float) -> Tuple[float, float]:
        # Ensure the triangle inequality holds
        if z > (self.upper_leg_length + self.lower_leg_length) or z < abs(self.upper_leg_length - self.lower_leg_length):
            print("Invalid length for inverseKin1D.")
            return None, None

        cos_alpha = (self.upper_leg_length**2 + self.lower_leg_length**2 - z**2) / (2 * self.upper_leg_length * self.lower_leg_length)
        cos_beta  = (z**2 + self.lower_leg_length**2 - self.upper_leg_length**2) / (2 * z * self.lower_leg_length)

        # Check ranges for acos
        if cos_alpha < -1 or cos_alpha > 1:
            print(f"Invalid cos_alpha: {cos_alpha}")
            return None, None

        if cos_beta < -1 or cos_beta > 1:
            print(f"Invalid cos_beta: {cos_beta}")
            return None, None

        alpha = math.acos(cos_alpha)
        beta = math.acos(cos_beta)

        return alpha, beta

    def inverseKin2D(self, x: float, z: float) -> Tuple[float, float]:
        distance = math.sqrt(z**2 + x**2)
        alpha, beta = self.inverseKin1D(distance)
        if alpha is None or beta is None:
            return None, None

        beta += math.atan2(x, z)  # Adjusting beta for 2D position
        return alpha, beta
    
    def inverseKin3D(self, x: float, y: float, z: float) -> Tuple[float, float, float]:
        # Calculate distance in the horizontal plane from the hip to the foot
        distance = math.sqrt((y - self.hip_to_shoulder) ** 2 + z ** 2)
        alpha, beta = self.inverseKin2D(x, distance)
        if alpha is None or beta is None:
            return None, None, None
            
        # Set gamma based on the y position relative to hip_to_shoulder
        gamma = math.atan2(y - self.hip_to_shoulder, x)  # Angle around the vertical axis
        
        # Adjusting Angles for Mirrored Legs
        if(self.id % 2 == 0):
            alpha = math.pi - alpha
            beta = math.pi - beta
            gamma = math.pi - gamma
        
        return alpha, beta, gamma
    
    def move_leg(self, x: float, y: float, z: float):
        alpha, beta, gamma = self.inverseKin3D(x, y, z)
        if alpha is None or beta is None or gamma is None:
            return

        # Move the servos to the calculated angles
        self.servos[0].move_to_angle(gamma)
        self.servos[1].move_to_angle(beta)
        self.servos[2].move_to_angle(alpha)
        
def main():
    # Define the leg dimensions
    upper_leg_length = 108.5
    lower_leg_length = 136.0
    hip_to_shoulder = 50.0
    
    # Create an instance of the RobotLeg class
    leg1 = RobotLeg(upper_leg_length, lower_leg_length, hip_to_shoulder)
    
    # Test inputs for the inverse kinematics
    x = 0.0
    y = 50.0  # Adjusting y to be more realistic based on the hip height
    z = math.sqrt(lower_leg_length **2 + upper_leg_length**2)  # z should be positive to represent the upward height

    # Calculate the angles
    alpha, beta, gamma = leg1.inverseKin3D(x,y,z)

    print("Alpha (joint angle 1):", alpha/(2*math.pi)*360)
    print("Beta (joint angle 2):", beta/(2*math.pi)*360)
    print("Gamma (joint angle 3):", gamma/(2*math.pi)*360)

if __name__ == "__main__":
    main()
