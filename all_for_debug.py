import sys

def debug_input_file(func):
    def wrapper():
        sys.stdin = open("input.txt", "r")
        res = func()
        return res

    return wrapper

def debug_function_print_result(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(res)
        return res
    return wrapper


@debug_input_file
def use_input_txt():
    from library_equation import gui_main_one_dimensional__equation
    args = sys.stdin.read().splitlines()
    return gui_main_one_dimensional__equation(*args)
