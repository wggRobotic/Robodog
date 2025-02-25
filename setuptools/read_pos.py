import sys
import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

sys.path.append("..")
from STservo_sdk import *  # Uses STServo SDK library

# Default setting
BAUDRATE = 1000000
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
    if servo_id.lower() == 'q':
        break

    try:
        servo_id = int(servo_id)
    except ValueError:
        print("Invalid input. Please enter a number.")
        continue
    
    if int(servo_id) <= 6:
        packetHandler = packetHandlerf
    else:
        packetHandler = packetHandlerb
    # Read present position
    position, result, error = packetHandler.ReadPos(servo_id)

    if result == COMM_SUCCESS:
        print(f"Servo ID {servo_id} Position: {position}")
    else:
        print(f"Error reading position: {packetHandler.getTxRxResult(result)}")

# Close port
portHandler.closePort()
