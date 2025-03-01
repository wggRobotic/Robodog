import math
from typing import List

from idefix.robot_leg import RobotLeg
from idefix.servo_control import ServoControl
from idefix.robot_constants import *

class RobotDog:

    def __init__(self, body_length: float, body_width: float):
        self.body_length = body_length
        self.body_width = body_width
        self.legs = []
        self.current_pitch = 0.0
        self.current_yaw = 0.0
        self.current_roll = 0.0
        self.sc = ServoControl()

        for i in range(4):
            try:
                leg = RobotLeg(i, UPPER_LEG_LENGTH, LOWER_LEG_LENGTH, HIP_TO_SHOULDER, LEG_IDS[i], LEGS_INTIAL_POSITIONS[i], self.sc)
                self.legs.append(leg)
                angles = leg.inverseKin(*LEGS_INTIAL_POSITIONS[i])
                if None not in angles:
                    leg.move(*angles)
                else:
                    print(f"Warning: Invalid initial position for leg {i}")
            except Exception as e:
                print(f"Error initializing leg {i}: {e}")

    def move_legs(self, targets: List[List[float]]):
        for i in range(4):
            try:
                alpha, beta, gamma = self.legs[i].inverseKin(targets[i][0], targets[i][1], targets[i][2])
                if None not in (alpha, beta, gamma):
                    self.legs[i].move(alpha, beta, gamma)
                    self.legs[i].current_position = targets[i]
                else:
                    print(f"Warning: Invalid target position for leg {i}: {targets[i]}")
            except Exception as e:
                print(f"Error moving leg {i}: {e}")

    def roll(self, target_alpha: float):
        try:
            alpha = self.current_roll - target_alpha
            if abs(alpha) < 0.1:
                return
            delta_Y = 0.5 * self.body_width - 0.5 * self.body_width * math.cos(alpha)
            delta_Z = math.sin(alpha) * 0.5 * self.body_width
            new_positions = []

            for i, leg in enumerate(self.legs):
                x, y, z = leg.current_position
                if i in [0, 2]:  # left
                    z -= delta_Z
                else:  # right
                    z += delta_Z
                y += delta_Y
                new_positions.append([x, y, z])

            self.move_legs(new_positions)
            self.current_roll = target_alpha
        except Exception as e:
            print(f"Error in roll movement: {e}")

    def pitch(self, target_alpha: float):
        try:
            alpha = self.current_pitch - target_alpha
            if abs(alpha) < 0.1:
                return
            delta_X = 0.5 * self.body_length - 0.5 * self.body_length * math.cos(alpha)
            delta_Z = math.sin(alpha) * 0.5 * self.body_width
            new_positions = []

            for i, leg in enumerate(self.legs):
                x, y, z = leg.current_position
                if i in [0, 1]:  # front
                    z -= delta_Z
                else:  # back
                    z += delta_Z
                x += delta_X
                new_positions.append([x, y, z])

            self.move_legs(new_positions)
            self.current_pitch = target_alpha
        except Exception as e:
            print(f"Error in pitch movement: {e}")

    def yaw(self, target_alpha: float):
        try:
            target_alpha = 2 * (target_alpha + math.pi / 4)
            alpha = target_alpha - self.current_yaw
            if abs(alpha) < 0.1:
                return
            delta_X = math.sin(alpha) * self.body_width * 0.5
            delta_Y = math.cos(alpha) * self.body_length * 0.5
            new_positions = []

            for i, leg in enumerate(self.legs):
                x, y, z = leg.current_position
                match i:
                    case 0:
                        x -= delta_X
                        y += delta_Y
                    case 1:
                        x += delta_X
                        y += delta_Y
                    case 2:
                        x -= delta_X
                        y -= delta_Y
                    case 3:
                        x += delta_X
                        y -= delta_Y
                new_positions.append([x, y, z])

            self.move_legs(new_positions)
            self.current_yaw = target_alpha
        except Exception as e:
            print(f"Error in yaw movement: {e}")
