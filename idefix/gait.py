import math
from time import sleep
from typing import List
import time

from idefix.robot_dog import RobotDog
from idefix.robot_leg import RobotLeg
from idefix.utilities import shift_columns


class Gait:
    def __init__(self, dog: "RobotDog"):
        self.dog = dog
        self.steps = 10
        self.cycles = 3  # Number of complete cycles

    def walk(
        self,
        lin_x: float,
        lin_y: float,
        ang_z: float,
        step_length: float,
        step_height: float,
        interpolation_steps: int,
    ):
        output = []
        
        gait_sequence = [0, 3, 1, 2]  # Order in which the legs move

        delta_x = lin_x / interpolation_steps
        delta_y = lin_y / interpolation_steps
        
        leg_positions_at_start = self.dog.get_leg_positions()

        # moves legs up
        position_sequence = []
        for i in range(1, interpolation_steps + 1):    
            new_positions = []
            for position in leg_positions_at_start:
                x, y, z = position
                z -= math.sin(math.pi * i / interpolation_steps) * step_height
                new_positions.append(
                    [
                        x - delta_x * interpolation_steps / 2 + delta_x * i,
                        y - delta_y * interpolation_steps / 2 + delta_y * i,
                        z,
                    ]
                )
            position_sequence.append(new_positions)

        # moves legs down
        for i in range(interpolation_steps * 3, 0, -1):
            
            leg_positions_at_start = self.dog.get_leg_positions()

            new_positions = []
            for position in leg_positions_at_start:
                x, y, z = position
                new_positions.append(
                    [
                        x
                        - delta_x * interpolation_steps / 2
                        + delta_x * (i / interpolation_steps * 3),
                        y
                        - delta_y * interpolation_steps / 2
                        + delta_y * (i / interpolation_steps * 3),
                        z,
                    ]
                )
            position_sequence.append(new_positions)
        # makes legs async
        shifted_push_back = shift_columns(
            position_sequence,
            [
                0,
                interpolation_steps * 3,
                interpolation_steps * 2,
                interpolation_steps * 1,
            ],
        )
        # inserts moments where all 4 legs are touching the ground
        for i in range(3, -1, -1):
            push = []
            
            for j, position in enumerate(shifted_push_back[i * interpolation_steps]):
                should_x, should_y, should_z = position
                is_x, is_y, is_z = self.dog.legs[j].current_position
                push.append([should_x, should_y, is_z])
            for i in range(3): # Todo: make this smarter with the frequency of the gait and also the step length instead of just using linX and linY
                shifted_push_back.insert(i * interpolation_steps, push)
                
                
        # handles that the mass is always in the middle of the legs, which touch the ground.
        for push in shifted_push_back:
            # finds the leg that is above the ground
            leg_index_above_the_ground = None
            for i, position in enumerate(push):
                x, y, z = position
                if  z < leg_positions_at_start[i][2]:
                    leg_index_above_the_ground = i
                    
            if leg_index_above_the_ground is not None:
                delta_x_sum = 0
                delta_y_sum = 0
                for i in range(4):
                    if i == leg_index_above_the_ground:
                        continue
                    else:
                        delta_x_sum += self.dog.calculate_delta_x(i, push[i])
                        delta_y_sum += self.dog.calculate_delta_y(i, push[i])
                delta_x_m = delta_x_sum / 3
                delta_y_m = delta_y_sum / 3
            output.append(self.dog.translation(delta_x_m, delta_y_m, 0, push))
                

        return output

    # Maybe there is a use case for this in the future
    def interpolate_leg_movement(self, leg: "RobotLeg", start, end):
        for t in range(self.steps):
            interp = [
                start[i] + (end[i] - start[i]) * (t / self.steps) for i in range(3)
            ]
            alpha, beta, gamma = leg.inverseKin(*interp)
            leg.move(alpha, beta, gamma)
            sleep(0.05)
