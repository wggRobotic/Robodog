import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
import numpy as np

class Sim:
    def __init__(self, width, length, upper_leg_length, lower_leg_length, hip_to_shoulder):
        self.upper_leg_length = upper_leg_length
        self.lower_leg_length = lower_leg_length
        self.hip_to_shoulder = hip_to_shoulder

        self.x = [0, length, length, 0]  # x-coordinates (front to back)
        self.y = [0, 0, width, width]  # y-coordinates (side to side)
        self.z = [0, 0, 0, 0]  # z-coordinates (height)

        # Initial angle for the lines
        self.angle_blue_to_plane = 0  # Angle of the blue line to the plane (0 for horizontal)
        self.angle_red_to_plane = 90  # Angle of the red line to the plane (90 degrees to the blue line)
        self.angle_green_to_red = 0  # Angle of the green line relative to the red line

        # Initialize plot
        self.fig = plt.figure(figsize=(10, 10))  # Adjusted figure size
        self.ax = self.fig.add_subplot(111, projection="3d")

        # Create surface and lines
        self.plot_surface()
        self.plot_lines()

        # Add axis labels
        self.ax.set_xlabel('Depth (X-Axis)')
        self.ax.set_ylabel('Width (Y-Axis)')
        self.ax.set_zlabel('Height (Z-Axis)')

    def plot_surface(self):
        verts = [list(zip(self.x, self.y, self.z))]
        self.ax.add_collection3d(art3d.Poly3DCollection(verts, color="lightblue", alpha=0.6))

    def plot_lines(self):
        # Clear previous lines
        self.ax.cla()
        self.plot_surface()

        # 4 legs (one at each corner of the surface)
        self.leg_endpoints = []  # List to store all leg endpoints

        for i in range(4):
            x_start, y_start, z_start = self.x[i], self.y[i], self.z[i]

            # Calculate the angle of the blue line to the surface
            if i in [0, 1]:  # front (left and right)
                y_end_blue = y_start - self.hip_to_shoulder * np.cos(np.radians(self.angle_blue_to_plane))
            else:  # back (left and right)
                y_end_blue = y_start + self.hip_to_shoulder * np.cos(np.radians(self.angle_blue_to_plane))
            z_end_blue = z_start + self.hip_to_shoulder * np.sin(np.radians(self.angle_blue_to_plane))

            # Draw the blue line
            self.ax.plot([x_start, x_start], [y_start, y_end_blue], [z_start, z_end_blue], color="blue")

            # Red line: starts at the end position of the blue line
            # Always at a 90 degree angle to the blue line
            x_end_red = x_start + self.upper_leg_length * np.cos(np.radians(self.angle_red_to_plane))
            y_end_red = y_end_blue
            z_end_red = z_end_blue - self.upper_leg_length * np.sin(np.radians(self.angle_red_to_plane))

            # Draw the red line
            self.ax.plot([x_start, x_end_red], [y_end_blue, y_end_red], [z_end_blue, z_end_red], color="red")

            # Store the end points of the red line
            self.leg_endpoints.append((x_end_red, y_end_red, z_end_red))

            # Calculate the green line relative to the red line
            direction_vector = np.array([x_end_red - x_start, y_end_red - y_end_blue, z_end_red - z_end_blue])
            direction_vector /= np.linalg.norm(direction_vector)  # Normalize to unit length
            rotation_matrix = self.rotation_matrix_y(self.angle_green_to_red)
            rotated_vector = np.dot(rotation_matrix, direction_vector) * self.lower_leg_length
            x_end_green = x_end_red + rotated_vector[0]
            y_end_green = y_end_red + rotated_vector[1]
            z_end_green = z_end_red + rotated_vector[2]

            # Draw the green line
            self.ax.plot([x_end_red, x_end_green], [y_end_red, y_end_green], [z_end_red, z_end_green], color="green")

            # Store the end points of the green line
            self.leg_endpoints.append((x_end_green, y_end_green, z_end_green))

    def rotation_matrix_y(self, angle):
        """Rotation around the Y-axis for the given angle in degrees."""
        angle_rad = np.radians(angle)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        return np.array([
            [cos_a, 0, sin_a],
            [0, 1, 0],
            [-sin_a, 0, cos_a]
        ])

    def update_blue_line_angle(self, angle):
        """Change the angle of the blue line to the surface and update the plot."""
        self.angle_blue_to_plane = angle
        self.angle_red_to_plane = 90  # Red line stays at 90 degrees to blue
        self.plot_lines()
        plt.draw()

    def update_green_line_angle(self, angle):
        """Change the angle of the green line relative to the red line and update the plot."""
        self.angle_green_to_red = angle
        self.plot_lines()
        plt.draw()

    def show(self):
        plt.show()

# Example: create an instance of the class and adjust the angles of the lines
upper_leg_length = 108.5
lower_leg_length = 136.0
hip_to_shoulder = 50.0
body_width = 100
body_length = 200

sim = Sim(body_width, body_length, upper_leg_length, lower_leg_length, hip_to_shoulder)
sim.update_blue_line_angle(20)  # Angle of the blue line to the surface
sim.update_green_line_angle(-30)  # Angle of the green line relative to the red line
sim.show()
