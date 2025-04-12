import sys

def redirect_to_file(function, args, kwargs, filename):
    with open(filename) as out:
        orig_stdout = sys.stdout
        sys.stdout = out
        try:
            function(*args, **kwargs)
        finally:
            sys.stdout = orig_stdout

def modifies_locals_sum(x, y):
    locals()['z'] = x + y
    #z will not be defined as modifications to locals() do not alter the local variables.
    return z

def fixed_sum(x, y):
    z = x + y
    return z
