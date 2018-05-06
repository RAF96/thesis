import tkinter as tk
from tkinter import Frame
import tkinter.ttk as ttk
from library_equation import gui_main_one_dimensional__wave_equtation
import controller
from writer_plot import WriterPlot


class LabelEntry(tk.Frame):
    def __init__(self, parent=None, kwargs_label={}, kwargs_entry={}, **kwargs):
        Frame.__init__(self, parent, kwargs)
        self.label = tk.Label(self, kwargs_label)
        self.label.pack()

        self.entry = tk.Entry(self, kwargs_entry)
        self.entry.pack()

    def get(self):
        return self.entry.get()


class LabelCombobox(tk.Frame):
    def __init__(self, parent=None, kwargs_label={}, kwargs_combobox={}, **kwargs):
        Frame.__init__(self, parent, kwargs)

        self.label = tk.Label(self, kwargs_label)
        self.label.pack()

        self.combobox = ttk.Combobox(self, **kwargs_combobox)
        self.combobox.pack()

    def get(self):
        return self.combobox.get()


class Gui(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.menu = Menu(self, controller)
        self.menu.pack(side=tk.LEFT)

        self.plot = Plot(self) 
        self.plot.pack(side=tk.RIGHT)

        self.quit = tk.Button(self, text="Quit", command=parent.destroy)
        self.quit.pack(side=tk.BOTTOM)

    def myget(self):
        return (
                self.type_eq.get(),
                self.coef.get(),
                self.y__x_tzero.get(),
                self.dydt__x_tzero.get(),
                self.external_influences.get()
                )


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        list_type_equtations = ["homogeneous", "inhomogeneous"]
        self.type_eq = LabelCombobox(self, kwargs_label={"text": "Type equation"}, kwargs_combobox={"values": list_type_equtations, "state": "readonly"})
        self.type_eq.pack()

        self.y__x_tzero = LabelEntry(self, kwargs_label={"text": "y__x_tzero"})
        self.y__x_tzero.pack()
        
        self.dydt__x_tzero = LabelEntry(self, kwargs_label={"text": "dydt__x__tzero"})
        self.dydt__x_tzero.pack()
        
        self.coef = LabelEntry(self, kwargs_label={"text": "coef"})
        self.coef.pack()

        self.external_influences = LabelEntry(self, kwargs_label={"text": "external_influences"})
        self.external_influences.pack()

        # run should clear previous graphic
        self.run = tk.Button(self, text="Run", command=(lambda: controller.run(*self.myget()))) # to do
        self.run.pack()

    def myget(self):
        return (
                self.type_eq.get(),
                self.coef.get(),
                self.y__x_tzero.get(),
                self.dydt__x_tzero.get(),
                self.external_influences.get()
                )


class Plot(tk.Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)

        self.writer_plot = WriterPlot(parent)
        self.writer_plot.pack()

        self.scale = ttk.Scale(self, orient=tk.HORIZONTAL, length=200, from_=1.0, to=100.0, command=(lambda change: self.myscale(change)))
        self.scale.pack()

    def myscale(self, change):
        print(change)
