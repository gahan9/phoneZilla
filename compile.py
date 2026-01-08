from setuptools import setup, Extension
# Note: Cython might still need build_ext, but distutils.core is gone.
# Using Cython's build_ext if available.
try:
    from Cython.Distutils import build_ext
except ImportError:
    from setuptools.command.build_ext import build_ext


ext_modules = [
    Extension("mymodule1",  ["mymodule1.py"]),
    Extension("mymodule2",  ["mymodule2.py"]),

#   ... all your modules that need be compiled ...

]

setup(
    name = 'My Program Name',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)