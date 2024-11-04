import math
from typing import List, Tuple

from robot_leg import RobotLeg

class RobotDog:
    def __init__(self, body_length:float, body_width:float, leg1: RobotLeg, leg2: RobotLeg, leg3: RobotLeg, leg4: RobotLeg, startPositions: List[Tuple[float, float, float]]):
        self.body_length = body_length
        self.body_width = body_width
        self.legs = [leg1, leg2, leg3, leg4]
        self.Positions = startPositions

    def update(self):
        try:
            for i in range(4):
                self.legs[i].move_leg(*self.Positions[i])
        except Exception as e:
            print(f"Error in start: {e}")

    def move_legs(self, targets: List[Tuple[float, float, float]], steps: int):
        try:
            for i in range(steps):
                for j in range(4):
                    x, y, z = targets[j]
                    self.legs[j].move_leg(x * (i / steps), y * (i / steps), z * (i / steps))
        except Exception as e:
            print(f"Error in move_legs: {e}")

    def turn_body_X(self, alpha: float):
        a = math.sin(alpha) * 0.5 * self.body_length
        #left add right substract
        self.Positions[0][2] = self.Positions[0][2] + a
        self.Positions[1][2] = self.Positions[1][2] - a
        self.Positions[2][2] = self.Positions[2][2] + a
        self.Positions[3][2] = self.Positions[3][2] - a
        self.update()


    def turn_body_Y(self,alpha: float):
        a = math.sin(alpha) * 0.5 * self.body_width
        #front add back substract
        self.Positions[0][2] = self.Positions[0][2] + a
        self.Positions[1][2] = self.Positions[1][2] + a
        self.Positions[2][2] = self.Positions[2][2] - a
        self.Positions[3][2] = self.Positions[3][2] - a
        self.update()
        
    def turn_body_Z(self,alpha: float):
        delta_X = math.sin(alpha) * 0.5 * self.body_width
        delta_Y = math.cos(alpha) * 0.5 * self.body_length

        self.Positions[0][0] = self.Positions[0][0] - delta_X
        self.Positions[1][0] = self.Positions[1][0] + delta_X
        self.Positions[2][0] = self.Positions[2][0] - delta_X
        self.Positions[3][0] = self.Positions[3][0] + delta_X
        
        self.Positions[0][1] = self.Positions[0][1] + delta_Y 
        self.Positions[1][1] = self.Positions[1][1] - delta_Y
        self.Positions[2][1] = self.Positions[2][1] - delta_Y
        self.Positions[3][1] = self.Positions[3][1] + delta_Y
        