import numpy
import sympy

from matplotlib import pyplot, animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

#to do. The part of code wiil delete after repair scale and add "changes end time"
'''
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

    def str_to_float(self, x):
        try:
            res = float(x)
            return res
        except:
            return None

    #change make after click button "Запуск". it is not good
    def update_xy_lim(self, bottom_x, bottom_y, up_x, up_y):
        bottom_x = self.str_to_float(bottom_x) if self.str_to_float(bottom_x) is not None else self.ax.get_xlim()[0]
        bottom_y = self.str_to_float(bottom_y) if self.str_to_float(bottom_y) is not None else self.ax.get_ylim()[0]
        up_x = self.str_to_float(up_x) if self.str_to_float(up_x) is not None else self.ax.get_xlim()[1]
        up_y = self.str_to_float(up_y) if self.str_to_float(up_y) is not None else self.ax.get_ylim()[1]

        self.ax.set_xlim(bottom_x, up_x)
        self.ax.set_ylim(bottom_y, up_y)

    def get_init(self):
        def init():
            self.line.set_data([], [])
            return self.line,
        return init

    def get_animate(self):
        def animate(i):
            x = numpy.linspace(self.plot_bottom_x, self.plot_up_x, self.num_x)
            y = self.function(x, self.time.t.get())
            self.time.next()
            self.controller.new_function(self.time.t.get())
            self.line.set_data(x, y)
            return self.line,
        return animate

    def clear(self):
        if self.animation is not None:
            self.animation.event_source.stop()

    def print_animation(self, function, plot_bottom_x, plot_up_x):
        self.clear()
        self.time.t.set(0.1)
        self.time.dt = 0.05

        self.max_delta_x = self.controller.get_max_delta_x()
        self.plot_bottom_x, self.plot_up_x = plot_bottom_x, plot_up_x
        self.num_x = int((self.plot_up_x - self.plot_bottom_x) / self.max_delta_x)

        self.function = function
        self.animation = animation.FuncAnimation(self.fig, self.get_animate(), init_func=self.get_init(),
                                       frames=200, interval=20, blit=True)

        self.parent.mainloop()
'''

class WriterPlot_new(tk.Frame):
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
        self.animation_pause = True


    def get_init(self):
        def init():
            self.line.set_data([], [])
            self.time.start_value()
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

    def print_animation(self, animation_plot):
        self.clear()

        self.animation_pause = False
        self.animation_plot = animation_plot
        self.animation = animation.FuncAnimation(self.fig, self.get_animate(), init_func=self.get_init(),
                                       frames=len(animation_plot.y), interval=20, blit=True)

        self.parent.mainloop()

    def pause_continue(self):
        if self.animation is None:
            return
        if self.animation_pause == True:
            self.animation.event_source.start()
            self.animation_pause = False
        else:
            self.animation_pause = True
            self.animation.event_source.stop()
