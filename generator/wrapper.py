from os.path import join
from prims import Meta
from meta import IntT

FUNC_WRAPPER_DECL_TEMPLATE = """{{"{ext_name}", {func_wrapper}, METH_VARARGS, "{doc}"}}"""

FUNC_WRAPPER_TEMPLATE = """
static PyObject *
{func_wrapper_name}(PyObject *self, PyObject *args)
{{
    {func_args_decl}
    if (!PyArg_ParseTuple(args, "{func_args_code}", {func_args_refs})) return NULL;

    {rtype} res = {func_name}({func_args});
    return PyLong_FromSize_t(res);
}}
"""

FUNC_VOID_WRAPPER_TEMPLATE = """

static PyObject *
{func_wrapper_name}(PyObject *self, PyObject *args)
{{
    {func_args_decl}

    if (!PyArg_ParseTuple(args, "{func_args_code}", {func_args_refs})) return NULL;

    {func_name}({func_args});

    Py_RETURN_NONE;
}}

"""

PYD_TEMPLATE = """ //{module_name}
#include <Python.h>

{extern_func_list}

{func_wrappers_list}

static PyMethodDef {module_name}Methods[] = {{
    {funcs_list},
    {{NULL, NULL, 0, NULL}}        /* Sentinel */
}};


PyMODINIT_FUNC
init{module_name}(void)
{{
    (void) Py_InitModule("{module_name}", {module_name}Methods);
}}

int
main(int argc, char *argv[])
{{
}}
"""

parse_code = {
    IntT: 'i',
}


def wrap_write(meta, out_dir):
    """
    :type meta: Meta
    :rtype: str
    """
    main = wrap(meta)
    wrapper_name = meta.module_name + '_pywrap.cpp'
    f = open(join(out_dir, wrapper_name), 'w+')
    f.write(main)
    f.close()

    return wrapper_name


def wrap(meta):
    """
    :type meta: Meta
    """
    func_wrappers_gen = []
    func_decl_gen = []
    extern_funcs = []

    for m in filter(lambda x: x.is_ext, meta.funcs):
        wrapper_name = '{0}_wrapper'.format(m.name)

        if m.rtype is None:
            pass
        else:
            args_decl = '    '.join(map(lambda x: '{0} {1};\n'.format(x[1].cpp_type, x[0]), m.args))
            args_code = ''.join(map(lambda x: parse_code[x[1]], m.args))
            args_refs = ', '.join(map(lambda x: '&{0}'.format(x[0]), m.args))
            args = ', '.join(map(lambda x: x[0], m.args))

            gen = FUNC_WRAPPER_TEMPLATE.format(func_wrapper_name=wrapper_name,
                                               func_args_decl=args_decl,
                                               func_args_code=args_code,
                                               func_args_refs=args_refs,
                                               func_args=args,
                                               func_name=m.name,
                                               rtype=m.rtype.cpp_type)
            func_wrappers_gen.append(gen)

            args_typed = ', '.join(map(lambda x: '{0} {1}'.format(x[1].cpp_type, x[0]), m.args))
            extern = 'extern {rtype} {func_name}({func_args});'.format(rtype=m.rtype.cpp_type,
                                                                       func_name=m.name,
                                                                       func_args=args_typed)
            extern_funcs.append(extern)

        decl_gen = FUNC_WRAPPER_DECL_TEMPLATE.format(ext_name=m.name,
                                                     func_wrapper=wrapper_name,
                                                     doc='')
        func_decl_gen.append(decl_gen)

    main = PYD_TEMPLATE.format(func_wrappers_list=''.join(func_wrappers_gen),
                               funcs_list=',\n    '.join(func_decl_gen),
                               module_name=meta.module_name,
                               extern_func_list='\n'.join(extern_funcs))

    return main


if __name__ == "__main__":
    import pyparser
    import os
    import generator
    from os.path import join
    module, tree = pyparser.parse(join(os.getcwd(), 'simple_class.py'))
    ctx = generator.generate(module, tree)
    pywrap = wrap(ctx)

    f = open(module.__name__ + '.cpp', 'w+')
    f.write(ctx._out)
    f.close()

    w = open(module.__name__ + '_pywrap.cpp', 'w+')
    w.write(pywrap)
    w.close()