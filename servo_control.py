import math
from STservo_sdk import *  # Uses STServo SDK library
import robot_constants as rc


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
port_handler1 = PortHandler(rc.DEVICENAME1)
port_handler2 = PortHandler(rc.DEVICENAME2)

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler1 = sts(port_handler1)
packetHandler2 = sts(port_handler2)

# Open port
if port_handler1.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")


if port_handler2.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")


# Set port baudrate
if port_handler1.setBaudRate(rc.BAUDRATE1):
    print("Succeeded to set baudrate")
else:
    print("Failed to set baudrate")

if port_handler2.setBaudRate(rc.BAUDRATE2):
    print("Succeeded to set baudrate")
else:
    print("Failed to set baudrate")


def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def servo_move(channel: int, angle: float):
    STS_MOVING_SPEED = 2400  # Standard-Geschwindigkeit
    STS_MOVING_ACC = 50  # Standard-Beschleunigung

    # Map angle to servo position
    servo_position = map_value(angle, -math.pi/2, math.pi/2, rc.STS_MINIMUM_POSITION_VALUE, rc.STS_MAXIMUM_POSITION_VALUE)

    # Set goal position
    sts_comm_result, sts_error = packetHandler1.write2ByteTxRx(port_handler1, channel, STS_GOAL_POSITION_L, int(servo_position))
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler1.getTxRxResult(sts_comm_result))
    elif sts_error != 0:
        print("%s" % packetHandler1.getRxPacketError(sts_error))

    # Syncwrite goal position
    sts_comm_result = packetHandler1.groupSyncWrite.txPacket()
    if sts_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler1.getTxRxResult(sts_comm_result))

    # Clear syncwrite parameter storage
    packetHandler1.groupSyncWrite.clearParam()

def servo_move(channel: int, angle: float):
    STS_MOVING_SPEED = 2400  # Standard-Geschwindigkeit
    STS_MOVING_ACC = 50  # Standard-Beschleunigung

    # Map angle to servo position
    servo_position = map_value(angle, -math.pi/2, math.pi/2, rc.STS_MINIMUM_POSITION_VALUE, rc.STS_MAXIMUM_POSITION_VALUE)

    # Set goal position
    sts_comm_result, sts_error = packetHandler2.write2ByteTxRx(port_handler2, channel, STS_GOAL_POSITION_L, int(servo_position))
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
