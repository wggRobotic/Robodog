import matplotlib.pyplot as plt
import numpy as np
import mpld3
from flask import Flask, render_template_string

app = Flask(__name__)
leg_positions = []  

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Leg Position Projection</title>
</head>
<body>
    <h1>Leg Position Projection (XZ Plane)</h1>
    {{ plot_html|safe }}
</body>
</html>
"""

def plot_leg_positions(positions):
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.suptitle("Leg Position Projection (XZ Plane)")
    
    colors = ['r', 'g', 'b', 'c']  #
    
    for leg_idx in range(4):  
        color = colors[leg_idx]
        x_vals = [pos[leg_idx][0] for pos in positions]  # X
        z_vals = [pos[leg_idx][2] for pos in positions]  # Z
        
        ax.plot(x_vals, z_vals, marker='o', linestyle='-', color=color, label=f'Leg {leg_idx+1}')
    
    ax.set_title("XZ Projection")
    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    ax.legend()
    
    return mpld3.fig_to_html(fig)

@app.route("/")
def index():
    plot_html = plot_leg_positions(leg_positions)
    return render_template_string(HTML_TEMPLATE, plot_html=plot_html)

def start_server(positions):
    global leg_positions
    leg_positions = positions
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    example_positions = [
        [[0, 0, 0], [1, 1, 0], [2, 2, 1], [3, 3, 2]],
        [[0, 0, 1], [1, -1, 1], [2, -2, 2], [3, -3, 3]],
        [[0, 0, 2], [1, 1, 2], [2, 2, 3], [3, 3, 4]],
        [[0, 0, 3], [1, -1, 3], [2, -2, 4], [3, -3, 5]]
    ]
    start_server(example_positions)
