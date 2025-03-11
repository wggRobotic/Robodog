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
from idefix.utilities import map_value
from idefix.imu import IMU

def print_present_currents(dog):
    sums = []
    for leg in dog.legs:
        sums.append(leg.get_present_current_sum())
    
    for i, sum in enumerate(sums):
        if sum >= 3:
            print(f"id: {i} Down {sum}")
        else:
            print(f"id: {i} Up {sum}")
            
    time.sleep(0.4)
    
def walking_loop(dog):
    g = Gait(dog)
    push_back = g.walk(50.0, 0.0, 0.0, 2.0, 20.0,8)
    while True:
        for push in push_back:
            # print(push)
            dog.move_legs(push)
            time.sleep(0.1)
            
def compare_imu_with_rotation(dog):
    i2c = board.I2C()
    imu = IMU(i2c,pitch_offset= -4.0,roll_offset= 0.0, window_size=3, threshold=50.0)

    while True:
        
        try:
            pitch_target = float(input("Enter target pitch angle (in degrees): "))
            roll_target = float(input("Enter target roll angle (in degrees): "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return

        pitch_target_rad = pitch_target * math.pi / 180
        roll_target_rad = roll_target * math.pi / 180
        dog.move_legs(dog.pitch(pitch_target_rad, dog.roll(roll_target_rad, LEGS_INITIAL_POSITIONS)))
    
        momevement_total = True
        while momevement_total:
            momevement_total = False
            for i, leg in enumerate(dog.legs):
                #print(f"id:{i} {leg.read_movement()}")
                if(leg.read_movement()):
                    momevement_total = True
        
        angles = imu.get_raw_euler_angles()
        if angles:
            roll, pitch, yaw = angles
            roll_value = int(roll) / 180 * math.pi
            pitch_value = int(pitch) / 180 * math.pi
            print(f"Current Euler angles:       Roll= {roll:.2f}°, Pitch= {(pitch):.2f}°")
            print(f"Target angles:              Roll= {roll_target:.2f}°, Pitch= {pitch_target:.2f}°")
            print(f"Current angles in radians:  Roll= {roll_value:.2f}, Pitch= {pitch_value:.2f}")
            print(f"Target angles in radians:   Roll= {roll_target_rad:.2f}, Pitch= {pitch_target_rad:.2f}")
            print("---")

        time.sleep(0.5)  # Small sleep to prevent high CPU usage
        
def print_angles():
    i2c = board.I2C()
    imu = IMU(i2c,pitch_offset= 0.0,roll_offset= 0.0, window_size=1, threshold=50.0)
    while True:
        angles = imu.get_raw_euler_angles()
        if angles:
            roll, pitch, yaw = angles
            print(f"Filtered Euler angles: Roll={roll:.2f}°, Pitch={pitch:.2f}°, Yaw={yaw:.2f}")
        time.sleep(0.1)

            
def auto_balance(dog):
    i2c = board.I2C()
    imu = IMU(i2c,pitch_offset= -0.0,roll_offset= 0.0, window_size=3, threshold=50.0)

    roll_value = 0
    pitch_value = 0
    
    roll_sensor_value = 0
    pitch_sensor_value = 0
    new_pos = LEGS_INITIAL_POSITIONS

    while True:
       
        angles = imu.get_filtered_euler_angles()
        if angles:
            roll, pitch, yaw = angles
            roll_sensor_value = int(roll) / 180 * math.pi # if abs(roll) > 1 else 0
            pitch_sensor_value = int(pitch + 4.5) / 180 * math.pi # if abs(pitch + 4.5) > 2 else 0
            print(f"Filtered Euler angles: Roll={roll:.2f}°, Pitch={(pitch + 4.5):.2f}°, roll_value={roll_sensor_value:.2f}, pitch_value={pitch_sensor_value:.2f}")

        if abs(pitch) > 2 or abs(roll) > 1:
            roll_value -= roll_sensor_value
            pitch_value -= pitch_sensor_value
            
            new_pos = dog.pitch(pitch_value, dog.roll(roll_value, LEGS_INITIAL_POSITIONS))
            dog.move_legs(new_pos)
            
            movement_total = True
            while movement_total:
                movement_total = False
                for i, leg in enumerate(dog.legs):
                    #print(f"id:{i} {leg.read_movement()}")
                    if(leg.read_movement()):
                        movement_total = True
                time.sleep(0.1)
                
                
def control_rotation(dog):
    
    a_lock = False
    b_lock = False
    active = True
    
    controller = XboxController()
    deadzone = 0.2
    
    while True:
        # Read controller input for the left joystick Y-axis
        ly_raw = controller.get_axis('ABS_Y')
        a = controller.get_button('BTN_SOUTH')
        b = controller.get_button('BTN_EAST')
        lx_raw = controller.get_axis('ABS_X')
        z_raw = controller.get_axis('ABS_Z')

        ly = map_value(ly_raw, 0, 65535, -1, 1)
        lx = map_value(lx_raw, 0, 65535, -1, 1)
        rz = map_value(z_raw, 0, 65535, -1, 1)

        # Apply a deadzone to ignore small movements
        if abs(ly) < deadzone:
            ly = 0.0
        if abs(lx) < deadzone:
            lx = 0.0
        if abs(rz) < deadzone:
            rz = 0.0

        yaw_positions = dog.yaw(rz*20/180*math.pi,LEGS_INITIAL_POSITIONS)
        roll_position = dog.roll(lx*60/180*math.pi, yaw_positions)
        pitch_positions = dog.pitch(ly*40/180*math.pi, roll_position)
        if (active):
            dog.move_legs(pitch_positions)

        # Emergency stop ;)
        if(a==1 and not a_lock):
            a_lock = True
            active = True
            for leg in dog.legs:
                leg.deactivate_leg(True)
            a_lock = False

        if(b==1 and not b_lock):
            b_lock = True
            active = False
            for leg in dog.legs:
                leg.deactivate_leg(False)
            b_lock = False

        time.sleep(0.1)
    
        
def main():
    sc = ServoControl()
    
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
    
    # control_rotation(dog)
    # compare_imu_with_rotation(dog)
    walking_loop(dog)
    # print_present_currents(dog)
    # print_angles()
    # auto_balance(dog)
    
    # time.sleep(1.0)
    # dog.move_legs(dog.translation(0.0 ,20.0 ,0.0 ,LEGS_INITIAL_POSITIONS))
    
    

    

    
    
    
        
        
     


if __name__ == "__main__":
    main()
