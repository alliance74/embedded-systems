import serial
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from math import radians, sin, cos
import time

ser = serial.Serial('COM3', 9600, timeout=1)
plt.style.use('seaborn-v0_8-darkgrid')
plt.ion()
fig = plt.figure(figsize=(12, 6))
fig.patch.set_facecolor('#0A0E1A')
ax_graph = fig.add_subplot(121)
ax_3d = fig.add_subplot(122, projection='3d')

cube = np.array([[1,1,1],[-1,1,1],[-1,-1,1],[1,-1,1],
                 [1,1,-1],[-1,1,-1],[-1,-1,-1],[1,-1,-1]])
faces = [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[0,3,7,4],[1,2,6,5]]
pitch_data, roll_data = [], []

ax_graph.set_facecolor('#0A0E1A')
ax_3d.set_facecolor('#0A0E1A')
ax_graph.tick_params(colors='white')
ax_3d.tick_params(colors='white')
for spine in ax_graph.spines.values():
    spine.set_color('white')
fig.suptitle("Live Orientation Tracker", color='cyan', fontsize=15, fontweight='bold')

def rotation_matrix(pitch, roll):
    p, r = radians(pitch), radians(roll)
    Rx = np.array([[1,0,0],[0,cos(r),-sin(r)],[0,sin(r),cos(r)]])
    Ry = np.array([[cos(p),0,sin(p)],[0,1,0],[-sin(p),0,cos(p)]])
    return Ry @ Rx

while True:
    try:
        line = ser.readline().decode(errors='ignore').strip().split(',')
        if len(line) < 2:
            continue
        pitch, roll = float(line[0]), float(line[1])
        pitch_data.append(pitch)
        roll_data.append(roll)
        if len(pitch_data) > 100:
            pitch_data.pop(0)
            roll_data.pop(0)

        ax_graph.clear()
        ax_graph.set_facecolor('#0A0E1A')
        ax_graph.plot(pitch_data, color='#00FF9C', linewidth=2, label='Pitch')
        ax_graph.plot(roll_data, color='#00BFFF', linewidth=2, label='Roll')
        ax_graph.set_ylim(-90, 90)
        ax_graph.legend(facecolor='#1A1E2B', edgecolor='white', labelcolor='white')
        ax_graph.set_title("Pitch & Roll Graph", color='white')
        ax_graph.tick_params(colors='white')
        for spine in ax_graph.spines.values():
            spine.set_color('white')

        R = rotation_matrix(pitch, roll)
        rotated_cube = cube @ R.T
        ax_3d.clear()
        for f in faces:
            ax_3d.add_collection3d(Poly3DCollection(
                [rotated_cube[f]],
                facecolors='#00FFFF',
                linewidths=1.2,
                edgecolors='white',
                alpha=0.3))
        ax_3d.set_xlim(-2, 2)
        ax_3d.set_ylim(-2, 2)
        ax_3d.set_zlim(-2, 2)
        ax_3d.set_title("3D Orientation Cube", color='white')
        ax_3d.view_init(elev=25, azim=35)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.03)
    except:
        continue
