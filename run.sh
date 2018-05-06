#!/bin/bash

if [ $# -eq 0 ]
then
    python3 main.py
elif [ $1 = "terminal" ]
then
    python3 terminal_input.py
else
    echo "No exist this parameters"
fi
