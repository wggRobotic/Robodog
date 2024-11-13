import servo_control
from robot_dog import RobotDog
import curses

dog = None

#temporary input system
def kb_main(stdscr):
    global dog

    stdscr.nodelay(True)

    while True:
        key = stdscr.getch()

        if key == ord('+') or key == ord('-') or key == ord('w') or key == ord('s') or key == ord('a') or key == ord('d'):
            new_x: float = dog.legs[0].current_position[0]
            new_y: float = dog.legs[0].current_position[1]
            new_z: float = dog.legs[0].current_position[2]

            if key == ord('+'):
                new_z += 5
            if key == ord('-'):
                new_z -= 5
            if key == ord('w'):
                new_x -= 5
            if key == ord('s'):
                new_x += 5
            if key == ord('a'):
                new_y -= 5
            if key == ord('d'):
                new_y += 5
        
            dog.move_legs([[new_x, new_y, new_z], [new_x, new_y, new_z], [new_x, new_y, new_z], [new_x, new_y, new_z]])
            print(dog.legs[0].current_position[0], dog.legs[0].current_position[1], dog.legs[0].current_position[2])

        stdscr.refresh()


def main():
    global dog
    servo_control.servo_control_init()

    body_length: float = 100
    body_width: float = 100
    dog = RobotDog(body_length,body_width)

    curses.wrapper(kb_main)

if __name__ == "__main__":
    main()