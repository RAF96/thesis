import sympy
from sympy import abc

def calculate(function):
    return sympy.lambdify((abc.x, abc.t), function)
