import tkinter as tk

from controller import DataController
from model import DataModel
from view import DataView

if __name__ == "__main__":
    root = tk.Tk()
    view = DataView(root)
    model = DataModel()
    controller = DataController()
    root.mainloop()