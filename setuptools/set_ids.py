import math
from STservo_sdk import *  

# Default setting
BAUDRATE                    = 1000000           # STServo default baudrate : 1000000
DEVICENAME                  = '/dev/board_front'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

STS_MINIMUM_POSITION_VALUE  = 0                 # STServo will rotate between this value
STS_MAXIMUM_POSITION_VALUE  = 4095
STS_MOVING_SPEED            = 2400              # STServo moving speed
STS_MOVING_ACC              = 50                # STServo moving acc

index = 0
sts_goal_position = [STS_MINIMUM_POSITION_VALUE, STS_MAXIMUM_POSITION_VALUE]         # Goal position


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Get methods and members of Protocol
packetHandler = sts(portHandler)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()
    
NEW_SERVO_ID = input("NEW_SERVO_ID: ")
OLD_SERVO_ID = 1    

packetHandler.unLockEprom()
sts_comm_result, sts_error = packetHandler.write1ByteTxRx(portHandler, OLD_SERVO_ID, STS_ID, NEW_SERVO_ID)
packetHandler.LockEprom()

if sts_comm_result != COMM_SUCCESS:
    print("Failed to change ID: %s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("Servo error: %s" % packetHandler.getRxPacketError(sts_error))
else:
    print(f"Servo ID changed from {OLD_SERVO_ID} to {NEW_SERVO_ID}")
