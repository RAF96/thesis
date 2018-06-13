import sympy.parsing.sympy_parser

def input_to_sympy(*args):
    return [sympy.parsing.sympy_parser.parse_expr(func) for func in args]
