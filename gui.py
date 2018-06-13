import tkinter as tk
from tkinter import Frame
import tkinter.ttk as ttk
import controller
from writer_plot import WriterPlot
from view_models import Time


class LabelEntry(tk.Frame):
    def __init__(self, parent, kwargs_label={}, **kwargs):
        Frame.__init__(self, parent, kwargs)
        self.label = tk.Label(self, kwargs_label)
        self.label.pack()

        self.entry_text = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entry_text)
        self.entry.pack()

    def get(self):
        return self.entry.get()


class LabelCombobox(tk.Frame):
    def __init__(self, parent, kwargs_label={}, kwargs_combobox={}, **kwargs):
        Frame.__init__(self, parent, kwargs)
        self.parent = parent

        self.label = tk.Label(self, kwargs_label)
        self.label.pack()

        self.combobox = ttk.Combobox(self, **kwargs_combobox)
        self.combobox.pack()
        self.combobox.bind("<<ComboboxSelected>>", self.parent.change_visibility_elements)

    def get(self):
        return self.combobox.get()


class Gui(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.width=800
        self.height=600

        self.menu_choose_saved = MenuChooseSaved(self, controller)
        self.menu_choose_saved.pack(side=tk.LEFT)

        self.menu = Menu(self, controller)
        self.menu.pack(side=tk.LEFT)

        self.plot = Plot(self, controller)
        self.plot.pack(side=tk.LEFT)

        self.quit = tk.Button(self, text="Выход", command=parent.destroy)
        self.quit.pack(side=tk.BOTTOM)


class Menu(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        list_type_equtations = ["волновое уравнение",
                                "уравнение теплопроводности"]
        self.type_equation = LabelCombobox(self, kwargs_label={"text": "Тип уравнения"}, kwargs_combobox={"values": list_type_equtations, "state": "readonly"})
        self.type_equation.pack()

        list_type_tasks = ["Задача Коши", "Первая краевая задача", "Вторая краевая задача", "Третья краевая задача"]
        self.type_task = LabelCombobox(self, kwargs_label={"text": "Тип граничных условий"}, kwargs_combobox={"values": list_type_tasks, "state": "readonly"})
        self.type_task.pack()

        self.coef = LabelEntry(self, kwargs_label={"text": "Коэффициент"})
        self.coef.pack()

        self.external_influences = LabelEntry(self, kwargs_label={"text": "Cвободный член"})
        self.external_influences.pack()

        self.y__x_tzero = LabelEntry(self, kwargs_label={"text": "u(x,0)"})
        self.y__x_tzero.pack()

        self.dydt__x_tzero = LabelEntry(self, kwargs_label={"text": "(du/dt)(x, 0)"})

        self.y__xzero_t = LabelEntry(self, kwargs_label={"text": "u(0, t)"})

        self.xeql = LabelEntry(self, kwargs_label={"text": "Конечная точка l"})

        self.y__xeql_t = LabelEntry(self, kwargs_label={"text": "u(l, t)"})

        self.run = tk.Button(self, text="Запуск", command=(lambda: controller.run(self.get_value())))
        self.run.pack(side=tk.BOTTOM)

        self.run = tk.Button(self, text="Сохранить", command=(lambda: self.save()))
        self.run.pack(side=tk.BOTTOM)

    def change_visibility_elements(self, *args):
        type_equation = self.type_equation.get()
        type_task = self.type_task.get()
        if type_equation == "волновое уравнение":
            self.dydt__x_tzero.pack()
        else:
            self.dydt__x_tzero.pack_forget()

        if type_task == "Первая краевая задача":
            self.y__xzero_t.pack()
            self.xeql.pack()
            self.y__xeql_t.pack()
        else:
            self.y__xzero_t.pack_forget()
            self.xeql.pack_forget()
            self.y__xeql_t.pack_forget()


    def get_value(self):
        x = controller.InputData()
        x.update(
            {
                "supporting_data":
                {
                    "type_equation": self.type_equation.get(),
                    "type_task": self.type_task.get(),

                },
                "entry_conditions":
                {
                    "coef": self.coef.get(),
                    "external_influences": self.external_influences.get(),
                    "y__x_tzero": self.y__x_tzero.get(),
                    "dydt__x_tzero": self.dydt__x_tzero.get(),
                },
                "boundary_values":
                {
                    "y__xzero_t": self.y__xzero_t.get(),
                    "xeql": self.xeql.get(),
                    "y__xeql_t": self.y__xeql_t.get(),
                }
            }
        )
        return x

    # Add boundary_values
    def set(self, equation):
        if equation.get("type_equation") is not None:
            self.type_equation.combobox.set(equation["type_equation"])
        if equation.get("type_task") is not None:
            self.type_task.combobox.set(equation["type_task"])
        if equation.get("coef") is not None:
            self.coef.entry_text.set(equation["coef"])
        if equation.get("y__x_tzero") is not None:
            self.y__x_tzero.entry_text.set(equation["y__x_tzero"])
        if equation.get("dydt__x_tzero") is not None:
            self.dydt__x_tzero.entry_text.set(equation["dydt__x_tzero"])
        if equation.get("external_influences") is not None:
            self.external_influences.entry_text.set(equation["external_influences"])

        if equation.get("y__xzero_t") is not None:
            self.y__xzero_t.entry_text.set(equation["y__xzero_t"])
        if equation.get("xeql") is not None:
            self.xeql.entry_text.set(equation["xeql"])
        if equation.get("y__xeql_t") is not None:
            self.y__xeql_t.entry_text.set(equation["y__xeql_t"])
        self.change_visibility_elements()

    def save(self):
        toplevel = tk.Toplevel()
        toplevel.focus_set()
        new_window_for_save = NewWindowForSave(toplevel, self.controller, self.get_value())
        new_window_for_save.pack()



class NewWindowForSave(tk.Frame):
    def __init__(self, parent, controller, input_data):
        Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.name = LabelEntry(self, kwargs_label={"text": "Название примера"})
        self.name.pack()

        self.button = tk.Button(self, text="Отправить", command=(lambda: self.command(input_data)))
        self.button.pack()

    def command(self, input_data):
        self.controller.save(self.name.get(), input_data)
        self.parent.destroy()


class Plot(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.time = Time(0, 0.05)

        self.writer_plot = WriterPlot(parent, self.time)
        self.writer_plot.pack()

        self.button = tk.Button(self, text="Пауза/Продолжить", command=(lambda: controller.pause_continue()))
        self.button.pack()


        self.scale = ttk.Scale(
                               self,
                               variable=self.time.t,
                               orient=tk.HORIZONTAL,
                               length=200,
                               from_=0.1,
                               to=100.0
                               )
        self.scale.pack()

    def change_to(self, text):
        self.scale.to = float(text)


class MenuChooseSaved(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Выбрать сохраненный график")
        self.label.pack()

        self.listbox = tk.Listbox(self)
        self.listbox.pack()

        names = controller.get_names_saved_equations()

        for name in names:
            self.listbox.insert(tk.END, name)

        self.button_insert = tk.Button(self, text="Подставить", command=(lambda: controller.insert_equation(self.listbox.get("active"))))
        self.button_insert.pack()

        self.button_delete = tk.Button(self, text="Удалить", command=(lambda: controller.delete_equation(self.listbox.get("active"))))
        self.button_delete.pack()

        self.border_menu = MenuBorder(self, controller)
        self.border_menu.pack(side=tk.BOTTOM)



class MenuBorder(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.bottom_x = LabelEntry(self, kwargs_label={"text": "Левая граница Оси x"})
        self.bottom_x.pack()

        self.bottom_y = LabelEntry(self, kwargs_label={"text": "Левая граница Оси y"})
        self.bottom_y.pack()

        self.up_x = LabelEntry(self, kwargs_label={"text": "Правая граница Оси x"})
        self.up_x.pack()

        self.up_y = LabelEntry(self, kwargs_label={"text": "Правая граница Оси y"})
        self.up_y.pack()

        self.button = tk.Button(self, text="Применить", command=(lambda: controller.change_border_for_writer(*self.get_value())))
        self.button.pack()

    def get_value(self):
        return (
                self.bottom_x.get(),
                self.bottom_y.get(),
                self.up_x.get(),
                self.up_y.get()
                )

