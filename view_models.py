import tkinter as tk
import numpy

class DisplayedTime:
    def __init__(self, t, dt):
        self.t = tk.DoubleVar(t)
        self.dt = dt

    def next(self):
        self.t.set(self.t.get() + self.dt)


class AnimationPlot:
    def __init__(self):
        self.time_start = 0
        self.time_finish = 100
        self.num_time_step = 1000

        self.start_x = 0
        self.end_x = 10
        dx = self.get_dx()
        self.num_x = int((self.end_x - self.start_x) / dx)

        self.y = list()
        self.x = numpy.linspace(self.start_x, self.end_x, self.num_x)
        self.t = numpy.linspace(self.time_start, self.time_finish, self.num_time_step)

    def get_dx(self):
        return ((self.time_finish - self.time_start) / self.num_time_step * 2) ** 0.5
