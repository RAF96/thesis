#!/usr/bin/python3

import sys
from controller import Controller
from all_for_debug import use_input_txt

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("use_input_txt return: ", use_input_txt())
    else:
        controller = Controller()
