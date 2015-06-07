from os import system, getcwd, chdir
from os.path import join

TEMPLATE = """#GENERATED
from distutils.core import setup, Extension

module = Extension("{module_name}", sources=[{files}])
setup(name= "{module_name}", version= '1.0', ext_modules= [module])
"""


def write_setup(module_name, files, out_dir):
    f = open(join(out_dir, 'setup.py'), 'w+')
    files_list = map(lambda e: "'{0}'".format(e), files)
    f.write(TEMPLATE.format(module_name=module_name, files=', '.join(files_list)))
    f.close()


def exec_setup(out_dir):
    cwd_backup =  getcwd()
    chdir(out_dir)
    system('python setup.py build')
    chdir(cwd_backup)