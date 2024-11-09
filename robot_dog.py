import math
from typing import List

from robot_leg import RobotLeg

class RobotDog:
    def __init__(self, body_length:float, body_width:float, legs: List[RobotLeg]):
        self.body_length = body_length
        self.body_width = body_width
        self.legs = legs
        self.positions = [legs[0].current_position,legs[1].current_position,legs[2].current_position,legs[3].current_position]


    def move_legs(self, targets: List[List[float]], steps: int):
        try:
            for i in range(1, steps + 1):
                for j in range(4):
                    x, y, z = targets[j]
                    self.legs[j].move_leg(x * (i / steps), y * (i / steps), z * (i / steps))
                    self.positions[j] = [x * (i / steps), y * (i / steps), z * (i / steps)]
        except Exception as e:
            print(f"Error in move_legs: {e}")

    def turn_body_X(self, alpha: float):#roll
        delta_Y = 0.5 * self.body_width - 0.5 * self.body_width * math.cos(alpha)
        delta_Z = math.sin(alpha) * 0.5 * self.body_width
        #modify the position of the legs
        self.move_legs()


    def turn_body_Y(self,alpha: float):#pitch
        delta_X = 0.5 * self.body_length - 0.5 * self.body_length * math.cos(alpha)
        delta_Z = math.sin(alpha) * 0.5 * self.body_width
        #modify the position of the legs
        self.move_legs()
        
    def turn_body_Z(self,alpha: float):#yaw
        delta_X = math.sin(alpha) * 0.5 * self.body_width
        delta_Y = math.cos(alpha) * 0.5 * self.body_length
        #modify the position of the legs
        self.move_legs()
        