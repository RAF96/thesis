import sys
import math
import numpy
import matplotlib
import scipy
import scipy.integrate
import sympy
import sympy.parsing.sympy_parser
from sympy import abc

from all_for_debug import debug_function_print_result, debug_input_file
from reader import input_to_sympy
from view_models import AnimationPlot


def gui_main_one_dimensional__wave_equation__task_0(input_data):
    coef, y__x_tzero, dydt__x_tzero, external_influences = input_data.get("coef", "y__x_tzero", "dydt__x_tzero", "external_influences")
    if external_influences:
        return gui_main_one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences)
    else:
        return gui_main_one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero)


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


def calculate(function):
    return sympy.lambdify((abc.x, abc.t), function)


def gui_main_one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero):
    coef, y__x_tzero, dydt__x_tzero = input_to_sympy(coef, y__x_tzero, dydt__x_tzero)
    function = calculate(one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero))
    animation_plot = AnimationPlot()

    for t in animation_plot.t:
        animation_plot.y.append(function(animation_plot.x, t))

    return animation_plot


def gui_main_one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences):
    coef, y__x_tzero, dydt__x_tzero, external_influences = input_to_sympy(coef, y__x_tzero, dydt__x_tzero, external_influences)
    function = calculate(one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences))

    animation_plot = AnimationPlot()

    for t in animation_plot.t:
        animation_plot.y.append(function(animation_plot.x, t))

    return animation_plot


def gui_main_one_dimensional__wave_equation__task_1(input_data):
    input_data_get = input_data.get("coef", "y__x_tzero", "dydt__x_tzero", "external_influences", "y__xzero_t", "y__xeql_t")
    args = input_to_sympy(*input_data_get)
    return calculate__one_dimensional__wave_equation__task_1(*args)


def calculate__one_dimensional__wave_equation__task_1(coef, y__x_tzero, dydt__x_tzero, external_influences, y__xzero_t, y__xeql_t):
    y__x_tzero = calculate(y__x_tzero)
    dydt__x_tzero = calculate(dydt__x_tzero)
    external_influences = calculate(external_influences)
    y__xzero_t = calculate(y__xzero_t)
    y__xeql_t = calculate(y__xeql_t)
    sqrt_coef = coef ** 0.5

    def function(x, t, y_previous, y):
        n = len(x) - 1
        dx = x[1] - x[0]
        dt = 0.05
        gamma2 = (dt / dx * sqrt_coef) ** 2

        if y is None:
            y = [0] * (n + 1)
            for i in range(0, n+1):
                y[i] = y__x_tzero(x[i], t) + dt ** 2 * external_influences(x[i], t)
            return y

        if y_previous is not None:
            y_next = [0] * (n + 1)
            for i in range(1, n):
                y_next[i] = 2 * y[i] - y_previous[i] + \
                                 gamma2 * (y[i + 1] - 2 * y[i] + y[i - 1]) + \
                                 dt ** 2 * external_influences(x[i], t)
        else:
            y_next = [0] * (n + 1)
            for i in range(1, n):
                y_next[i] = y[i] + \
                                 gamma2 / 2 * (y[i + 1] - 2 * y[i] + y[i - 1]) + \
                                 dt * dydt__x_tzero(x[i], t) + \
                                 dt ** 2 / 2 * external_influences(x[i], t)

        y_next[0] = y__xzero_t(x[i], t)
        y_next[n] = y__xeql_t(x[i], t)

        return y_next

    animation_plot = AnimationPlot()
    y_previous = y = None

    for t in animation_plot.t:
        animation_plot.y.append(function(animation_plot.x, t, y_previous, y))
        y_previous, y = y, animation_plot.y[-1]

    return animation_plot


def gui_main_one_dimensional__wave_equation__task_2(input_data):
    pass


def gui_main_one_dimensional__wave_equation__task_3(input_data):
    pass
