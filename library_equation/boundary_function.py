from library_equation.common import calculate


def get_first_boundary_function(y__x_t):
    y__x_t = calculate(y__x_t)
    def foo(x, t, dt, y):
        return y__x_t(x, t)
    return foo

def get_second_boundary_function(dydx__x_t):
    dydx__x_t = calculate(dydx__x_t)
    def foo(x, t, dt, y):
        return dydx__x_t(x, t) * dt + y
    return foo

def get_third_boundary_function(a__x, b__x, third_boundary_function__x):
    third_boundary_function__x = calculate(third_boundary_function__x)
    def foo(x, t, dt, y):
        return (third_boundary_function__x(x, t) * dt + y) / \
                (dt * a__x + b__x)
    return foo
