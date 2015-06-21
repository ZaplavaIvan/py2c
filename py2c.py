import sys
import os
import imp
from os.path import join, dirname, basename, splitext, split

from generator import pyparser, generator, pycompiler, wrapper, benchmark, autotest, meta
from optparse import OptionParser

if len(sys.argv) == 1:
    sys.argv.extend(['-m', r'tests\test2.py', '-c', r'tests\test2_context.py'])

opt = OptionParser()
opt.add_option("-m", "--module", dest="module")
opt.add_option('-c', "--context", dest="context")
opt.add_option('', "--pyd", action="store_true", dest="pyd", default=False, help="generate pyd module wrapper")
opt.add_option('', "--build", action="store_true", dest="build", default=False)
opt.add_option('', "--autotest", action="store_true", dest="autotest", default=False)
opt.add_option('', "--benchmark", action="store_true", dest="benchmark", default=False)

(options, args) = opt.parse_args()

module_name, ext = splitext(basename(options.module))
abs_module_path = join(os.getcwd(), options.module)
out_dir = join(dirname(abs_module_path), module_name)


def register_ext_types(context_path):
    directory, module_name = split(context_path)
    sys.path.append(directory)
    mod = imp.load_source(splitext(module_name)[0], options.context)
    if hasattr(mod, 'register_types'):
        ext_types = getattr(mod, 'register_types')()
        for t in ext_types:
            type_name, type_def = t
            type_decl = meta.Type(*type_def)
            meta.register_type(type_name, type_decl)


if not os.path.exists(out_dir):
    os.makedirs(out_dir)

if options.context:
    register_ext_types(options.context)

mod, tree, meta = pyparser.parse(abs_module_path)
ctx, src_file = generator.generate_write(tree, meta, out_dir, module_name)

if options.pyd:
    wrapper_file = wrapper.wrap_write(meta, out_dir)

    if options.build:
        pycompiler.write_setup(module_name, [src_file, wrapper_file], out_dir)
        pycompiler.exec_setup(module_name, out_dir)

if options.autotest:
    print ''

    autotest.create(out_dir, meta, module_name)
    autotest.exec_test(out_dir)

if options.benchmark:
    print ''

    benchmark.create(out_dir, meta, module_name)
    benchmark.exec_benchmark(out_dir)
