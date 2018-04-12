import sys

import numpy
import matplotlib
import scipy
import sympy
import sympy.parsing.sympy_parser
import sympy.abc

from writer_plot import WriterPlot
from all_for_debug import debug_function_print_result, debug_input_file
from reader import read_function, read_coef, read_type_function


def one_dimensional__wave_equtation__homogeneous(coef, y__x_tzero, dydt__x_tzero):
    x, t = sympy.symbols('x t')
    return (y__x_tzero.subs(x, x - coef * t) + y__x_tzero.subs(x, x + coef * t)) / sympy.Rational(2) + \
           sympy.Rational(0.5 / coef) * sympy.integrate(dydt__x_tzero, (x, x - coef * t, x + coef * t))


def one_dimensional__wave_equtation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, func):
    x, t, T = sympy.symbols('x t T')
    func.subs(t, T)
    return one_dimensional__wave_equtation__homogeneous(coef, y__x_tzero, dydt__x_tzero) + \
           sympy.Rational(0.5 / coef) * \
           sympy.integrate(sympy.integrate(func, (x, x - coef * (t - T), x + coef * (t + T))), (T, 0, t))
           

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


def main():
    possible_option = { 
        "homogeneous": main_one_dimensional__wave_equtation__homogeneous, 
        "inhomogeneous": main_one_dimensional__wave_equtation__inhomogeneous,
    }
    type_function = read_type_function()
    possible_option[type_function]()


if __name__ == "__main__":
    main()
