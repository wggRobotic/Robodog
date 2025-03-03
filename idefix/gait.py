import math
from time import sleep
from typing import List

from idefix.robot_dog import RobotDog
from idefix.robot_leg import RobotLeg


class Gait:
    def __init__(self, dog: 'RobotDog'):
        self.dog = dog
        self.steps = 10  
        self.cycles = 3  # Number of complete cycles

    def walk(self, lin_x: float, lin_y: float, ang_z: float, step_length: float, step_height: float):
        gait_sequence = [0, 3, 1, 2]  # Order in which the legs move

        alpha = math.atan2(self.dog.body_width, self.dog.body_length)
        delta_y = math.cos(alpha) * ang_z
        delta_x = math.sin(alpha) * ang_z

        # Movement vectors for each leg
        vectors = [
            [lin_x - delta_x, lin_y + delta_y],  # Front Left (FL)
            [lin_x + delta_x, lin_y + delta_y],  # Front Right (FR)
            [lin_x - delta_x, lin_y - delta_y],  # Back Left (BL)
            [lin_x + delta_x, lin_y - delta_y]   # Back Right (BR)
        ]

        for _ in range(self.cycles):  # Perform a specific number of steps
            for leg_index in gait_sequence:
                leg = self.dog.legs[leg_index]
                x, y, z = leg.current_position  

                startposition = [x, y, z]  # Initial position
                endposition = [x + vectors[leg_index][0] * step_length, 
                               y + vectors[leg_index][1] * step_length, 
                               z]  # Target position
                midposition = [x, y, z + step_height]  # Mid-position below the current position

                # Mid → End (move the leg forward)
                self.interpolate_leg_movement(leg, midposition, endposition)

                # End → Mid (lower the leg)
                self.interpolate_leg_movement(leg, endposition, midposition)

                # Mid → Start (reset leg position)
                self.interpolate_leg_movement(leg, midposition, startposition)

    def interpolate_leg_movement(self, leg: 'RobotLeg', start, end):
        for t in range(self.steps):
            interp = [
                start[i] + (end[i] - start[i]) * (t / self.steps) for i in range(3)
            ]
            alpha, beta, gamma = leg.inverseKin(*interp)
            leg.move(alpha, beta, gamma)
            sleep(0.05)