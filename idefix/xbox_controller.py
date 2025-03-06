from evdev import InputDevice, ecodes
import threading


class XboxController:
    def __init__(self, device_path="/dev/input/event4"):
        try:
            self.gamepad = InputDevice(device_path)
            print(f"Controller connected: {self.gamepad}")
        except FileNotFoundError:
            print("Controller not found. Make sure it is connected.")
            exit(1)

        # State of the controller
        self.state = {
            "axes": {
                "ABS_X": 32768,  # Left Joystick X-axis
                "ABS_Y": 32768,  # Left Joystick Y-axis
                "ABS_RX": 32768,  # Right Joystick X-axis
                "ABS_RY": 32768,  # Right Joystick Y-axis
                "ABS_Z": 32768,  # Left Trigger
                "ABS_RZ": 32768,  # Right Trigger
                "ABS_HAT0X": 0,  # D-Pad Left/Right
                "ABS_HAT0Y": 0,  # D-Pad Up/Down
            },
            "buttons": {
                "BTN_SOUTH": 0,  # A Button
                "BTN_EAST": 0,  # B Button
                "BTN_NORTH": 0,  # Y Button
                "BTN_WEST": 0,  # X Button
                "BTN_TL": 0,  # Left Bumper
                "BTN_TR": 0,  # Right Bumper
                "BTN_SELECT": 0,  # Back Button
                "BTN_START": 0,  # Start Button
                "BTN_THUMBL": 0,  # Left Joystick Press
                "BTN_THUMBR": 0,  # Right Joystick Press
            },
        }

        # Start a thread to monitor controller events
        self._monitor_thread = threading.Thread(
            target=self._monitor_controller, daemon=True
        )
        self._monitor_thread.start()

    def _monitor_controller(self):
        """Monitors the controller and updates the state."""
        for event in self.gamepad.read_loop():
            if event.type == ecodes.EV_ABS:  # Axis events
                if event.code == ecodes.ABS_X:
                    self.state["axes"]["ABS_X"] = event.value
                elif event.code == ecodes.ABS_Y:
                    self.state["axes"]["ABS_Y"] = event.value
                elif event.code == ecodes.ABS_RX:
                    self.state["axes"]["ABS_RZ"] = event.value
                elif event.code == ecodes.ABS_RY:
                    self.state["axes"]["ABS_Z"] = event.value
                elif event.code == ecodes.ABS_Z:
                    self.state["axes"]["ABS_Z"] = event.value
                elif event.code == ecodes.ABS_RZ:
                    self.state["axes"]["ABS_RZ"] = event.value
                elif event.code == ecodes.ABS_HAT0X:  # D-Pad Left/Right
                    self.state["axes"]["ABS_HAT0X"] = event.value
                elif event.code == ecodes.ABS_HAT0Y:  # D-Pad Up/Down
                    self.state["axes"]["ABS_HAT0Y"] = event.value
            elif event.type == ecodes.EV_KEY:  # Button events
                if event.code == ecodes.BTN_SOUTH:
                    self.state["buttons"]["BTN_SOUTH"] = event.value
                elif event.code == ecodes.BTN_EAST:
                    self.state["buttons"]["BTN_EAST"] = event.value
                elif event.code == ecodes.BTN_NORTH:
                    self.state["buttons"]["BTN_NORTH"] = event.value
                elif event.code == ecodes.BTN_WEST:
                    self.state["buttons"]["BTN_WEST"] = event.value
                elif event.code == ecodes.BTN_TL:
                    self.state["buttons"]["BTN_TL"] = event.value
                elif event.code == ecodes.BTN_TR:
                    self.state["buttons"]["BTN_TR"] = event.value
                elif event.code == ecodes.BTN_SELECT:
                    self.state["buttons"]["BTN_SELECT"] = event.value
                elif event.code == ecodes.BTN_START:
                    self.state["buttons"]["BTN_START"] = event.value
                elif event.code == ecodes.BTN_THUMBL:
                    self.state["buttons"]["BTN_THUMBL"] = event.value
                elif event.code == ecodes.BTN_THUMBR:
                    self.state["buttons"]["BTN_THUMBR"] = event.value

    def get_axis(self, axis_name):
        """Returns the value of an axis."""
        return self.state["axes"].get(axis_name, None)

    def get_button(self, button_name):
        """Returns the state of a button."""
        return self.state["buttons"].get(button_name, None)


if __name__ == "__main__":
    controller = XboxController()

    while True:
        # Example: Query axis and button values
        left_stick_x = controller.get_axis("ABS_Z")
        a_button = controller.get_button("BTN_SOUTH")
        dpad_x = controller.get_axis("ABS_HAT0X")  # D-Pad Left/Right
        dpad_y = controller.get_axis("ABS_HAT0Y")  # D-Pad Up/Down

        print(
            f"Left Joystick X: {left_stick_x}, A Button: {a_button}, D-Pad X: {dpad_x}, D-Pad Y: {dpad_y}"
        )
