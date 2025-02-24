#!/bin/python3
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
DEVICENAME = '/dev/board_front'  # Adjust this for your system
#DEVICENAME = '/dev/serial/by-id/usb-1a86_USB_Single_Serial_58FD016753-if00'  # Adjust this for your system

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
        print(f"Servo ID {servo_id} Position: {position}")
    else:
        print(f"Error reading position: {packetHandler.getTxRxResult(result)}")

# Close port
portHandler.closePort()
