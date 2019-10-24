from distutils.core import setup, Extension, DEBUG

sfc_module = Extension('reader', sources = ['Main.cpp'])

setup(name = 'reader', version = '1.0',
    description = 'Python Package with .grd-reader functionality',
    )