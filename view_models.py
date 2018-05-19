import tkinter as tk

class Time:
    def __init__(self, t, dt):
        self.t = tk.DoubleVar(t)
        self.dt = dt

    def next(self):
        self.t.set(self.t.get() + self.dt)
