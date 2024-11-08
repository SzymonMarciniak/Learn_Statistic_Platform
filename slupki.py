import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Przykładowe dane
data = [500, 700, 200, 900, 400]

def animate_barchart(i):
    for bar, height in zip(bars, data):
        bar.set_height(height * (i / 100))  # Rosnące wartości słupków

def start_animation():
    anim = FuncAnimation(fig, animate_barchart, frames=10, interval=2)
    canvas.draw()

# Konfiguracja GUI
root = tk.Tk()
fig, ax = plt.subplots()
bars = ax.bar(range(len(data)), [0] * len(data))  # Słupki startujące od zera

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Przycisk do uruchomienia animacji
button = tk.Button(root, text="Start Animation", command=start_animation)
button.pack()

root.mainloop()
