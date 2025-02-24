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
STS_MOVING_SPEED = 2400  # Servo speed
STS_MOVING_ACC = 50  # Servo acceleration

DEVICENAMEF = '/dev/board_front'
DEVICENAMEB = '/dev/board_back'

# Initialize PortHandler instance
portHandlerb = PortHandler(DEVICENAMEB)
portHandlerf = PortHandler(DEVICENAMEF)
# Initialize PacketHandler instance
packetHandlerf = sts(portHandlerf)
packetHandlerb = sts(portHandlerb)
# Open port
if not portHandlerf.openPort():
    print("Failed to open the port")
    sys.exit()

if not portHandlerb.openPort():
    print("Failed to open the port")
    sys.exit()
    
# Set baudrate
if not portHandlerb.setBaudRate(BAUDRATE):
    print("Failed to set baudrate")
    sys.exit()
    
# Set baudrate
if not portHandlerf.setBaudRate(BAUDRATE):
    print("Failed to set baudrate")
    sys.exit()

while True:
    servo_id = input("Enter Servo ID (or 'q' to quit): ")
    if int(servo_id) <= 6:
        packetHandler = packetHandlerf
    else:
        packetHandler = packetHandlerb
        
        
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
        print(f"Position at the moment:{position}")
        new_position = int(input("New Position:"))
        print(position)
        packetHandler.WritePosEx(servo_id, new_position, -2400, STS_ACC)
        time.sleep(2.5)  # Wait for movement

    else:
        print(f"Error reading position: {packetHandler.getTxRxResult(result)}")

# Close port
portHandlerf.closePort()
portHandlerb.closePort()
