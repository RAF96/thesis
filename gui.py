import tkinter as tk
from tkinter import Frame
import sys
from main import gui_main_one_dimensional__wave_equtation__homogeneous


class Line(tk.Frame):
    def __init__(self, parent=None, **kwargs):
        Frame.__init__(self, parent)

        self.label = tk.Label(self, kwargs)
        self.label.pack()

        self.entry = tk.Entry(self, kwargs)
        self.entry.pack()

    def get(self):
        return self.entry.get()


class Gui(tk.Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent, width=1000, height=500)

        self.type_eq = Line(self, text="type_eq")
        self.type_eq.pack()

        self.y__x_tzero = Line(self, text="y__x_tzero")
        self.y__x_tzero.pack()
        
        self.dydt__x_tzero = Line(self, text="dydt__x__tzero")
        self.dydt__x_tzero.pack()
        
        self.coef = Line(self, text="coef")
        self.coef.pack()

        run = tk.Button(self, text="Run", command=(lambda: gui_main_one_dimensional__wave_equtation__homogeneous(*self.myget())))
        run.pack()

        quit = tk.Button(self, text="Quit", command=self.destroy)
        quit.pack()

    def myget(self):
        return (
                self.coef.get(),
                self.y__x_tzero.get(),
                self.dydt__x_tzero.get()
                )


if __name__ == '__main__':
    window = tk.Tk()
    my_gui = Gui(window)
    my_gui.pack()
    my_gui.pack_propagate(False)
    window.mainloop()
