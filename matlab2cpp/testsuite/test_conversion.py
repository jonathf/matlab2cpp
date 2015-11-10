import matlab2cpp
import tempfile
import os
import shutil
from subprocess import Popen, PIPE


def setup_module(module):
    """Create temporary folder and save path to module before start
    """

    path = tempfile.mkdtemp()
    os.chdir(path)
    module.path = path

def teardown_module(module):
    """Remove temporary folder after job is complete
    """

    shutil.rmtree(module.path)


def test_variable_suggest():
    """Test basic variable types
    """

    # change to temporary dir
    os.chdir(path)

    m_code = """
a = 1
b = 2.
c = '3'
d = [4, 5]
e = [6; 7]
    """

    f = open("test.m", "w")
    f.write(m_code)
    f.close()

    os.system("mconvert test.m -rs > /dev/null")

    f = open("test.m.cpp", "r")
    converted_code = f.read()
    f.close()

    # strip header
    converted_code = "\n\n".join(converted_code.split("\n\n")[1:])

    reference_code = """int main(int argc, char** argv)
{
  double b ;
  int a ;
  irowvec d ;
  ivec e ;
  string c ;
  a = 1 ;
  b = 2. ;
  c = "3" ;
  int _d [] = {4, 5} ;
  d = irowvec(_d, 2, false) ;
  int _e [] = {6, 7} ;
  e = ivec(_e, 2, false) ;
  return 0 ;
}"""

    assert converted_code == reference_code



def test_function_suggestion():
    """Test suggestion for function with single return
    """

    # change to temporary dir
    os.chdir(path)

    m_code = """
function y=f(x)
    y = x+2
end
function g()
    x = [1,2,3]
    y = f(x)
end
    """

    f = open("test.m", "w")
    f.write(m_code)
    f.close()

    os.system("mconvert test.m -rs > /dev/null")

    f = open("test.m.hpp", "r")
    converted_code = f.read()
    f.close()

    # strip header
    converted_code = "\n\n".join(converted_code.split("\n\n")[1:])

    reference_code = """irowvec f(irowvec x)
{
  irowvec y ;
  y = x+2 ;
  return y ;
}

void g()
{
  irowvec x, y ;
  int _x [] = {1, 2, 3} ;
  x = irowvec(_x, 3, false) ;
  y = f(x) ;
}"""

    assert converted_code == reference_code



def test_functions_suggestion():
    """Test suggestion for function with multiple returns
    """

    # change to temporary dir
    os.chdir(path)

    m_code = """
function [y,z]=f(a,b)
    y = a+2
    z = b-3
end
function g()
    a = [1,2,3]
    b = [4;5;6]
    [y,z] = f(a,b)
end
    """

    f = open("test.m", "w")
    f.write(m_code)
    f.close()

    os.system("mconvert test.m -rs > /dev/null")

    f = open("test.m.hpp", "r")
    converted_code = f.read()
    f.close()

    # strip header
    converted_code = "\n\n".join(converted_code.split("\n\n")[1:])

    reference_code = """void f(irowvec a, ivec b, irowvec& y, ivec& z)
{
  y = a+2 ;
  z = b-3 ;
}

void g()
{
  irowvec a, y ;
  ivec b, z ;
  int _a [] = {1, 2, 3} ;
  a = irowvec(_a, 3, false) ;
  int _b [] = {4, 5, 6} ;
  b = ivec(_b, 3, false) ;
  f(a, b, y, z) ;
}"""

    assert converted_code == reference_code



def _test_cross_files():
    """Test suggestion for function with multiple returns
    """

    # change to temporary dir
    os.chdir(path)

    x = """
    """
    f = open("x.m", "w")
    f.write(x)
    f.close()

    y = """
    """
    f = open("x.m", "w")
    f.write(x)
    f.close()

    z = """
    """
    f = open("x.m", "w")
    f.write(x)
    f.close()

    test = """
a = x(4)
b = y(a)
c = z(b)
    """
    f = open("test.m", "w")
    f.write(m_code)
    f.close()

    os.system("mconvert test.m -rs > /dev/null")

    f = open("test.m.hpp", "r")
    converted_code = f.read()
    f.close()

    # strip header
    converted_code = "\n\n".join(converted_code.split("\n\n")[1:])

    reference_code = """void f(irowvec a, ivec b, irowvec& y, ivec& z)
{
  y = a+2 ;
  z = b-3 ;
}

void g()
{
  irowvec a, y ;
  ivec b, z ;
  int _a [] = {1, 2, 3} ;
  a = irowvec(_a, 3, false) ;
  int _b [] = {4, 5, 6} ;
  b = ivec(_b, 3, false) ;
  f(a, b, y, z) ;
}"""

    assert converted_code == reference_code


if __name__ == "__main__":
    os.system("py.test --tb short")
