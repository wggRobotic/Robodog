from typing import List, Tuple
from robot_leg import RobotLeg

class RobotDog:
    def __init__(self, leg1: RobotLeg, leg2: RobotLeg, leg3: RobotLeg, leg4: RobotLeg, startPositions: List[Tuple[float, float, float]]):
        self.legs = [leg1, leg2, leg3, leg4]
        self.startPositions = startPositions

    def start(self):
        try:
            for i in range(4):
                self.legs[i].move_leg(*self.startPositions[i])
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
