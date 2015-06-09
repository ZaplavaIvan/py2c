from os.path import join
from prims import Meta
import random

MAIN_TEMPLATE = """#{module_name} benchmark
import timeit
import sys

print '{module_name} benchmark started...'

{functions_benchmark}
"""

FUNCTION_TEMPLATE = """
if '{module_name}' in sys.modules:
    del sys.modules['{module_name}']

source_code_setup = 'import sys; sys.path.insert(0, ".."); import {module_name}; sys.path.pop(0)'
source_code_exec_time = timeit.timeit('{module_name}.{func_name}({args})', setup=source_code_setup, number={number})

del sys.modules['{module_name}']

extension_code_setup = 'import {module_name}'
extension_code_exec_time = timeit.timeit('{module_name}.{func_name}({args})', setup=extension_code_setup, number={number})

print "\\n{func_name} timeit results(number={number}):"
print "    python:   {{0}}".format(source_code_exec_time)
print "    c++:      {{0}}".format(extension_code_exec_time)
print "    speed-up: {{0}}%".format(100.0 * (-1.0 + source_code_exec_time / extension_code_exec_time))
"""


def create(out_dir, meta, module_name):
    """
    :type out_dir: str
    :type meta: Meta
    :type module_name
    """

    funcs_data = []

    for func in meta.funcs:
        values = {
            'int': lambda: random.randint(0, 100),
            'float': lambda: random.random() * 100
        }
        number = 10000
        args = ', '.join(map(lambda e: str(values[e[1]]()), func.args))

        func = FUNCTION_TEMPLATE.format(module_name=module_name,
                                        func_name=func.name,
                                        args=args,
                                        number=number)
        funcs_data.append(func)

    data = MAIN_TEMPLATE.format(module_name=module_name,
                                functions_benchmark='\n'.join(funcs_data))

    f = open(join(out_dir, 'benchmark.py'), 'w+')
    f.write(data)
    f.close()