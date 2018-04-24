from reader import read_function, read_coef, read_type_function
from main import one_dimensional__wave_equtation__homogeneous, \
    one_dimensional__wave_equtation__inhomogeneous
from writer_plot import WriterPlot
from all_for_debug import *


def main_one_dimensional__wave_equtation__homogeneous():
    variables = ('x', )
    y__x_tzero = read_function(variables, "function with t = 0")
    dydt__x_tzero = read_function(variables, "derivative of the function with t = 0")
    coef = read_coef()
    res = one_dimensional__wave_equtation__homogeneous(coef, y__x_tzero, dydt__x_tzero)
    writer_plot = WriterPlot(res)
    writer_plot.print_animation()


def main_one_dimensional__wave_equtation__inhomogeneous():
    variables = ('x', )
    y__x_tzero = read_function(variables, "function with t = 0")
    dydt__x_tzero = read_function(variables, "derivative of the function with t = 0")
    coef = read_coef()
    external_influences = read_function(variables + ('t', ), "function of external influences")
    res = one_dimensional__wave_equtation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences)
    writer_plot = WriterPlot(res)
    writer_plot.print_animation()


@debug_input_file
def main():
    possible_option = { 
        "homogeneous": main_one_dimensional__wave_equtation__homogeneous, 
        "inhomogeneous": main_one_dimensional__wave_equtation__inhomogeneous,
    }
    type_function = read_type_function()
    possible_option[type_function]()


if __name__ == "__main__":
    main()
