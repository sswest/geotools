import glob

from setuptools import setup, Extension

# 从源代码中构建一个扩展模块
geotools_module = Extension(
    'geodev.coord',
    sources=['src/export.c'],
)

ext_modules = [geotools_module, ]

try:
    import numpy

    numpy.array([[121, 23], [31, 43]], ndmin=2, dtype='d')
    vec_module = Extension(
        'geodev.vec',
        sources=['src/export_vec.c'],
        include_dirs=[numpy.get_include()],
    )
    ext_modules.append(vec_module)
except ModuleNotFoundError:
    pass

setup(
    name='geodev',
    version='0.1.0',
    description='Python interface for the geotools C library',
    ext_modules=ext_modules,
    data_files=[('geodev', glob.glob('geodev-python/*.pyi'))],
)
