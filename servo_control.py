import math
from STservo_sdk import *  # Uses STServo SDK library
import robot_constants as rc

class ServoControl:
    def __init__(self):
        # Initialize PortHandler instances
        self.port_handler1 = PortHandler(rc.DEVICENAME1)
        self.port_handler2 = PortHandler(rc.DEVICENAME2)

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
        if self.port_handler1.setBaudRate(rc.BAUDRATE1):
            print("Succeeded to set baudrate 1")
        else:
            print("Failed to set baudrate 1")

        if self.port_handler2.setBaudRate(rc.BAUDRATE2):
            print("Succeeded to set baudrate 2")
        else:
            print("Failed to set baudrate 2")

    def servo_in(self, channel: int, angle: float):
        if channel <= 6:
            self.servo_move(self.packetHandler1, self.port_handler1, channel, angle)
        else:
            self.servo_move(self.packetHandler2, self.port_handler2, channel, angle)

    @staticmethod
    def map_value(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def servo_move(self, packetHandler, port_handler, channel, angle):
        # Map angle to servo position
        servo_position = self.map_value(angle, 0, math.pi*2, rc.STS_MINIMUM_POSITION_VALUE, rc.STS_MAXIMUM_POSITION_VALUE)

        # Set goal position
        sts_comm_result, sts_error = packetHandler.write2ByteTxRx(port_handler, channel, STS_GOAL_POSITION_L, int(servo_position))
        if sts_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(sts_comm_result))
        elif sts_error != 0:
            print("%s" % packetHandler.getRxPacketError(sts_error))

        # Syncwrite goal position
        sts_comm_result = packetHandler.groupSyncWrite.txPacket()
        if sts_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(sts_comm_result))

        # Clear syncwrite parameter storage
        packetHandler.groupSyncWrite.clearParam()
