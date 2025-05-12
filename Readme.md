# Robodog

This is the demo software for **Idefix**. It contains controller input, gait generation, inverse kinematics, controlling the servos for each leg, and reading data from an IMU sensor.  
This was the first attempt at implementing these concepts to get the quadruped robot to walk.

## What should you know?

### Prerequisites

Before running the software, ensure you have the following:

- **Hardware**:
  - A quadruped robot with servo motors and a BNO055 IMU sensor.
  - Xbox controller for manual control.
  - A computer with Python installed.

- **Software**:
  - Python 3.8 or later.
  - Required Python libraries (see `requirements.txt`).
  - STServo SDK for servo motor control.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Robodog.git
   cd Robodog
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On Linux/Mac
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the servo controllers:
   - Follow the instructions in `setuptools/Servo_Controller_Setup.md` to configure udev rules for persistent device names.

## Usage

### Running the Main Program

To start the robot control program, run:
```bash
python idefix/main.py
```

### Available Modes

- **Walking Loop**: The robot continuously walks in a predefined pattern.
- **Controller Mode**: Use the Xbox controller to manually control the robot's movements.
- **Auto-Balance**: The robot adjusts its posture based on IMU sensor data.
- **Push-Ups**: Demonstrates the robot's ability to perform vertical movements.

### Calibration

- **IMU Calibration**: Use `setuptools/calibrate_imu.py` to calibrate the BNO055 sensor.
- **Servo Offset Adjustment**: Use `setuptools/set_ofs.py` to adjust servo offsets for precise movements.

## File Structure

```
Robodog/
├── idefix/
│   ├── debug.py                # Debugging tools for visualizing leg positions
│   ├── gait.py                 # Gait generation logic
│   ├── imu.py                  # IMU sensor integration
│   ├── main.py                 # Main entry point for the robot control
│   ├── robot_constants.py      # Robot-specific constants
│   ├── robot_dog.py            # Core robot control logic
│   ├── robot_leg.py            # Leg-specific control logic
│   ├── servo_control.py        # Servo motor control
│   ├── utilities.py            # Helper functions
│   └── xbox_controller.py      # Xbox controller integration
├── setuptools/
│   ├── calibrate_imu.py        # IMU calibration script
│   ├── disable_torque.py       # Disable servo torque
│   ├── move_servo.py           # Manually move servos
│   ├── read_pos.py             # Read servo positions
│   ├── set_ids.py              # Set servo IDs
│   ├── set_ofs.py              # Set servo offsets
│   └── Servo_Controller_Setup.md # Guide for setting up servo controllers
├── STservo_sdk/                # STServo SDK for servo control
├── .gitignore                  # Git ignore file
└── Readme.md                   # Project documentation
```

## Troubleshooting

- **Servo Not Responding**: Ensure the servo controllers are properly configured and connected. Check the udev rules if using Linux.
- **IMU Data Incorrect**: Recalibrate the IMU sensor using `calibrate_imu.py`.
- **Controller Not Detected**: Verify the Xbox controller is connected and recognized by the system.

## Future Improvements

Coming soon: A **ROS 2** version of the Robodog software with many improvements, including:

- Enhanced modularity and scalability.
- Real-time communication and control using ROS 2 nodes.
- Advanced gait generation and motion planning.
- Improved sensor integration and data processing.
- Support for additional hardware and sensors.

Stay tuned for updates!