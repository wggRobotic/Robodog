import math
from typing import List

from idefix.servo_control import*


class RobotLeg:
    def __init__(self, id: int, upper_leg_length: float, lower_leg_length: float, hip_to_shoulder: float,
                 servo_ids: List[int],
                 initial_position: List[float],sc: ServoControl):
        self.id = id
        self.upper_leg_length = upper_leg_length
        self.lower_leg_length = lower_leg_length
        self.hip_to_shoulder = hip_to_shoulder
        self.current_position = initial_position
        self.servo_ids = servo_ids
        self.sc = sc

    #angle calculations and actual moving functions are separated so cases where some legs are out of bounds can be handled
    #self.current_position has to be set manually
    
    def inverseKin1(self, z: float) -> List[float]:
        
        v1 = (self.upper_leg_length**2 + self.lower_leg_length**2 - z**2) / (2 * self.upper_leg_length * self.lower_leg_length)
    
        alpha = math.acos(v1)
        v2 = (self.upper_leg_length**2 - self.lower_leg_length**2 +z**2)/(2*self.upper_leg_length*z)
        beta = math.acos(v2)
        
        return [alpha,beta]
    
    def inverseKin2(self, x:float , z:float):
        shoulder_to_foot = math.sqrt(x**2 +z**2)
        delta_beta = math.atan2(x,z)
        print(delta_beta/math.pi * 180)
        alpha, beta = self.inverseKin1(shoulder_to_foot)
        beta = beta - delta_beta
        return alpha,beta
    
    def inverseKin3(self, x:float , y:float, z:float) -> List[float]:
        shoulder_to_foot = math.sqrt(z**2+y**2 - self.hip_to_shoulder**2)
        
        gamma1 = math.atan2(y,z)
        gamm2 = math.atan2(shoulder_to_foot,self.hip_to_shoulder)
        alpha, beta = self.inverseKin2(x,shoulder_to_foot)
        gamma = gamma1 + gamm2
        
        return alpha, beta, gamma
    

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
        self.sc.set_pos(self.servo_ids[0], ellbow_angle)
        self.sc.set_pos(self.servo_ids[1], shoulder_angle)
        self.sc.set_pos(self.servo_ids[2], hip_angle)
        self.sc.move_positions()
