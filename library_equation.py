import sys
import math
import numpy
import matplotlib
import scipy
import scipy.integrate
import sympy
import sympy.parsing.sympy_parser
from sympy import abc

from writer_plot import WriterPlot
from all_for_debug import debug_function_print_result, debug_input_file
from reader import input_to_sympy


def one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero):
    sqrt_coef = coef ** 0.5
    x, t = sympy.symbols('x t')
    return (y__x_tzero.subs(x, x - sqrt_coef * t) + y__x_tzero.subs(x, x + sqrt_coef * t)) / sympy.Rational(2) + \
           sympy.Rational(0.5 / sqrt_coef) * sympy.integrate(dydt__x_tzero, (x, x - sqrt_coef * t, x + sqrt_coef * t))


def one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences):
    sqrt_coef = coef ** 0.5
    x, t, T = sympy.symbols('x t T')
    function_for_integral = external_influences.subs(t, T)
    return one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero) + \
           sympy.Rational(0.5 / sqrt_coef) * \
           sympy.integrate(sympy.integrate(function_for_integral, (x, x - sqrt_coef * (t - T), x + sqrt_coef * (t - T))), (T, 0, t))


def gui_main_one_dimensional__equation(type_equation, coef, y__x_tzero, dydt__x_tzero, external_influences):
    possible_option = {
        "волновое уравнение": gui_main_one_dimensional__wave_equation,
        "уравнение теплопроводности": gui_main_one_dimensional__heat,
    }
    possible_args = {
        "волновое уравнение": (coef, y__x_tzero, dydt__x_tzero, external_influences),
        "уравнение теплопроводности": (coef, y__x_tzero, external_influences),
    }
    return possible_option[type_equation](*possible_args[type_equation])


def gui_main_one_dimensional__wave_equation(coef, y__x_tzero, dydt__x_tzero, external_influences):
    if external_influences:
        return gui_main_one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences)
    else:
        return gui_main_one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero)


def gui_main_one_dimensional__heat(coef, y__x_tzero, external_influences):
    if external_influences:
        return  gui_main_one_dimensional__heat__inhomogeneous(coef, y__x_tzero, external_influences)
    else:
        return gui_main_one_dimensional__heat__homogeneous(coef, y__x_tzero)

def calculate(function):
    return sympy.lambdify((abc.x, abc.t), function)


def gui_main_one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero):
    coef, y__x_tzero, dydt__x_tzero = input_to_sympy(coef, y__x_tzero, dydt__x_tzero)
    return calculate(one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero))


def gui_main_one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences):
    coef, y__x_tzero, dydt__x_tzero, external_influences = input_to_sympy(coef, y__x_tzero, dydt__x_tzero, external_influences)
    return calculate(one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences))


def gui_main_one_dimensional__heat__homogeneous(coef, y__x_tzero):
    coef, y__x_tzero = input_to_sympy(coef, y__x_tzero)
    return calculate(one_dimensional__heat__homogeneous(coef, y__x_tzero))


def gui_main_one_dimensional__heat__inhomogeneous(coef, y__x_tzero, external_influences):
    coef, y__x_tzero, external_influences = input_to_sympy(coef, y__x_tzero, external_influences)
    return calculate__one_dimensional__heat__inhomogeneous(coef, y__x_tzero, external_influences)


def one_dimensional__heat__homogeneous(coef, y__x_tzero):
    sqrt_coef = coef ** 0.5
    x, L = sympy.symbols('x L')
    t = sympy.Symbol('t', positive=True)
    function_for_integral = y__x_tzero.subs(x, L)
    first_multiplier = 1 / (2 * sqrt_coef * (sympy.pi * t) ** 0.5)
    test_f = function_for_integral * sympy.exp(-(x - L) ** 2 / (4 * coef * t))
    res = first_multiplier * sympy.integrate(test_f, (L, -sympy.oo, sympy.oo))
    res = sympy.simplify(res)
    res = res.subs(t, sympy.abc.t)
    return res


def calculate__one_dimensional__heat__inhomogeneous(coef, y__x_tzero, external_influences):
    first_augend = one_dimensional__heat__homogeneous(coef, y__x_tzero)
    lambdify_first_augend = sympy.lambdify((abc.x, abc.t), first_augend)

    def function(x_val, t_val):
        x, L = sympy.symbols("x L")
        t, S = sympy.symbols("t S")
        sqrt_coef = coef ** 0.5
        new_external_influences = external_influences.subs([(x, L), (abc.t, S)])
        function_for_integral = 1 / (2 * sqrt_coef * (sympy.pi * (t - S)) ** 0.5) * \
                                new_external_influences * \
                                sympy.exp(-(x - L) ** 2 / (4 * coef * (t - S)))


        lambdify_function_for_integral = sympy.lambdify((S, L, t, x), function_for_integral)

        second_augend, err = scipy.integrate.dblquad(lambdify_function_for_integral,
                                                     -numpy.inf, numpy.inf,
                                                     lambda S: 0, lambda S: t_val,
                                                     args=(t_val, x_val),
                                                     epsabs=0.000001, epsrel=0.000001)
        return second_augend + lambdify_first_augend(x_val, t_val)

    res = numpy.vectorize(function)
    return res
