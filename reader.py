import sympy.parsing.sympy_parser

def input_to_sympy(*args):
    return (sympy.parsing.sympy_parser.parse_expr(func) for func in args)

def read_function(variables, description = None):
    if description is not None:
        print(description)
    print("write function with variables: ", variables)
    func = input()
    res = sympy.parsing.sympy_parser.parse_expr(func)
    return res


def read_coef():
    print("write coef: ")
    return int(input())


def read_type_function():
    print("write_type_function: ")
    return input()
