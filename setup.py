"""Main installer."""
from setuptools import setup, find_packages

setup(
    name="matlab2cpp",
    version="2.0.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["m2cpp = matlab2cpp:m2cpp"]},
    url='http://github.com/jonathf/matlab2cpp',
    license='BSD',
    author="Jonathan Feinberg",
    author_email="jonathan@feinberg.no",
    description="Matlab to C++ transpiler",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Software Development :: Compilers',
    ],
    tests_require=["pytest", "pytest-runner"],
)
