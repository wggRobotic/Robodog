import servo_control
from robot_dog import RobotDog
import curses

dog = None

z: float = 200

def kb_main(stdscr):
    global dog
    global z

    stdscr.nodelay(True)

    while True:
        key = stdscr.getch()

        if key == ord('+') or key == ord('-'):
            new_z: float = z
            if key == ord('+'):
                new_z += 10
            if key == ord('-'):
                new_z -= 10
            
            print(new_z)
            alpha, beta, gamma = dog.legs[0].inverseKinematics(0, 0, new_z)

            print(f"{alpha} {beta} {gamma}")

            if alpha != None: 
                z = new_z
                dog.legs[0].move(alpha, beta, gamma)
                
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