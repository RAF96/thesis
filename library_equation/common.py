import sympy
from sympy import abc
import numpy

def calculate(function):
    return sympy.lambdify((abc.x, abc.t), function) # , modules=["math", "mpmath", "sympy", {"Integral": integral_as_quad}])

def integral_as_quad(expr, lims):
    var, a, b = lims
    return scipy.integrate.quad(lambdify(var, expr), a, b)[0]
