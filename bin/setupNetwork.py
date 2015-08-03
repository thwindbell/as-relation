from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'Network class',
    ext_modules = cythonize("Network.pyx"),
)
