from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'AS class',
    ext_modules = cythonize("AS.pyx"),
)
