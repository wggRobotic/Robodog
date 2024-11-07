import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D, art3d
import numpy as np

class Sim:
    def __init__(self, line_length=1):
        self.line_length = line_length
        self.x = [0, 1, 1, 0]  # x-Koordinaten der Ecken
        self.y = [0, 0, 1, 1]  # y-Koordinaten der Ecken
        self.z = [0, 0, 0, 0]  # z-Koordinaten der Ecken (alle auf derselben Höhe)
        
        # Verschiebung des Rechtecks, so dass der Punkt (1, 1, 0) auf (0, 0, 0) verschoben wird
        self.shift_x = 1
        self.shift_y = 1
        self.shift_z = 0
        
        # Initialer Winkel für die Linien
        self.angle_blue_to_plane = 0  # Winkel der blauen Linie zur Fläche (0 für waagerecht)
        self.angle_red_to_plane = 0  # Winkel der roten Linie zur Fläche
        self.angle_green_to_red = 0  # Winkel der grünen Linie zur roten Linie
        
        # Plot initialisieren
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        
        # Fläche und Linien erstellen
        self.plot_surface()
        self.plot_lines()
        
        # Achsenbeschriftungen hinzufügen
        self.ax.set_xlabel('X-Achse')
        self.ax.set_ylabel('Y-Achse')
        self.ax.set_zlabel('Z-Achse')
        
    def plot_surface(self):
        # Verschiebe die Fläche, indem wir den Vektor subtrahieren
        x_shifted = [x - self.shift_x for x in self.x]
        y_shifted = [y - self.shift_y for y in self.y]
        z_shifted = [z - self.shift_z for z in self.z]
        
        verts = [list(zip(x_shifted, y_shifted, z_shifted))]
        self.ax.add_collection3d(art3d.Poly3DCollection(verts, color="lightblue", alpha=0.6))
        
    def plot_lines(self):
        # Lösche vorherige Linien
        self.ax.cla()
        self.plot_surface()
        
        # 4 Beine (links und rechts von der Fläche)
        for i in range(4):
            # Verschiebe die Startpunkte der Linien
            x_start, y_start, z_start = self.x[i] - self.shift_x, self.y[i] - self.shift_y, self.z[i] - self.shift_z
            
            # Berechne den Winkel der blauen Linie zur Fläche
            if i == 0:  # vorne links
                x_end_blue = x_start
                y_end_blue = y_start - self.line_length * np.cos(np.radians(self.angle_blue_to_plane))  # Blaue Linie nach unten/oben
                z_end_blue = z_start + self.line_length * np.sin(np.radians(self.angle_blue_to_plane))
            elif i == 1:  # vorne rechts
                x_end_blue = x_start
                y_end_blue = y_start - self.line_length * np.cos(np.radians(self.angle_blue_to_plane))  # Blaue Linie nach unten/oben
                z_end_blue = z_start + self.line_length * np.sin(np.radians(self.angle_blue_to_plane))
            elif i == 2:  # hinten rechts
                x_end_blue = x_start
                y_end_blue = y_start + self.line_length * np.cos(np.radians(self.angle_blue_to_plane))  # Blaue Linie nach unten/oben
                z_end_blue = z_start + self.line_length * np.sin(np.radians(self.angle_blue_to_plane))
            else:  # hinten links
                x_end_blue = x_start
                y_end_blue = y_start + self.line_length * np.cos(np.radians(self.angle_blue_to_plane))  # Blaue Linie nach unten/oben
                z_end_blue = z_start + self.line_length * np.sin(np.radians(self.angle_blue_to_plane))
                
            # Blaue Linie zeichnen
            self.ax.plot([x_start, x_end_blue], [y_start, y_end_blue], [z_start, z_end_blue], color="blue")  # Blaue Linie

            # Rote Linie: Beginnt an der Endposition der blauen Linie
            x_end_red = x_end_blue + self.line_length * np.cos(np.radians(self.angle_red_to_plane))
            y_end_red = y_end_blue
            z_end_red = z_end_blue - self.line_length * np.sin(np.radians(self.angle_red_to_plane))
            
            # Rote Linie zeichnen
            self.ax.plot([x_end_blue, x_end_red], [y_end_blue, y_end_red], [z_end_blue, z_end_red], color="red")
            
            # Berechnung der grünen Linie relativ zur roten Linie
            direction_vector = np.array([x_end_red - x_end_blue, y_end_red - y_end_blue, z_end_red - z_end_blue])
            direction_vector /= np.linalg.norm(direction_vector)  # Normierung auf Einheitslänge
            rotation_matrix = self.rotation_matrix_y(self.angle_green_to_red)
            rotated_vector = np.dot(rotation_matrix, direction_vector) * self.line_length
            x_end_green = x_end_red + rotated_vector[0]
            y_end_green = y_end_red + rotated_vector[1]
            z_end_green = z_end_red + rotated_vector[2]
            
            # Grüne Linie zeichnen
            self.ax.plot([x_end_red, x_end_green], [y_end_red, y_end_green], [z_end_red, z_end_green], color="green")
            
    def rotation_matrix_y(self, angle):
        """Rotation um die Y-Achse für den Winkel in Grad."""
        angle_rad = np.radians(angle)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        return np.array([
            [cos_a, 0, sin_a],
            [0, 1, 0],
            [-sin_a, 0, cos_a]
        ])
        
    def update_blue_line_angle(self, angle):
        """Ändert den Winkel der blauen Linie zur Fläche und aktualisiert den Plot."""
        self.angle_blue_to_plane = angle
        self.plot_lines()
        plt.draw()
        
    def update_red_line_angle(self, angle):
        """Ändert den Winkel der roten Linie zur Fläche und aktualisiert den Plot."""
        self.angle_red_to_plane = angle
        self.plot_lines()
        plt.draw()
        
    def update_green_line_angle(self, angle):
        """Ändert den Winkel der grünen Linie relativ zur roten Linie und aktualisiert den Plot."""
        self.angle_green_to_red = angle
        self.plot_lines()
        plt.draw()
        
    def show(self):
        plt.show()

# Beispiel: Instanz der Klasse erstellen und Winkel der Linien anpassen
sim = Sim(line_length=1)
sim.update_blue_line_angle(30)  # Winkel der blauen Linie zur Fläche
sim.update_red_line_angle(45)   # Winkel der roten Linie zur Fläche
sim.update_green_line_angle(-30)  # Winkel der grünen Linie relativ zur roten Linie
sim.show()
