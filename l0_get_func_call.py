import re, os


# Read built-in function names.

def read_lines(path):
    with open(os.path.join('stuff', path)) as f:
        text = f.read()
    return text.splitlines()

std_funcs = read_lines('python_std/python_funcs.txt')
built_in_methods = read_lines('python_std/python_methods.txt')
std_funcs += built_in_methods
std_modules = read_lines('python_std/py_std_lib.txt')


# def get_func_call(line, imported_module_names):
def get_func_call(line):
    # Given a line of code, pull out a function call.
    # eg. "get_func_call('foo')"

    words = line.split()
    for iword, word in enumerate(words):
        if('(' not in word or
           (iword > 0 and words[iword - 1] == 'def')):
            continue
        match = re.match('([a-zA-Z0-9_\.\:]+)\(', word)
        if not match:
            continue
        word = match.group(1)
        full_word = word
        # (don't want std lib funcs in graph)
        if '.' in word:
            called_on, word = word.rsplit('.', 1)
            if(called_on in std_funcs or called_on in std_modules or
               word in std_funcs):
                continue
            # if called_on not in imported_module_names:
            #     continue
        if word in ('if', 'for') or ':' in word:
            continue
        if word.startswith('test_'):
            continue
        if word in std_funcs:
            continue
        return full_word


if __name__ == '__main__':
    with open('l1_file_to_dot.py') as f:
        text = f.read()
    func_names = []
    imported_module_names = set(['l0_get_func_call'])
    for line in text.splitlines():
        # func_name = get_func_call(line, imported_module_names)
        func_name = get_func_call(line)
        if(func_name):
            func_names.append(func_name)
        print '{:<20} | {:<100}'.format(func_name[:20] if func_name else func_name, line)
    print func_names
