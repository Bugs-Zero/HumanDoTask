# Sample file with intentional lint issues for testing

def badly_formatted_function(x,y,z):
    result=x+y+z   # Missing spaces around operators
    return  result  # Extra spaces

class poorlyNamedClass:  # Class name should be CamelCase
    def __init__(self):
        unused_variable = 42  # F841: local variable assigned but never used
        pass

def function_with_long_line():
    # E501: Line too long
    really_long_string = "This is a really really really really really really really really really really long line that exceeds the recommended length"
    return really_long_string

import os  # E402: Module level import not at top of file

def unused_function():  # This function is never called
    pass

# Missing newline at end of file