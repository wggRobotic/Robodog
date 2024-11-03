class ServoControl:
    def __init__(self, id:int, min_angle: int, max_angle: int):
        self.id = id
        self.min_angle = min_angle
        self.max_angle = max_angle
        
    def set_angle(self, angle: float)->float:
        if angle < self.min_angle:
            angle = self.min_angle
        elif angle > self.max_angle:
            angle = self.max_angle
        print(f"Servo {self.id} set to {angle} degrees.")
        return angle    
    
    def move(self, angle: float):
        angle = self.set_angle(angle)
        # Move the servo to the specified angle
        # use self.id to identify the servo
        