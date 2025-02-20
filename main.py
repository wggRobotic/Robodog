import sys
import time
import curses
from servo_control import ServoControl
import robot_constants as robot_constants
from robot_leg import RobotLeg
from robot_dog import RobotDog
#from gait import Gait 

dog = None

# Temporary keyboard input system for manual control
def kb_main(stdscr):
    global dog
    stdscr.nodelay(True)

    while True:
        key = stdscr.getch()

        if key in [ord('+'), ord('-'), ord('w'), ord('s'), ord('a'), ord('d')]:
            new_x = dog.legs[0].current_position[0]
            new_y = dog.legs[0].current_position[1]
            new_z = dog.legs[0].current_position[2]

            if key == ord('+'):
                new_z += 5
            elif key == ord('-'):
                new_z -= 5
            elif key == ord('w'):
                new_x -= 5
            elif key == ord('s'):
                new_x += 5
            elif key == ord('a'):
                new_y -= 5
            elif key == ord('d'):
                new_y += 5

            dog.move_legs([[new_x, new_y, new_z]] * 4)
            print(f"Leg position: {new_x}, {new_y}, {new_z}")

        stdscr.refresh()


def main():
    #i sneaked in :)
    ServoControl
    global dog

    # Initialize servo control
    ServoControl()

    # Define body and leg dimensions
    body_length = 100
    body_width = 100
    upper_leg_length = 108.5
    lower_leg_length = 136.0
    hip_to_shoulder = robot_constants.hip_to_shoulder

    # Define servo channels for each leg
    servos_from_legs = [
        [13, 14, 15],  # Leg 1
        [0, 0, 0],     # Leg 2
        [0, 0, 0],     # Leg 3
        [0, 0, 0]      # Leg 4
    ]

    # Initial leg position
    start_position = (10, 25, 30)

    # Create the robot legs
    legs = [RobotLeg(i, upper_leg_length, lower_leg_length, hip_to_shoulder, servos_from_legs[i], start_position) for i in range(4)]

    # Create the robot dog object
    dog = RobotDog(body_length, body_width, legs)

    # Create a Gait object for movement control
    #gait = Gait(dog)

    # Read optional z-position from command-line arguments
    if len(sys.argv) > 1:
        z = float(sys.argv[1])
        dog.move_legs([[0, 0, z]] * 4, 1)

    # Uncomment to enable keyboard input for manual control
    # curses.wrapper(kb_main)


if __name__ == "__main__":
    main()
