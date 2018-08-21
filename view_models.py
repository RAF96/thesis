import tkinter as tk
import numpy
import bisect

class DisplayedTime:
    def __init__(self, controller, t, dt):
        self.controller = controller
        self.t = t
        self.view_t = tk.DoubleVar(t)
        self.dt = dt

    def next(self):
        self.t = self.t + self.dt
        self.view_t.set(round(self.t, 1))

    def change_time(self, time):
        self.t = time
        self.update()

    def update(self):
        self.controller.update_view_time()

    def start_value(self):
        self.t = 0


class AnimationPlot:
    def __init__(self, time_start, time_finish, start_x, end_x):
        self.time_start = time_start # 0
        self.time_finish = time_finish # 100
        self.dt = 0.05

        self.start_x = start_x # 0
        self.end_x = end_x # 10

        self.y = list()

    def get_x(self):
        return numpy.linspace(self.start_x, self.end_x, self.get_num_x())

    def get_t(self):
        return numpy.linspace(self.time_start, self.time_finish, self.get_num_time_step())

    def get_dx(self):
        return (self.get_dt() * 2) ** 0.5

    def get_dt(self):
        return self.dt

    def get_num_time_step(self):
        return int((self.time_finish - self.time_start) / self.dt)

    def get_num_x(self):
        return int((self.end_x - self.start_x) / self.get_dx())

    def clean_result_part(self):
        self.y = list()

    def change_time_finish(self, time_finish):
        self.time_finish = time_finish
        self.clean_result_part()

    def get_index_by_time(self, time):
        return bisect.bisect_left(self.get_t(), time)

    def change_start_x(self, x):
        self.start_x = x
        self.clean_result_part()


class ChangerAnimationPlot:
    def __init__(self, controller):
        self.controller = controller
        self.animation_plot = None
        self.time_finish = 100
        # self.animation_plot = AnimationPlot(0, 100, 0, 10)

    def start_new(self, input_data):
        self.input_data = input_data
        from library_equation.library_equation import gui_main_one_dimensional__equation
        if input_data["supporting_data"]["type_task"] == "Задача Коши":
            x_bottom, x_up = self.controller.get_lim_border_x()
            self.animation_plot = AnimationPlot(0, self.time_finish, x_bottom, x_up)
        else:
            self.animation_plot = AnimationPlot(0, self.time_finish, 0, float(input_data["boundary_values"]["xeql"]))

        gui_main_one_dimensional__equation(self.animation_plot, input_data)
        return self.animation_plot

    def change_finish_time(self, time_finish):
        self.time_finish = time_finish
        if self.animation_plot is not None:
            self.animation_plot.change_time_finish(time_finish)
        if hasattr(self, "input_data"):
            self.restart()

    def restart(self):
        from library_equation.library_equation import gui_main_one_dimensional__equation
        gui_main_one_dimensional__equation(self.animation_plot, self.input_data)
        return self.animation_plot


class LimBorder:
    def __init__(self):
        self.bottom_x = -10
        self.bottom_y = -10
        self.up_x = 10
        self.up_y = 10

    def update(self, bottom_x, bottom_y, up_x, up_y):
        self.bottom_x, self.bottom_y, self.up_x, self.up_y = bottom_x, bottom_y, up_x, up_y

    def get_x(self):
        return self.bottom_x, self.up_x
