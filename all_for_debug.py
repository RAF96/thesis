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
