import tkinter as tk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Przykładowe dane do regresji liniowej
x = np.arange(0, 10, 0.5)
y = 2 * x + 1 + np.random.normal(scale=2, size=len(x))

def linear_regression_animation(i):
    line.set_data(x[:i], y_pred[:i])  # Aktualizowanie danych linii

def start_animation():
    global y_pred
    coeffs = np.polyfit(x, y, 1) 
    y_pred = np.polyval(coeffs, x)
    anim = FuncAnimation(fig, linear_regression_animation, frames=len(x), interval=100)
    canvas.draw()

# GUI i ustawienia
root = tk.Tk()
fig, ax = plt.subplots()
ax.scatter(x, y, color="blue")
line, = ax.plot([], [], color="red")  # Początkowo pusta linia

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

button = tk.Button(root, text="Start Animation", command=start_animation)
button.pack()

root.mainloop()
