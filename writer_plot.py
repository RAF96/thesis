import numpy
import sympy

from matplotlib import pyplot, animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk


class WriterPlot(tk.Frame):
    def __init__(self, parent, controller, time):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.time = time
        self.fig = Figure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.get_tk_widget().pack()
        self.ax = self.fig.add_subplot(111, xlim=(-10, 10), ylim=(-10, 10))
        self.line, = self.ax.plot([], [], color='r')
        self.ax.axhline(y=0, color='b')
        self.ax.axvline(x=0, color='b')
        self.animation = None
        self.animation_plot = None
        self.animation_pause = True
        self.get_init()()


    def get_init(self):
        def init():
            self.line.set_data([], [])
            self.time.start_value()
            self.shift = 0
            self.i = 0
            return self.line,
        return init

    def get_animate(self):
        def animate(i):
            self.line.set_data(self.animation_plot.x, self.animation_plot.y[i])
            self.time.next()
            return self.line,
        return animate

    def clear(self):
        if self.animation is not None:
            self.canvas.get_tk_widget().pack_forget()
            self.animation.event_source.stop()
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent)
            self.canvas.get_tk_widget().pack()

    def get_frame(self):
        def foo():
            while True:
                self.i = 0
                while self.i < self.animation_len:
                    yield self.i
                    self.i += 1
        return foo()


    def print_animation(self, animation_plot):
        self.clear()

        self.animation_pause = False
        self.animation_plot = animation_plot
        self.animation_len = len(animation_plot.y)

        self.animation = animation.FuncAnimation(self.fig, self.get_animate(), init_func=self.get_init(),
                                       frames=self.get_frame(), interval=20, blit=True)

        self.parent.mainloop()

    def change_animation_index(self, index):
        self.i = index
        if self.animation is not None:
            self.animation.new_frame_seq()

    def update_view_time(self):
        if self.animation_plot is not None:
            self.change_animation_index(self.animation_plot.get_index_by_time(self.time.t))

    def pause_continue(self):
        if self.animation is None:
            return
        if self.animation_pause == True:
            self.animation.event_source.start()
            self.animation_pause = False
        else:
            self.animation_pause = True
            self.animation.event_source.stop()
