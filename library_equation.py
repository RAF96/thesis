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


def gui_main_one_dimensional__equation(input_data):
    possible_option = {
        "волновое уравнение": gui_main_one_dimensional__wave_equation,
        "уравнение теплопроводности": gui_main_one_dimensional__heat_equation,
    }
    type_equation = input_data["supporting_data"]["type_equation"]
    return possible_option[type_equation](input_data)


def gui_main_one_dimensional__wave_equation(input_data):
    possible_option = {
        "Задача Коши": gui_main_one_dimensional__wave_equation__task_0,
        "Первая краевая задача": gui_main_one_dimensional__wave_equation__task_1,
    }
    type_task = input_data["supporting_data"]["type_task"]
    return possible_option[type_task](input_data)


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


def gui_main_one_dimensional__wave_equation__task_0(input_data):
    coef, y__x_tzero, dydt__x_tzero, external_influences = input_data.get("coef", "y__x_tzero", "dydt__x_tzero", "external_influences")
    if external_influences:
        return gui_main_one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences)
    else:
        return gui_main_one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero)


def gui_main_one_dimensional__heat_equation(input_data):
    coef, y__x_tzero, external_influences = input_data.get("coef", "y__x_tzero", "external_influences")
    coef, y__x_tzero, external_influences = input_to_sympy(coef, y__x_tzero, external_influences)
    if external_influences:
        return  gui_main_one_dimensional__heat_equation__inhomogeneous(coef, y__x_tzero, external_influences)
    else:
        return gui_main_one_dimensional__heat_equation__homogeneous(coef, y__x_tzero)

def calculate(function):
    return sympy.lambdify((abc.x, abc.t), function)


def gui_main_one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero):
    coef, y__x_tzero, dydt__x_tzero = input_to_sympy(coef, y__x_tzero, dydt__x_tzero)
    return calculate(one_dimensional__wave_equation__homogeneous(coef, y__x_tzero, dydt__x_tzero))


def gui_main_one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences):
    coef, y__x_tzero, dydt__x_tzero, external_influences = input_to_sympy(coef, y__x_tzero, dydt__x_tzero, external_influences)
    return calculate(one_dimensional__wave_equation__inhomogeneous(coef, y__x_tzero, dydt__x_tzero, external_influences))


def gui_main_one_dimensional__heat_equation__homogeneous(coef, y__x_tzero):
    return calculate(one_dimensional__heat_equation__homogeneous(coef, y__x_tzero))


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

def gui_main_one_dimensional__wave_equation__task_1(*args):
    args = input_to_sympy(*args)
    l = (*args, 0, 0)
    return calculate__one_dimensional__wave_equation__task_1(*l)

def calculate__one_dimensional__wave_equation__task_1(coef, y__x_tzero, dydt__x_tzero, external_influences, y__xzero_t, y__xeql__t):

    class Task():
        def __init__(self, coef, y__x_tzero, dydt__x_tzero, external_influences, y__xzero_t, y__xeql__t):
            self.coef, self.y__x_tzero, self.dydt__x_tzero, self.external_influences, self.y__xzero_t, self.y__xeql__t = \
            coef, y__x_tzero, dydt__x_tzero, external_influences, y__xzero_t, y__xeql__t
            self.y__x_tzero = calculate(self.y__x_tzero)
            self.dydt__x_tzero = calculate(self.dydt__x_tzero)
            self.external_influences = calculate(self.external_influences)
            self.sqrt_coef = coef ** 0.5
            self.y_previous = self.y = self.y_next = None

        def function(self, x, t):
            n = len(x) - 1
            dx = x[1] - x[0]
            dt = 0.05
            gamma2 = (dt / dx * self.sqrt_coef) ** 2

            if self.y is None:
                self.y = self.y__x_tzero(x, t) + dt ** 2 * self.external_influences(x, t)
                return self.y

            if self.y_previous is not None:
                for i in range(1, n):
                    self.y_next[i] = 2 * self.y[i] - self.y_previous[i] + \
                                     gamma2 * (self.y[i + 1] - 2 * self.y[i] + self.y[i - 1]) + \
                                     dt ** 2 * self.external_influences(x[i], t)

                self.y_next[n] = self.y_next[0] = 0
            else:
                self.y_next = [0] * (n + 1)
                for i in range(1, n):
                    self.y_next[i] = self.y[i] + gamma2 / 2 * (self.y[i + 1] - 2 * self.y[i] + self.y[i - 1])

                self.y_next[n] = self.y_next[0] = 0

            self.y_previous, self.y = self.y, self.y_next
            return self.y_next

    res = Task(coef, y__x_tzero, dydt__x_tzero, external_influences, y__xzero_t, y__xeql__t).function
    return res
