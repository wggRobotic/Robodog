import sys
import os
import time

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import tty, termios
    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

sys.path.append("..")
from STservo_sdk import *  # Uses STServo SDK library


# Default settings
BAUDRATE = 1000000  # Default baud rate for STServo
DEVICENAME = '/dev/board_front'  # Adjust the serial port according to your system

STS_MINIMUM_POSITION_VALUE = 0
STS_MAXIMUM_POSITION_VALUE = 4095
STS_MOVING_SPEED = 2400
STS_MOVING_ACC = 50

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = sts(portHandler)

# Open port
if not portHandler.openPort():
    print("Failed to open the port")
    quit()
print("Succeeded in opening the port")

# Set port baud rate
if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the baud rate")
    quit()
print("Succeeded in changing the baud rate")

# Select servo ID
SERVO_ID = int(input("Enter SERVO ID: "))  

# Read and display current offset
offset_low, _, _ = packetHandler.read1ByteTxRx(SERVO_ID, STS_OFS_L)
offset_high, _, _ = packetHandler.read1ByteTxRx(SERVO_ID, STS_OFS_H)
CURRENT_OFFSET = (offset_high << 8) | offset_low
print(f"Current offset: {CURRENT_OFFSET}")

# Set new offset
NEW_OFFSET = int(input("Enter NEW OFFSET VALUE: "))
offset_low = NEW_OFFSET & 0xFF
offset_high = (NEW_OFFSET >> 8) & 0xFF

# Unlock EEPROM, write new offset, then lock EEPROM
packetHandler.unLockEprom(SERVO_ID)
sts_comm_result, sts_error = packetHandler.write1ByteTxRx(SERVO_ID, STS_OFS_L, offset_low)
sts_comm_result2, sts_error2 = packetHandler.write1ByteTxRx(SERVO_ID, STS_OFS_H, offset_high)
packetHandler.LockEprom(SERVO_ID)

# Check if the offset was set successfully
if sts_comm_result != COMM_SUCCESS or sts_comm_result2 != COMM_SUCCESS:
    print(f"Failed to set offset: {packetHandler.getTxRxResult(sts_comm_result)}")
else:
    print(f"Offset successfully set to {NEW_OFFSET}")

# Allow user to test a new position
TEST_POSITION = int(input("Enter a test position (0-4095): "))

# Send position command
sts_comm_result, sts_error = packetHandler.write2ByteTxRx(SERVO_ID, STS_GOAL_POSITION_L, TEST_POSITION)

if sts_comm_result != COMM_SUCCESS:
    print(f"Failed to move servo: {packetHandler.getTxRxResult(sts_comm_result)}")
else:
    print(f"Servo moved to position {TEST_POSITION}")
