import numpy
import sympy

from matplotlib import pyplot, animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

class WriterPlot(tk.Frame):

    def __init__(self, parent, time):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.time = time
        self.fig = Figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack()
        self.ax = self.fig.add_subplot(111, xlim=(-10, 10), ylim=(-10, 10))
        self.line, = self.ax.plot([], [], color='r')
        self.ax.axhline(y=0, color='b')
        self.ax.axvline(x=0, color='b')
        self.animation = None

    def get_init(self):
        def init():
            self.line.set_data([], [])
            return self.line,
        return init

    def get_animate(self):
        def animate(i):
            x = numpy.linspace(-11, 11, 100)
            y = self.function(x, self.time.t.get())
            self.time.next()
            self.line.set_data(x, y)
            return self.line,
        return animate

    def clear(self):
        if self.animation is not None:
            self.animation.event_source.stop()

    def print_animation(self, function):
        self.clear()
        self.time.t.set(0.1)
        self.time.dt = 0.05
        self.function = function
        # self.function = sympy.lambdify((sympy.abc.x, sympy.abc.t), function)
        self.animation = animation.FuncAnimation(self.fig, self.get_animate(), init_func=self.get_init(),
                                       frames=200, interval=20, blit=True)

        self.parent.mainloop()
