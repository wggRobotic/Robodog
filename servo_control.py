import math
from STservo_sdk import *  # Uses STServo SDK library
from robot_constants import *

class ServoControl:
    def __init__(self):
        # Initialize PortHandler instances
        self.port_handler1 = PortHandler(DEVICENAME1)
        self.port_handler2 = PortHandler(DEVICENAME2)

        # Initialize PacketHandler instances
        self.packetHandler1 = sts(self.port_handler1)
        self.packetHandler2 = sts(self.port_handler2)

        # Open ports
        if self.port_handler1.openPort():
            print("Succeeded to open port 1")
        else:
            print("Failed to open port 1")

        if self.port_handler2.openPort():
            print("Succeeded to open port 2")
        else:
            print("Failed to open port 2")

        # Set baud rates
        if self.port_handler1.setBaudRate(BAUDRATE1):
            print("Succeeded to set baudrate 1")
        else:
            print("Failed to set baudrate 1")

        if self.port_handler2.setBaudRate(BAUDRATE2):
            print("Succeeded to set baudrate 2")
        else:
            print("Failed to set baudrate 2")

    def servo_in(self, id: int, angle: float):
        if id <= 6:
            self.servo_move(self.packetHandler1, id, angle)
        else:
            self.servo_move(self.packetHandler2, id, angle)

    @staticmethod
    def map_value(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def servo_move(self, packetHandler: sts, id, angle):
        # Map angle to servo position
        servo_position = int(self.map_value(angle, 0, math.pi*2, STS_MINIMUM_POSITION_VALUE, STS_MAXIMUM_POSITION_VALUE))

        # Set goal position
        sts_comm_result = packetHandler.SyncWritePosEx(id,servo_position + legs_offset[id],STS_MOVING_SPEED,STS_MOVING_ACC)  
        if sts_comm_result != True:
            print("[ID:%03d] groupSyncWrite addparam failed" % servo_position)

        # Clear syncwrite parameter storage
        packetHandler.groupSyncWrite.clearParam()
