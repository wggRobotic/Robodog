import math
from typing import Tuple

class robot_leg:  # Class names should typically be capitalized in Python
    def __init__(self, upper_leg_length: int, lower_leg_length: int, hip_to_shoulder: int):
        self.upper_leg_length = upper_leg_length
        self.lower_leg_length = lower_leg_length
        self.hip_to_shoulder = hip_to_shoulder

    def inverseKin1D(self, z: float) -> Tuple[float, float]:
        alpha = math.acos((self.upper_leg_length**2 + self.lower_leg_length**2 - z**2) / (2 * self.upper_leg_length * self.lower_leg_length))
        beta = math.acos((z**2 + self.lower_leg_length**2 - self.upper_leg_length**2) / (2 * z * self.lower_leg_length))
        return alpha, beta

    def inverseKin2D(self, x: float, z: float ) -> Tuple[float, float]:
        alpha, beta = self.inverseKin1D(math.sqrt(z**2 + x**2)) 
        beta += math.atan2(x,z) 
        return alpha, beta
    
    def inverseKin3D(self, x: float, y:float, z:float) -> Tuple[float, float, float]:
        alpha, beta = self.inverseKin2D(x, math.sqrt((y-self.hip_to_shoulder)**2 + z**2))
        beta +=math.pi/2
        gamma = math.atan2(y-self.hip_to_shoulder, x)
        return alpha, beta, gamma

def main():
    upper_leg_length = 108.5
    lower_leg_length = 136.0
    hip_to_shoulder = 10
    leg1 = robot_leg(10, 10, 10)
    x = 5.0
    y= 5.0
    z = 15.0
    alpha, beta, gamma = leg1.inverseKin3D(x,y,z)
    print("Alpha:", alpha)
    print("Beta:", beta)
    print("Gamma:", gamma)

if __name__ == "__main__":
    main()
