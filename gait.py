import math
from time import sleep
from typing import List

from robot_dog import RobotDog

class Gait:
    def __init__(self, dog: 'RobotDog'):
        # Initialize the gait with the RobotDog object
        self.dog = dog
        self.steps = 100  # Number of steps for a full movement

    def walk(self, step_length: float, step_height: float, speed: float):
        """
        Standard walking gait. Moves the dog forward with a certain step length and height.
        step_length: The length of each step the dog will take
        step_height: The height of the step (how high the leg will lift)
        speed: The speed of the movement (time per step)
        """
        for step in range(self.steps):
            for i, leg in enumerate(self.dog.legs):
                # Calculate the x and y position for each leg for a step
                x_position = step_length * math.cos(math.pi * step / self.steps)
                y_position = step_length * math.sin(math.pi * step / self.steps)
                
                # Z position changes with each step, creating a "up and down" motion
                z_position = step_height * math.sin(math.pi * step / self.steps)
                
                # Move the leg
                leg.move_leg(x_position, y_position, z_position)
            sleep(speed)

    def trot(self, step_length: float, step_height: float, speed: float):
        """
        Trot gait: The legs on the same side move together.
        This is faster than a walk and involves a more even movement pattern.
        """
        for step in range(self.steps):
            for i, leg in enumerate(self.dog.legs):
                # For trot, alternate the movement of the legs
                x_position = step_length * math.cos(math.pi * step / self.steps)
                y_position = step_length * math.sin(math.pi * step / self.steps)
                z_position = step_height * math.sin(math.pi * step / self.steps)
                
                if i % 2 == 0:
                    # Odd legs move in sync with each other
                    leg.move_leg(x_position, y_position, z_position)
                else:
                    # Even legs move in sync with each other
                    leg.move_leg(-x_position, -y_position, z_position)
            sleep(speed)

    def pace(self, step_length: float, step_height: float, speed: float):
        """
        Pace gait: Both legs on the same side move together, typically used for faster movements.
        """
        for step in range(self.steps):
            for i, leg in enumerate(self.dog.legs):
                # For pace, all legs on the same side move in sync
                x_position = step_length * math.cos(math.pi * step / self.steps)
                y_position = step_length * math.sin(math.pi * step / self.steps)
                z_position = step_height * math.sin(math.pi * step / self.steps)

                if i < 2:
                    # First two legs move together (left side)
                    leg.move_leg(x_position, y_position, z_position)
                else:
                    # Last two legs move together (right side)
                    leg.move_leg(-x_position, -y_position, z_position)
            sleep(speed)

    def turn(self, angle: float, step_length: float, step_height: float, speed: float):
        """
        Rotates the dog around the vertical axis (Z-axis) while walking.
        angle: The angle in degrees to rotate the dog
        step_length: The length of each step the dog will take
        step_height: The height of the step
        speed: Speed of the movement
        """
        # Convert angle to radians
        angle_rad = math.radians(angle)

        for step in range(self.steps):
            for i, leg in enumerate(self.dog.legs):
                # Calculate the x and y position for each leg
                x_position = step_length * math.cos(math.pi * step / self.steps)
                y_position = step_length * math.sin(math.pi * step / self.steps)
                
                # Rotate the position by the angle
                rotated_x = x_position * math.cos(angle_rad) - y_position * math.sin(angle_rad)
                rotated_y = x_position * math.sin(angle_rad) + y_position * math.cos(angle_rad)
                
                # Z position remains the same
                z_position = step_height * math.sin(math.pi * step / self.steps)
                
                # Move the leg to the new rotated position
                leg.move_leg(rotated_x, rotated_y, z_position)
            sleep(speed)
