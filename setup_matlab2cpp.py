from distutils.core import setup

setup(
    name='matlab2cpp',
    version='0.1',
    packages=['matlab2cpp', 'matlab2cpp.targets',
              'matlab2cpp.testsuite', 'matlab2cpp.snippets'],
    package_dir={'': 'src'},
    url='http://github.com/jonathf/matlab2cpp',
    license='BSD',
    author="Jonathan Feinberg",
    author_email="jonathan@feinberg.no",
    description='Matlab to C++ converter'
)
