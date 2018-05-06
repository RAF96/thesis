import sys

import numpy
import matplotlib
import scipy
import sympy
import sympy.parsing.sympy_parser
import sympy.abc

from writer_plot import WriterPlot
from all_for_debug import debug_function_print_result, debug_input_file
from reader import read_function, read_coef, read_type_function, input_to_sympy


def one_dimensional__wave_equtation__homogeneous(coef, y__x_tzero, dydt__x_tzero):
    sqrt_coef = coef ** 0.5
    x, t = sympy.symbols('x t')
    return (y__x_tzero.subs(x, x - sqrt_coef * t) + y__x_tzero.subs(x, x + sqrt_coef * t)) / sympy.Rational(2) + \
           sympy.Rational(0.5 / sqrt_coef) * sympy.integrate(dydt__x_tzero, (x, x - sqrt_coef * t, x + sqrt_coef * t))


def one_dimensional__wave_equtation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences):
    sqrt_coef = coef ** 0.5
    x, t, T = sympy.symbols('x t T')
    function_for_integral = external_influences.subs(t, T)
    return one_dimensional__wave_equtation__homogeneous(coef, y__x_tzero, dydt__x_tzero) + \
           sympy.Rational(0.5 / sqrt_coef) * \
           sympy.integrate(sympy.integrate(function_for_integral, (x, x - sqrt_coef * (t - T), x + sqrt_coef * (t - T))), (T, 0, t))
           

def gui_main_one_dimensional__wave_equtation(type_equation, coef, y__x_tzero, dydt__x_tzero, external_influences):
    possible_option = { 
        "homogeneous": gui_main_one_dimensional__wave_equtation__homogeneous, 
        "inhomogeneous": gui_main_one_dimensional__wave_equtation__inhomogeneous,
    }
    possible_args = {
        "homogeneous": (coef, y__x_tzero, dydt__x_tzero), 
        "inhomogeneous": (coef, y__x_tzero, dydt__x_tzero, external_influences),
    }
    return possible_option[type_equation](*possible_args[type_equation])


def gui_main_one_dimensional__wave_equtation__homogeneous(coef, y__x_tzero, dydt__x_tzero):
    coef, y__x_tzero, dydt__x_tzero = input_to_sympy(coef, y__x_tzero, dydt__x_tzero)
    return one_dimensional__wave_equtation__homogeneous(coef, y__x_tzero, dydt__x_tzero)


def gui_main_one_dimensional__wave_equtation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences):
    coef, y__x_tzero, dydt__x_tzero, external_influences = input_to_sympy(coef, y__x_tzero, dydt__x_tzero, external_influences)
    return one_dimensional__wave_equtation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences)

