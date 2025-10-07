import serial
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
import numpy as np

ser = serial.Serial('COM3', 9600, timeout=1)
plt.style.use('seaborn-v0_8-darkgrid')
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 9))
fig.patch.set_facecolor('#101820')
ax1.set_facecolor('#101820')
ax2.set_facecolor('#101820')
fig.suptitle("Live Pitch Monitor", fontsize=15, color='cyan', fontweight='bold')

line, = ax1.plot([], [], color='#00FF9C', linewidth=2)
pitch_data = []
ax1.set_xlim(0, 100)
ax1.set_ylim(-90, 90)
ax1.tick_params(colors='white')
ax1.spines['bottom'].set_color('white')
ax1.spines['top'].set_color('white')
ax1.spines['left'].set_color('white')
ax1.spines['right'].set_color('white')
ax1.set_xlabel("Samples", color='white')
ax1.set_ylabel("Pitch (°)", color='white')

rect = Rectangle((-0.5, -0.5), 1, 1, fc='#00BFFF', ec='white', lw=2)
ax2.add_patch(rect)
ax2.set_xlim(-2, 2)
ax2.set_ylim(-2, 2)
ax2.set_aspect('equal')
ax2.set_title("Orientation View", color='white')

def update(frame):
    try:
        data = ser.readline().decode(errors='ignore').strip().split(',')
        if not data or len(data[0]) == 0:
            return line, rect
        pitch = float(data[0])
        pitch_data.append(pitch)
        if len(pitch_data) > 100:
            pitch_data.pop(0)
        x = np.arange(len(pitch_data))
        line.set_data(x, pitch_data)
        rect.angle = pitch
        ax1.relim()
        ax1.autoscale_view()
    except:
        pass
    return line, rect

ani = FuncAnimation(fig, update, interval=50, blit=False)
plt.show()
