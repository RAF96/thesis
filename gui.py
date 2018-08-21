import tkinter as tk
from tkinter import Frame
import tkinter.ttk as ttk
import controller
from writer_plot import WriterPlot
from view_models import DisplayedTime, LimBorder


class LabelEntry(tk.Frame):
    def __init__(self, parent, kwargs_label={}, kwargs_entry={}, **kwargs):
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

        self.plot = GuiPlot(self, controller)
        self.plot.pack(side=tk.LEFT)


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

        # boundary value problem
        self.xeql = LabelEntry(self, kwargs_label={"text": "Конечная точка l"})

        # 1 boundary value problem
        self.y__xzero_t = LabelEntry(self, kwargs_label={"text": "u(0, t)"})
        self.y__xeql_t = LabelEntry(self, kwargs_label={"text": "u(l, t)"})

        # 2 boundary value problem
        self.dydx__xzero_t = LabelEntry(self, kwargs_label={"text": "(du/dx)(0, t)"})
        self.dydx__xeql_t = LabelEntry(self, kwargs_label={"text": "(du/dx)(l, t)"})

        # 3 boundary value problem
        self.a__xzero = LabelEntry(self, kwargs_label={"text": "coef при u(0,t)"})
        self.b__xzero = LabelEntry(self, kwargs_label={"text": "coef при (du/dx)(0,t)"})
        self.third_boundary_function__xzero = LabelEntry(self, kwargs_label={"text": "Чему равна a*u(0, t) + b*(du/dx)(0, t)"})

        self.a__xeql = LabelEntry(self, kwargs_label={"text": "coef при u(l,t)"})
        self.b__xeql = LabelEntry(self, kwargs_label={"text": "coef при (du/dx)(l,t)"})
        self.third_boundary_function__xeql = LabelEntry(self, kwargs_label={"text": "Чему равна a*u(l, t) + b*(du/dx)(l, t)"})


        self.start_new_animation = tk.Button(self, text="Запуск", command=(lambda: controller.start_new(self.get_value())))
        self.start_new_animation.pack(side=tk.BOTTOM)

        self.button_save = tk.Button(self, text="Сохранить", command=(lambda: self.save()))
        self.button_save.pack(side=tk.BOTTOM)

    def change_visibility_elements(self, *args):
        type_equation = self.type_equation.get()
        type_task = self.type_task.get()

        if type_equation == "волновое уравнение":
            self.dydt__x_tzero.pack()
        else:
            self.dydt__x_tzero.pack_forget()

        # boundary value problem
        self.xeql.pack_forget()

        # 1 boundary value problem
        self.y__xzero_t.pack_forget()
        self.y__xeql_t.pack_forget()

        # 2 boundary value problem
        self.dydx__xzero_t.pack_forget()
        self.dydx__xeql_t.pack_forget()

        # 3 boundary value problem
        self.a__xzero.pack_forget()
        self.b__xzero.pack_forget()
        self.third_boundary_function__xzero.pack_forget()

        self.a__xeql.pack_forget()
        self.b__xeql.pack_forget()
        self.third_boundary_function__xeql.pack_forget()

        if type_task == "Первая краевая задача":
            self.xeql.pack()
            self.y__xzero_t.pack()
            self.y__xeql_t.pack()
        elif type_task == "Вторая краевая задача":
            self.xeql.pack()
            self.dydx__xzero_t.pack()
            self.dydx__xeql_t.pack()
        elif type_task == "Третья краевая задача":
            self.xeql.pack()
            self.a__xzero.pack()
            self.b__xzero.pack()
            self.third_boundary_function__xzero.pack()

            self.a__xeql.pack()
            self.b__xeql.pack()
            self.third_boundary_function__xeql.pack()


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
                    "xeql": self.xeql.get(),
                    "y__xzero_t": self.y__xzero_t.get(),
                    "y__xeql_t": self.y__xeql_t.get(),

                    "dydx__xzero_t": self.dydx__xzero_t.get(),
                    "dydx__xeql_t": self.dydx__xeql_t.get(),

                    "a__xzero": self.a__xzero.get(),
                    "b__xzero": self.b__xzero.get(),
                    "third_boundary_function__xzero": self.third_boundary_function__xzero.get(),

                    "a__xeql": self.a__xeql.get(),
                    "b__xeql": self.b__xeql.get(),
                    "third_boundary_function__xeql": self.third_boundary_function__xeql.get(),
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

        if equation.get("dydx__xzero_t") is not None:
            self.dydx__xzero_t.entry_text.set(equation["dydx__xzero_t"])
        if equation.get("dydx__xeql_t") is not None:
            self.dydx__xeql_t.entry_text.set(equation["dydx__xeql_t"])


        if equation.get("a__xzero") is not None:
            self.a__xzero.entry_text.set(equation["a__xzero"])
        if equation.get("b__xzero") is not None:
            self.b__xzero.entry_text.set(equation["b__xzero"])
        if equation.get("third_boundary_function__xzero") is not None:
            self.third_boundary_function__xzero.entry_text.set(equation["third_boundary_function__xzero"])

        if equation.get("a__xeql") is not None:
            self.a__xeql.entry_text.set(equation["a__xeql"])
        if equation.get("b__xeql") is not None:
            self.b__xeql.entry_text.set(equation["b__xeql"])
        if equation.get("third_boundary_function__xeql") is not None:
            self.third_boundary_function__xeql.entry_text.set(equation["third_boundary_function__xeql"])

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


class GuiPlot(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller
        self.time = DisplayedTime(controller, 0, 0.05)

        self.frame_for_writer_plot = tk.Frame(self)
        self.frame_for_writer_plot.pack(side = tk.TOP)
        self.writer_plot = WriterPlot(self.frame_for_writer_plot, controller, self.time, LimBorder())
        self.writer_plot.pack(side = tk.TOP)

        self.button = tk.Button(self, text="Пауза/Продолжить", command=(lambda: self.writer_plot.pause_continue()))
        self.button.pack(side = tk.TOP)

        def foo(time):
            # time_to_index
            # self.writer_plot.change_animation_index(index)
            self.time.change_time(float(time))

        self.scale = tk.Scale(
                               self,
                               command=foo,
                               orient=tk.HORIZONTAL,
                               resolution=1,
                               from_=0,
                               to=100
                               )
        self.scale.pack(side = tk.LEFT)

        self.finish_time = LabelEntry(self, kwargs_label={"text": "Окончательное время"})
        self.finish_time.entry_text.set(100)
        self.finish_time.pack(side = tk.LEFT)

        self.view_time = ViewTime(self, controller, self.time)
        self.view_time.pack(side = tk.RIGHT)

        def change_finish_time(finish_time):
            finish_time = float(finish_time)
            self.scale.to = finish_time # not working
            self.controller.change_finish_time(finish_time)

        self.button_change_finish_time = tk.Button(self, text="Применить", command=(lambda: change_finish_time(self.finish_time.get())))
        self.button_change_finish_time.pack(side = tk.BOTTOM)


    def change_to(self, text):
        self.scale.to = float(text)


class ViewTime(tk.Frame):
    def __init__(self, parent, controller, time):
        Frame.__init__(self, parent)

        self.text = tk.Label(self, text=" t = ")
        self.text.config(font=("Courier", 20))
        self.text.pack(side = tk.LEFT)
        self.time = tk.Label(self, textvariable=time.view_t)
        self.time.config(font=("Courier", 20))
        self.time.pack(side = tk.RIGHT)


class MenuChooseSaved(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Выбрать сохраненный график")
        self.label.pack()

        self.controller = controller

        self.listbox = tk.Listbox(self)
        self.listbox.pack()

        names = controller.get_names_saved_equations()

        for name in names:
            self.listbox.insert(tk.END, name)

        self.button_insert = tk.Button(self, text="Подставить", command=(lambda: controller.insert_equation(self.listbox.get("active"))))
        self.button_insert.pack()

        def foo():
            toplevel = tk.Toplevel()
            toplevel.focus_set()
            warn_label = tk.Label(toplevel, text="Вы уверены, что хотите удалить запись?")
            warn_label.pack()

            def bar():
                toplevel.destroy()
                self.controller.delete_equation(self.listbox.get("active"))

            button_ok = tk.Button(toplevel, text="Да", command=(lambda: bar()))
            button_ok.pack()

        self.button_delete = tk.Button(self, text="Удалить", command=(lambda: foo()))
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

