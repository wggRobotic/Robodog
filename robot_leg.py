import math
from typing import List

import servo_control

class RobotLeg:
    def __init__(self, id: int, upper_leg_length: float, lower_leg_length: float, hip_to_shoulder: float,
                 servo_channels: List[int],
                 initial_position: List[float]):
        self.id = id
        self.upper_leg_length = upper_leg_length
        self.lower_leg_length = lower_leg_length
        self.hip_to_shoulder = hip_to_shoulder
        self.current_position = initial_position
        self.servo_channels = servo_channels

    #angle calculations and actual moving functions are separated so cases where some legs are out of bounds can be handled
    #self.current_position has to be set manually

    #returnes leg angles for given foot position
    def inverseKinematics(self, x: float, y: float, z: float) -> List[float]:
        #kinematics are oriented relative to hip joint
        #pos x = backwards relative to  robot
        #pos y = outwards relative to robot
        #pos z = down

        #distance hip - foot on y,z plane
        d_hip_foot = math.sqrt(y**2 + z**2)

        #distance shoulder - foot on y,z plane
        if d_hip_foot**2 - self.hip_to_shoulder**2 < 0:
            print(f"Target point too close to joint at leg {self.id}")
            return None, None, None
        d_shoulder_foot = math.sqrt(d_hip_foot**2 - self.hip_to_shoulder**2)

        #hip joint
        hip_angle = math.atan2(y, z) + math.atan2(d_shoulder_foot, self.hip_to_shoulder) - math.pi / 2

        #distance shoulder - foot on plane formed by span of upper and lower leg after hip rotation
        virtual_leg_length = math.sqrt(d_shoulder_foot**2 + x**2)

        if virtual_leg_length == 0:
            print("virtual_leg_length 0")
            return None, None, None

        cos_alpha = (virtual_leg_length**2 - self.upper_leg_length**2 - self.lower_leg_length**2) / (2 * self.upper_leg_length * self.lower_leg_length)
        cos_beta = (virtual_leg_length**2 + self.upper_leg_length**2 - self.lower_leg_length**2) / (2 * virtual_leg_length * self.upper_leg_length)

        if (not (-1 <= cos_alpha <= 1)) or (not (-1 <= cos_beta <= 1)):
            print(f"Target out of physical range at leg {self.id} cos alpha {cos_alpha} cos beta {cos_beta}")
            return None, None, None
        
        #ellbow joint
        ellbow_angle = math.acos(cos_alpha)
        #shoulder joint
        shoulder_angle = math.acos(cos_beta) + math.atan2(x, d_shoulder_foot)

        #TODO angle bound check

        return ellbow_angle, shoulder_angle, hip_angle

    #moves the joints to specified angles
    def move(self, ellbow_angle: float, shoulder_angle: float, hip_angle: float):
        #TODO angle bound check
        servo_control.servo_move(self.servo_channels[0], ellbow_angle)
        servo_control.servo_move(self.servo_channels[1], shoulder_angle)
        servo_control.servo_move(self.servo_channels[2], hip_angle)
