import sys
import time
import curses
import math
import board

sys.path.append("..")
from idefix.servo_control import ServoControl
from idefix.robot_leg import RobotLeg
from idefix.robot_dog import RobotDog
from idefix.gait import Gait
from idefix.xbox_controller import XboxController
from idefix.robot_constants import *
from idefix.imu import IMU


def main():
    sc = ServoControl()
    controller = XboxController()
    leg0 = RobotLeg(
        0,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[0],
        LEGS_INITIAL_POSITIONS[0],
        sc,
    )
    leg1 = RobotLeg(
        1,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[1],
        LEGS_INITIAL_POSITIONS[1],
        sc,
    )
    leg2 = RobotLeg(
        2,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[2],
        LEGS_INITIAL_POSITIONS[2],
        sc,
    )
    leg3 = RobotLeg(
        3,
        UPPER_LEG_LENGTH,
        LOWER_LEG_LENGTH,
        HIP_TO_SHOULDER,
        LEG_IDS[3],
        LEGS_INITIAL_POSITIONS[3],
        sc,
    )

    dog = RobotDog(BODY_LENGTH, BODY_WIDTH)
    # dog.move_legs(
    #     [
    #         [0.0,HIP_TO_SHOULDER +50.0 ,160.0],#0
    #         [0.0,-HIP_TO_SHOULDER +50.0,160.0],#1
    #         [0.0,HIP_TO_SHOULDER +50.0,160.0],#2
    #         [0.0,-HIP_TO_SHOULDER +50.0,160.0],#3
    #     ], 5
    # )
    i2c = board.I2C()
    imu = IMU(i2c, window_size=3, threshold=120.0)
    g = Gait(dog)
    old_ly = 0.0
    old_lx = 0.0
    old_rz = 0.0
    a_lock = False
    b_lock = False
    active = True

    deadzone = 0.2

    # while True:
    #     # Read controller input for the left joystick Y-axis
    #     ly_raw = controller.get_axis('ABS_Y')
    #     a = controller.get_button('BTN_SOUTH')
    #     b = controller.get_button('BTN_EAST')
    #     lx_raw = controller.get_axis('ABS_X')
    #     z_raw = controller.get_axis('ABS_Z')

    #     ly = ServoControl.map_value(ly_raw, 0, 65535, -1, 1)
    #     lx = ServoControl.map_value(lx_raw, 0, 65535, -1, 1)
    #     rz = ServoControl.map_value(z_raw, 0, 65535, -1, 1)

    #     # Apply a deadzone to ignore small movements
    #     if abs(ly) < deadzone:
    #         ly = 0.0
    #     if abs(lx) < deadzone:
    #         lx = 0.0
    #     if abs(rz) < deadzone:
    #         rz = 0.0

    #     yaw_positions = dog.yaw2(rz*20/180*math.pi,LEGS_INTIAL_POSITIONS)
    #     roll_position = dog.roll2(lx*60/180*math.pi, yaw_positions)
    #     pitch_positions = dog.pitch2(ly*40/180*math.pi, roll_position)
    #     if (active):
    #         dog.move_legs(pitch_positions)

    #     # Emergency stop ;)
    #     if(a==1 and not a_lock):
    #         a_lock = True
    #         active = True
    #         for leg in dog.legs:
    #             leg.deactivate_leg(True)
    #         a_lock = False

    #     if(b==1 and not b_lock):
    #         b_lock = True
    #         active = False
    #         for leg in dog.legs:
    #             leg.deactivate_leg(False)
    #         b_lock = False

    #     time.sleep(0.1)
    #pitch_pos = dog.pitch(-2 / 180 * math.pi, LEGS_INITIAL_POSITIONS)
    #dog.move_legs(pitch_pos)
    # push_back = g.walk(50.0, 0.0, 0.0, 2.0, 30.0,8)
    # while True:
    #     for push in push_back:
    #         # print(push)
    #         dog.move_legs(push)
    #         time.sleep(0.1)
    
    while True:
        #angles = imu.get_filtered_euler_angles()
        # if angles:
        #     roll, pitch, yaw = angles
        #     print(f"Filtered Euler angles: Roll={roll:.2f}°, Pitch={pitch:.2f}°, Yaw={yaw:.2f}°")
        #     new_pos = dog.pitch( -pitch/180*math.pi, dog.roll(-roll/180*math.pi,LEGS_INITIAL_POSITIONS))
        #     dog.move_legs(new_pos)
        
        sum = 0
        for leg in dog.legs:
            sum +=leg.get_present_current_sum()
        #print(sum)
        if sum > 13:
            print("Down")
        else:
            print("Up")
        time.sleep(0.1)
        

    # # for leg in dog.legs:
    #     leg.deactivate_leg(True)


if __name__ == "__main__":
    main()
