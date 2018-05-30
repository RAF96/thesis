import tkinter as tk
from tkinter import Frame
import tkinter.ttk as ttk
import controller
from writer_plot import WriterPlot
from view_models import Time


class LabelEntry(tk.Frame):
    def __init__(self, parent=None, kwargs_label={}, **kwargs):
        Frame.__init__(self, parent, kwargs)
        self.label = tk.Label(self, kwargs_label)
        self.label.pack()

        self.entry_text = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entry_text)
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

        self.coef = LabelEntry(self, kwargs_label={"text": "Коэффициент"})
        self.coef.pack()

        self.y__x_tzero = LabelEntry(self, kwargs_label={"text": "u(x,0)"})
        self.y__x_tzero.pack()

        self.dydt__x_tzero = LabelEntry(self, kwargs_label={"text": "(du/dt)(x, 0)"})
        self.dydt__x_tzero.pack()

        self.external_influences = LabelEntry(self, kwargs_label={"text": "Cвободный член"})
        self.external_influences.pack()

        #Warning run should clear previous graphic
        self.run = tk.Button(self, text="Запуск", command=(lambda: controller.run(*self.get_value())))
        self.run.pack()

        self.run = tk.Button(self, text="Сохранить", command=(lambda: self.save()))
        self.run.pack()

    def get_value(self):
        return (
                self.type_equation.get(),
                self.coef.get(),
                self.y__x_tzero.get(),
                self.dydt__x_tzero.get(),
                self.external_influences.get()
                )

    def set(self, equation):
        self.type_equation.combobox.set(equation["type_equation"])
        self.coef.entry_text.set(equation["coef"])
        self.y__x_tzero.entry_text.set(equation["y__x_tzero"])
        self.dydt__x_tzero.entry_text.set(equation["dydt__x_tzero"])
        self.external_influences.entry_text.set(equation["external_influences"])

    def save(self):
        toplevel = tk.Toplevel()
        toplevel.focus_set()
        new_window_for_save = NewWindowForSave(toplevel, self.controller, *self.get_value())
        new_window_for_save.pack()



class NewWindowForSave(tk.Frame):
    def __init__(self, parent, controller, *args):
        Frame.__init__(self, parent)

        self.parent = parent
        self.controller = controller

        self.name = LabelEntry(self, kwargs_label={"text": "Название примера"})
        self.name.pack()

        self.button = tk.Button(self, text="Отправить", command=(lambda: self.command(*args)))
        self.button.pack()

    def command(self, *args):
        self.controller.save(self.name.get(), *args)
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
