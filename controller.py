import tkinter as tk
import gui
from view_models import ChangerAnimationPlot
import json
from pathlib import Path
import os


class Controller:

    def __init__(self):
        self.db = DB("data")
        self.db.create_table("equations")

        self.changer_animation_plot = ChangerAnimationPlot(self)

        self.window = tk.Tk()
        self.window.attributes()
        self.my_gui = gui.Gui(self.window, self)
        self.my_gui.master.minsize(1000, 600)
        self.my_gui.pack()
        self.window.mainloop()

    def start_new(self, input_data):
        self.input_data = input_data
        equation = self.changer_animation_plot.start_new(input_data)
        self.my_gui.plot.writer_plot.print_animation(equation)

    def change_finish_time(self, finish_time):
        self.my_gui.plot.writer_plot.clear()
        self.changer_animation_plot.change_finish_time(finish_time)
        if hasattr(self, "input_data"):
            self.my_gui.plot.writer_plot.print_animation(self.changer_animation_plot.animation_plot)

    def get_names_saved_equations(self):
        if not self.db.equations:
            return tuple()
        return (element for element in self.db.equations.find())

    def save(self, name, input_data):
        equation = {name : {"name": name}}
        for key1, value1 in input_data.items():
            equation[name].update(value1)

        self.db.equations.insert_one(equation)
        self.my_gui.menu_choose_saved.listbox.insert(tk.END, name)

    def delete_equation(self, name):
        self.db.equations.delete_one({"name": name})
        self.my_gui.menu_choose_saved.listbox.delete("active")

    def insert_equation(self, name):
        equation = self.db.equations.find_one({"name": name})
        self.my_gui.menu.set(equation)

    def change_border_for_writer(self, *args):
        self.my_gui.plot.writer_plot.update_xy_lim(*list(map(float, args)))

    def update_view_time(self):
        self.my_gui.plot.writer_plot.update_view_time()

    def get_lim_border_x(self):
        return self.my_gui.plot.writer_plot.xy_lim.get_x()


class DB:
    def __init__(self, name):
        self.name = name
        self.path = "./" + name

        directory = self.path # os.path.dirname(self.path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def create_table(self, name):
        self.__setattr__(name, TableBD(self.path, name))


class TableBD:
    def __init__(self, path_db, name):
        self.name = name
        self.path = "%s/%s.json" % (path_db, name)

        if Path(self.path).exists() is False:
            outfile = open(self.path, "w")
            json.dump(dict(), outfile, sort_keys=True, indent=4)

    def find(self):
        data = None
        with open(self.path, "r") as infile:
            data = json.load(infile)
        return data

    def insert_one(self, equation):
        data = None
        with open(self.path, "r") as infile:
            data = json.load(infile)
        data.update(equation)
        with open(self.path, "w") as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def delete_one(self, name):
        data = None
        with open(self.path, "r") as infile:
            data = json.load(infile)
        data.pop(name["name"])
        with open(self.path, "w") as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def find_one(self, name):
        data = None
        with open(self.path, "r") as infile:
            data = json.load(infile)
        return data[name["name"]]



class InputData():
    def __init__(self):
        self.dict = dict()
        self.list = "supporting_data", "entry_conditions", "boundary_values"

        list_supporting_data = "type_task", "type_equation"
        self.dict.update({"supporting_data": {e : None for e in list_supporting_data}})

        list_entry_conditions = "coef", "y__x_tzero", "dydt__x_tzero"
        self.dict.update({"entry_conditions": {e : None for e in list_entry_conditions}})

        list_boundary_values = "xeql", "y__xzero_t", "y__xeql_t", \
                "dydx__xzero_t", "dydx__xeql_t", \
                "a__xzero", "b__xzero", "third_boundary_function__xzero", \
                "a__xeql", "b__xeql", "third_boundary_function__xeql",

        self.dict.update({"boundary_values": {e : None for e in list_boundary_values}})

    def __getitem__(self, index):
        return self.dict[index]

    def update(self, element):
        self.dict.update(element)

    def get(self, *args):
        result = list()
        for e in args:
            flag = False
            for value in self.dict.values():
                if value.get(e) is not None:
                    result.append(value[e])
                    flag = True
                    break
            if flag is False:
                raise NameError("InputData haven't the element: " + e)
        return result

    def items(self):
        return self.dict.items()

    def __str__(self):
        return "InputData:\n" + str(self.dict)
