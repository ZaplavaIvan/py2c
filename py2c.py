import sys
import os
from os.path import join, dirname, basename, splitext

from generator import pyparser, generator, pycompiler, wrapper, benchmark, autotest
from optparse import OptionParser

if len(sys.argv) == 1:
    sys.argv.extend(['-m', r'tests\test1.py', '-p', '-c'])

opt = OptionParser()
opt.add_option("-m", "--module", dest="module")
opt.add_option('-p', "--pyd", action="store_true", dest="pyd", default=False, help="generate pyd module wrapper")
opt.add_option('-c', "--compile", action="store_true", dest="compile", default=False)

(options, args) = opt.parse_args()

module_name, ext = splitext(basename(options.module))
abs_module_path = join(os.getcwd(), options.module)
out_dir = join(dirname(abs_module_path), module_name)

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

mod, tree, meta = pyparser.parse(abs_module_path)
ctx, src_file = generator.generate_write(tree, meta, out_dir, module_name)

if options.pyd:
    wrapper_file = wrapper.wrap_write(meta, out_dir)

    if options.compile:
        pycompiler.write_setup(module_name, [src_file, wrapper_file], out_dir)
        pycompiler.exec_setup(module_name, out_dir)

print ''

autotest.create(out_dir, meta, module_name)
autotest.exec_test(out_dir)

print ''

benchmark.create(out_dir, meta, module_name)
benchmark.exec_benchmark(out_dir)
