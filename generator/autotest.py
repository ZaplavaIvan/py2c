from os import system, getcwd, chdir
from os.path import join
from prims import Meta
from functools import reduce
import random

MAIN_TEMPLATE = """#{module_name} auto test
import sys

print '{module_name} auto test started...'

{functions_tests}
"""

FUNCTION_TEMPLATE = """
if '{module_name}' in sys.modules:
    del sys.modules['{module_name}']

import sys; sys.path.insert(0, ".."); import {module_name}; sys.path.pop(0)

source_res = {module_name}.{func_name}({args})

del sys.modules['{module_name}']

import {module_name}
extension_res = {module_name}.{func_name}({args})

on_fail = 'failed {{0}} != {{1}}'.format(source_res, extension_res)
print '    {{0:{max_func_name}}} test: {{1}}'.format('{func_name}', ('ok' if source_res == extension_res else on_fail))
"""


def create(out_dir, meta, module_name):
    """
    :type out_dir: str
    :type meta: Meta
    :type module_name
    """

    funcs_data = []
    max_func_name = reduce(lambda a, b: max(a, len(b.name)), meta.funcs, 0)

    for func in meta.funcs:
        values = {
            'int': lambda: random.randint(0, 100),
            'float': lambda: random.random() * 100
        }
        args = ', '.join(map(lambda e: str(values[e[1]]()), func.args))

        func = FUNCTION_TEMPLATE.format(module_name=module_name,
                                        func_name=func.name,
                                        args=args,
                                        max_func_name=max_func_name)
        funcs_data.append(func)

    data = MAIN_TEMPLATE.format(module_name=module_name,
                                functions_tests='\n'.join(funcs_data))

    f = open(join(out_dir, 'autotest.py'), 'w+')
    f.write(data)
    f.close()


def exec_test(out_dir):
    cwd_backup = getcwd()
    chdir(out_dir)

    system("python autotest.py")

    chdir(cwd_backup)