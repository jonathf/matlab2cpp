from distutils.core import setup
import matlab2cpp as package

setup(
    name='matlab2cpp',
    version=package.__version__,
    packages=['matlab2cpp', 'matlab2cpp/targets',
              'matlab2cpp/testsuite', 'matlab2cpp/snippets'],
    url='http://github.com/jonathf/matlab2cpp',
    license='BSD',
    author=package.__author__,
    description='Matlab to C++ converter'
)
