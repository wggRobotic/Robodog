import time
import board
import sys
import adafruit_bno055
import math
from collections import deque
sys.path.append("..")
from idefix.robot_constants import *

class IMU:
    def __init__(self, i2c, window_size=5, threshold=5.0):
        """Initializes the BNO055 sensor and the filter buffers."""
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        
        # Set the sensor offsets that you obtained from calibration
        self.sensor.offsets_gyroscope = OFFSETS_GYROSCOPE
        self.sensor.offsets_accelerometer = OFFSETS_ACCELEROMETER
        self.sensor.offsets_magnetometer = OFFSETS_MAGNETOMETER
        
        # Window size for moving average
        self.window_size = window_size
        
        # Threshold for outlier detection (in degrees)
        self.threshold = threshold
        
        # Buffers for the moving average of the three Euler angles
        self.roll_buffer = deque(maxlen=window_size)
        self.pitch_buffer = deque(maxlen=window_size)
        self.yaw_buffer = deque(maxlen=window_size)

        # Initialize with zero values
        self.prev_roll = 0.0
        self.prev_pitch = 0.0
        self.prev_yaw = 0.0

    def moving_average(self, buffer, new_value):
        """Adds a new value and calculates the moving average."""
        buffer.append(new_value)
        return sum(buffer) / len(buffer)

    def exponential_moving_average(self, prev_value, new_value, alpha=0.1):
        """Calculates the exponential moving average."""
        return alpha * new_value + (1 - alpha) * prev_value

    def quaternion_to_euler(self, w, x, y, z):
        """Converts quaternions to Euler angles (Roll, Pitch, Yaw)."""
        # Calculate Roll, Pitch, and Yaw from quaternions
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp) * (180 / math.pi)

        sinp = 2 * (w * y - z * x)
        pitch = math.copysign(90, sinp) if abs(sinp) >= 1 else math.asin(sinp) * (180 / math.pi)

        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp) * (180 / math.pi)

        return roll, pitch, yaw

    def filter_euler_angles(self, roll, pitch, yaw):
        """Filter the Euler angles with exponential moving average and outlier detection."""
        # Outlier detection: check if the new value deviates too much from the previous value
        if abs(roll - self.prev_roll) > self.threshold:
            roll = self.prev_roll  # Discard the new value if it’s too far from the previous value

        if abs(pitch - self.prev_pitch) > self.threshold:
            pitch = self.prev_pitch  # Discard the new value if it’s too far from the previous value

        if abs(yaw - self.prev_yaw) > self.threshold:
            yaw = self.prev_yaw  # Discard the new value if it’s too far from the previous value

        # Apply exponential moving average to smooth the angles
        roll = self.exponential_moving_average(self.prev_roll, roll)
        pitch = self.exponential_moving_average(self.prev_pitch, pitch)
        yaw = self.exponential_moving_average(self.prev_yaw, yaw)

        # Update previous values for next iteration
        self.prev_roll = roll
        self.prev_pitch = pitch
        self.prev_yaw = yaw

        return roll, pitch, yaw

    def get_filtered_euler_angles(self):
        """Reads quaternions, converts them, filters the Euler angles."""
        quat = self.sensor.quaternion
        if quat is not None:
            w, x, y, z = quat
            roll, pitch, yaw = self.quaternion_to_euler(w, x, y, z)

            # Apply filtering to the Euler angles
            roll, pitch, yaw = self.filter_euler_angles(roll, pitch, yaw)

            return pitch, roll, yaw
        return None

if __name__ == "__main__":
    i2c = board.I2C()
    imu = IMU(i2c, window_size=5, threshold=5.0)

    while True:
        angles = imu.get_filtered_euler_angles()
        if angles:
            pitch, roll, yaw = angles
            print(f"Filtered Euler angles: Roll={roll:.2f}°, Pitch={pitch:.2f}°, Yaw={yaw:.2f}°")
        time.sleep(0.1)
