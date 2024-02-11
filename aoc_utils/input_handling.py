def read_lines_from_file(path: str, func = None) -> list:
    """Read the specified file and return a list of lines in the file.
    If func is specified, apply it to each line of the file"""
    with open(path, 'r') as file:
        if func is None: return file.read().splitlines()
        else: return list(map(func, file.read().splitlines()))

def read_from_file(path: str, func = None):
    """Read the contents of a file and return the results.
    If func is specified, apply it to the contents of the file"""
    with open(path, 'r') as file:
        if func is None: return file.read()
        else: return func(file.read())