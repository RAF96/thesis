import tkinter as tk
import pymongo
from library_equation import gui_main_one_dimensional__equation
from writer_plot import WriterPlot
import gui


class Controller:

    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client.test_database

        self.window = tk.Tk()
        self.window.attributes()
        self.my_gui = gui.Gui(self.window, self)
        self.my_gui.master.maxsize(800, 600)
        self.my_gui.pack()
        self.window.mainloop()

    def run(self, *args):
        equation = gui_main_one_dimensional__equation(*args)
        self.my_gui.plot.writer_plot.print_animation(equation)

    def pause_continue(self, *args):
        if self.my_gui.plot.writer_plot.time.dt != 0:
            self.my_gui.plot.writer_plot.time.dt = 0
        else:
            self.my_gui.plot.writer_plot.time.dt = 0.05

    def get_names_saved_equations(self):
        if not self.db.equations:
            return tuple()
        return (element["name"] for element in self.db.equations.find())

    def save(self, *args):
        equation = {
            "name": args[0],
            "type_equation": args[1],
            "coef": args[2],
            "y__x_tzero": args[3],
            "dydt__x_tzero": args[4],
            "external_influences": args[5]
        }
        self.db.equations.insert_one(equation)
        self.my_gui.menu_choose_saved.listbox.insert(tk.END, equation["name"])

    def delete_equation(self, name):
        self.db.equations.delete_one({"name": name})
        self.my_gui.menu_choose_saved.listbox.delete("active")

    def insert_equation(self, name):
        equation = self.db.equations.find_one({"name": name})
        self.my_gui.menu.set(equation)
