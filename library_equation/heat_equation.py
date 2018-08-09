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


def gui_main_one_dimensional__heat_equation__task_0(animation_plot, input_data):
    coef, y__x_tzero, external_influences = input_data.get("coef", "y__x_tzero", "external_influences")
    coef, y__x_tzero, external_influences = input_to_sympy(coef, y__x_tzero, external_influences)
    if external_influences:
        return  gui_main_one_dimensional__heat_equation__inhomogeneous(animation_plot, coef, y__x_tzero, external_influences)
    else:
        return gui_main_one_dimensional__heat_equation__homogeneous(animation_plot, coef, y__x_tzero)

def calculate(function):
    return sympy.lambdify((abc.x, abc.t), function)

def gui_main_one_dimensional__heat_equation__homogeneous(animation_plot, coef, y__x_tzero):
    function = calculate(one_dimensional__heat_equation__homogeneous(coef, y__x_tzero))

    animation_plot.clean_result_part()
    for t in animation_plot.t:
        next_y = function(animation_plot.x, t)
        animation_plot.y.append(next_y)

    return animation_plot


def gui_main_one_dimensional__heat_equation__inhomogeneous(coef, y__x_tzero, external_influences):
    return calculate__one_dimensional__heat_equation__inhomogeneous(coef, y__x_tzero, external_influences)

def one_dimensional__heat_equation__homogeneous(coef, y__x_tzero):
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

#to do. Too slowly and I didn't decide what I need to do. Supporting was stoped. Now not working.
def calculate__one_dimensional__heat_equation__inhomogeneous(coef, y__x_tzero, external_influences):
    first_augend = one_dimensional__heat_equation__homogeneous(coef, y__x_tzero)
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

def gui_main_one_dimensional__heat_equation__task_1(animation_plot, input_data):
    input_data_get = input_data.get("coef", "y__x_tzero", "external_influences", "y__xzero_t", "y__xeql_t")
    args = input_to_sympy(*input_data_get)
    return calculate__one_dimensional__heat_equation__task_1(animation_plot, *args)


def calculate__one_dimensional__heat_equation__task_1(animation_plot, coef, y__x_tzero, external_influences, y__xzero_t, y__xeql_t):
    y__x_tzero = calculate(y__x_tzero)
    external_influences = calculate(external_influences)
    y__xzero_t = calculate(y__xzero_t)
    y__xeql_t = calculate(y__xeql_t)
    sqrt_coef = coef ** 0.5

    def function(x, t, y):
        y_next = None
        n = len(x) - 1
        dx = x[1] - x[0]
        dt = 0.05
        gamma2 = dt * (1. / dx * sqrt_coef) ** 2

        if y is None:
            y = [0] * (n + 1)
            for i in range(0, n+1):
                y[i] = y__x_tzero(x[i], t) + dt * external_influences(x[i], t)
            return y

        y_next = [0] * (n + 1)
        for i in range(1, n):
            y_next[i] = y[i] + \
                             gamma2 * (y[i + 1] - 2 * y[i] + y[i - 1]) + \
                             dt * external_influences(x[i], t)

        y_next[0] = y__xzero_t(x[0], t)
        y_next[n] = y__xeql_t(x[n], t)

        y = y_next
        return y_next

    animation_plot.clean_result_part()
    y = None
    for t in animation_plot.t:
        y = function(animation_plot.x, t, y)
        animation_plot.y.append(y)

    return animation_plot


def gui_main_one_dimensional__heat_equation__task_2(animation_plot, input_data):
    input_data_get = input_data.get("coef", "y__x_tzero", "external_influences", "dydx__xzero_t", "dydx__xeql_t")
    args = input_to_sympy(*input_data_get)
    return calculate__one_dimensional__heat_equation__task_2(animation_plot, *args)


def calculate__one_dimensional__heat_equation__task_2(animation_plot, coef, y__x_tzero, \
        external_influences, dydx__xzero_t, dydx__xeql_t):
    y__x_tzero = calculate(y__x_tzero)
    external_influences = calculate(external_influences)
    dydx__xzero_t = calculate(dydx__xzero_t)
    dydx__xeql_t = calculate(dydx__xeql_t)
    sqrt_coef = coef ** 0.5

    def function(x, t, y):
        y_next = None
        n = len(x) - 1
        dx = x[1] - x[0]
        dt = 0.05
        gamma2 = dt * (1. / dx * sqrt_coef) ** 2

        if y is None:
            y = [0] * (n + 1)
            for i in range(0, n+1):
                y[i] = y__x_tzero(x[i], t) + dt * external_influences(x[i], t)
            return y

        y_next = [0] * (n + 1)
        for i in range(1, n):
            y_next[i] = y[i] + \
                             gamma2 * (y[i + 1] - 2 * y[i] + y[i - 1]) + \
                             dt * external_influences(x[i], t)

        y_next[0] = dydx__xzero_t(x[0], t) * dt + y[0]
        y_next[n] = dydx__xeql_t(x[n], t) * dt + y[n]

        y = y_next
        return y_next

    animation_plot.clean_result_part()
    y = None
    for t in animation_plot.t:
        y = function(animation_plot.x, t, y)
        animation_plot.y.append(y)

    return animation_plot


def gui_main_one_dimensional__heat_equation__task_3(animation_plot, input_data):
    input_data_get = input_data.get("coef", "y__x_tzero", "external_influences", \
            "a__xzero", "b__xzero", "third_boundary_function__xzero", \
            "a__xeql", "b__xeql", "third_boundary_function__xeql")
    args = input_to_sympy(*input_data_get)
    return calculate__one_dimensional__heat_equation__task_3(animation_plot, *args)


def calculate__one_dimensional__heat_equation__task_3(animation_plot, coef, y__x_tzero, external_influences, \
            a__xzero, b__xzero, third_boundary_function__xzero, \
            a__xeql, b__xeql, third_boundary_function__xeql):

    y__x_tzero = calculate(y__x_tzero)
    external_influences = calculate(external_influences)
    third_boundary_function__xzero = calculate(third_boundary_function__xzero)
    third_boundary_function__xeql = calculate(third_boundary_function__xeql)
    sqrt_coef = coef ** 0.5

    def function(x, t, y):
        y_next = None
        n = len(x) - 1
        dx = x[1] - x[0]
        dt = 0.05
        gamma2 = dt * (1. / dx * sqrt_coef) ** 2

        if y is None:
            y = [0] * (n + 1)
            for i in range(0, n+1):
                y[i] = y__x_tzero(x[i], t) + dt * external_influences(x[i], t)
            return y

        y_next = [0] * (n + 1)
        for i in range(1, n):
            y_next[i] = y[i] + \
                             gamma2 * (y[i + 1] - 2 * y[i] + y[i - 1]) + \
                             dt * external_influences(x[i], t)
        y_next[0] = (third_boundary_function__xzero(x[0], t) * dt + y[0]) / \
                (dt * a__xzero + b__xzero)
        y_next[n] = (third_boundary_function__xeql(x[n], t) * dt + y[n]) / (dt * a__xeql + b__xeql)

        y = y_next
        return y_next

    animation_plot.clean_result_part()
    y = None
    for t in animation_plot.t:
        y = function(animation_plot.x, t, y)
        animation_plot.y.append(y)

    return animation_plot


