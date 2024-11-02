import robot_leg
from typing import List, Tuple
import math

class robot_dog:
    def __init__(self, upper_leg_length: int, lower_leg_length: int, hip_to_shoulder: int):
        self.legs = [
            robot_leg.RobotLeg(upper_leg_length, lower_leg_length, hip_to_shoulder),  # leg 1
            robot_leg.RobotLeg(upper_leg_length, lower_leg_length, hip_to_shoulder),  # leg 2
            robot_leg.RobotLeg(upper_leg_length, lower_leg_length, hip_to_shoulder),  # leg 3
            robot_leg.RobotLeg(upper_leg_length, lower_leg_length, hip_to_shoulder)   # leg 4
        ]

    def move_legs(self, targets: List[Tuple[float, float, float]], steps: int) -> None:
        # Check if we have 4 targets for the 4 legs
        if len(targets) != 4:
            raise ValueError("Exactly 4 target positions required for the legs.")

        # Store the initial positions of the legs
        initial_positions = [(0.0, 0.0, 0.0) for _ in range(4)]  # Assuming starting at (0, 0, 0)

        for step in range(steps + 1):
            # Calculate the interpolated position for each leg
            interpolated_positions = [
                (
                    initial_positions[i][0] + (targets[i][0] - initial_positions[i][0]) * (step / steps),
                    initial_positions[i][1] + (targets[i][1] - initial_positions[i][1]) * (step / steps),
                    initial_positions[i][2] + (targets[i][2] - initial_positions[i][2]) * (step / steps),
                ) for i in range(4)
            ]

            # Calculate joint angles for each leg based on the interpolated positions
            for leg, target in zip(self.legs, interpolated_positions):
                x, y, z = target
                alpha, beta, gamma = leg.inverseKin3D(x, y, z)

                # Print or store the angles for each step
                print(f"Leg target: {target} -> Angles: Alpha: {alpha/(2*math.pi)*360}, Beta: {beta/(2*math.pi)*360}, Gamma: {gamma/(2*math.pi)*360}")

def main():
    # Define leg dimensions
    upper_leg_length = 136.0
    lower_leg_length = 136.0
    hip_to_shoulder = 50.0
    
    # Create an instance of the robot_dog class
    dog = robot_dog(upper_leg_length, lower_leg_length, hip_to_shoulder)
    
    # Define target positions for each leg (x, y, z)
    targets = [
        (10, 25, 50),  # Target for leg 1
        (10, -25, 50), # Target for leg 2
        (-10, 25, 50), # Target for leg 3
        (-10, -25, 50) # Target for leg 4
    ]

    # Move all legs in parallel towards the targets in 10 steps
    dog.move_legs(targets, steps=10)

if __name__ == "__main__":
    main()
