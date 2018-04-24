import tkinter as tk
from tkinter import Frame
import tkinter.ttk as ttk
import sys
from main import gui_main_one_dimensional__wave_equtation


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
    def __init__(self, parent=None):
        Frame.__init__(self, parent, width=1000, height=500)

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

        run = tk.Button(self, text="Run", command=(lambda: gui_main_one_dimensional__wave_equtation(*self.myget())))
        run.pack()

        quit = tk.Button(self, text="Quit", command=parent.destroy)
        quit.pack()

    def myget(self):
        return (
                self.type_eq.get(),
                self.coef.get(),
                self.y__x_tzero.get(),
                self.dydt__x_tzero.get(),
                self.external_influences.get()
                )


if __name__ == '__main__':
    window = tk.Tk()
    my_gui = Gui(window)
    my_gui.pack()
    my_gui.pack_propagate(False)
    window.mainloop()
