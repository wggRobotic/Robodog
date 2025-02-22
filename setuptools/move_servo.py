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
BAUDRATE = 1000000
DEVICENAME = '/dev/board_back'  # Adjust for your system
STS_MOVING_SPEED = 2400  # Servo speed
STS_MOVING_ACC = 50  # Servo acceleration

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = sts(portHandler)

# Open port
if not portHandler.openPort():
    print("Failed to open the port")
    sys.exit()

# Set baudrate
if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to set baudrate")
    sys.exit()

while True:
    servo_id = input("Enter Servo ID (or 'q' to quit): ")
    if servo_id.lower() == 'q':
        break

    try:
        servo_id = int(servo_id)
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue

    # Read present position
    position, result, error = packetHandler.ReadPos(servo_id)
    if result == COMM_SUCCESS:
        print(f"Servo ID {servo_id} Current Position: {position}")

        # Move 10 units forward
        new_position = position + 10
        packetHandler.WritePosEx(servo_id, new_position, STS_MOVING_SPEED, STS_MOVING_ACC)
        time.sleep(1)  # Wait for movement

        # Move back to original position
        packetHandler.WritePosEx(servo_id, position, STS_MOVING_SPEED, STS_MOVING_ACC)
        time.sleep(1)  # Wait for movement

    else:
        print(f"Error reading position: {packetHandler.getTxRxResult(result)}")

# Close port
portHandler.closePort()
