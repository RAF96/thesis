from library_equation.wave_equation import gui_main_one_dimensional__wave_equation__task_0, \
                          gui_main_one_dimensional__wave_equation__task_1, \
                          gui_main_one_dimensional__wave_equation__task_2, \
                          gui_main_one_dimensional__wave_equation__task_3
from library_equation.heat_equation import gui_main_one_dimensional__heat_equation__task_0, \
                          gui_main_one_dimensional__heat_equation__task_1, \
                          gui_main_one_dimensional__heat_equation__task_2, \
                          gui_main_one_dimensional__heat_equation__task_3


def gui_main_one_dimensional__equation(animation_plot, input_data):
    possible_option = {
        "волновое уравнение": gui_main_one_dimensional__wave_equation,
        "уравнение теплопроводности": gui_main_one_dimensional__heat_equation,
    }
    type_equation = input_data["supporting_data"]["type_equation"]
    return possible_option[type_equation](animation_plot, input_data)


def gui_main_one_dimensional__wave_equation(animation_plot, input_data):
    possible_option = {
        "Задача Коши": gui_main_one_dimensional__wave_equation__task_0,
        "Первая краевая задача": gui_main_one_dimensional__wave_equation__task_1,
        "Вторая краевая задача": gui_main_one_dimensional__wave_equation__task_2,
        "Третья краевая задача": gui_main_one_dimensional__wave_equation__task_3,
    }
    type_task = input_data["supporting_data"]["type_task"]
    return possible_option[type_task](animation_plot, input_data)


def gui_main_one_dimensional__heat_equation(animation_plot, input_data):
    possible_option = {
        "Задача Коши": gui_main_one_dimensional__heat_equation__task_0,
        "Первая краевая задача": gui_main_one_dimensional__heat_equation__task_1,
        "Вторая краевая задача": gui_main_one_dimensional__heat_equation__task_2,
        "Третья краевая задача": gui_main_one_dimensional__heat_equation__task_3,
    }
    type_task = input_data["supporting_data"]["type_task"]
    return possible_option[type_task](animation_plot, input_data)






















