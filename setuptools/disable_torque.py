import sys
sys.path.append("..")
from STservo_sdk import *  

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

# Control table address
STS_TORQUE_ENABLE = 40  # Address to enable/disable torque

# Torque states
TORQUE_ENABLE = 1  # Enable torque
TORQUE_DISABLE = 0  # Disable torque



# User input for servo ID
servo_id = int(input("Enter Servo ID: "))

if int(servo_id) <= 6:
    packetHandler = packetHandlerf
else:
    packetHandler = packetHandlerb
        
# User input for enabling/disabling torque
torque_state = input("Enable torque? (y/n): ").strip().lower()

torque_value = TORQUE_ENABLE if torque_state == 'y' else TORQUE_DISABLE

# Send command to servo
sts_comm_result, sts_error = packetHandler.write1ByteTxRx(servo_id, STS_TORQUE_ENABLE, torque_value)

if sts_comm_result != COMM_SUCCESS:
    print("Failed to change torque state: %s" % packetHandler.getTxRxResult(sts_comm_result))
elif sts_error != 0:
    print("Servo error: %s" % packetHandler.getRxPacketError(sts_error))
else:
    state_text = "enabled" if torque_value == TORQUE_ENABLE else "disabled"
    print(f"Torque {state_text} for Servo ID {servo_id}")

# Close port
portHandlerb.closePort()
portHandlerf.closePort()
