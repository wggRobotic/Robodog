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

    
    def calculate_shift_from_gait_sequence(self, gait_sequence):
        shift = [0] * len(gait_sequence)

        for i, value in enumerate(gait_sequence):
            shift[value] = (
                i  # Store the index of the value at its respective position in the gait sequence
            )

        return shift

    def walk(
        self,
        lin_x: float,
        lin_y: float,
        ang_z: float,
        step_length: float,
        step_height: float,
        interpolation_steps: int,
    ):
        gait_sequence = [0, 3, 1, 2]  # Order in which the legs move

        position_sequence = []

        delta_x = lin_x / 8
        delta_y = lin_y / 8

        # moves legs up
        for i in range(1, interpolation_steps + 1):
            print(i)

            leg_positions = self.dog.get_leg_positions()
            new_positions = []
            for position in leg_positions:
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
            print(i)
            leg_positions = self.dog.get_leg_positions()

            new_positions = []
            for position in leg_positions:
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
            shifted_push_back.insert(i * interpolation_steps, push)
            shifted_push_back.insert(i * interpolation_steps, push)
            shifted_push_back.insert(i * interpolation_steps, push)


        return shifted_push_back

    # Maybe there is a use case for this in the future
    def interpolate_leg_movement(self, leg: "RobotLeg", start, end):
        for t in range(self.steps):
            interp = [
                start[i] + (end[i] - start[i]) * (t / self.steps) for i in range(3)
            ]
            alpha, beta, gamma = leg.inverseKin(*interp)
            leg.move(alpha, beta, gamma)
            sleep(0.05)
