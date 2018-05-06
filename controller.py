import tkinter as tk
from library_equation import gui_main_one_dimensional__wave_equtation
from writer_plot import WriterPlot
import gui


class Controller:
   
    def __init__(self):
        self.window = tk.Tk()
        self.window.attributes("-zoomed", True)
        self.my_gui = gui.Gui(self.window, self)
        self.my_gui.pack(side="left")
        self.window.mainloop()

    def run(self, *args):
        equation = gui_main_one_dimensional__wave_equtation(*args)
        self.my_gui.plot.writer_plot.print_animation(equation)


