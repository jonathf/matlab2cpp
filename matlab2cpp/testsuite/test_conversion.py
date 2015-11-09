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


def test_variable_sugges():
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
  int a ;
  double b ;
  irowvec d ;
  string c ;
  ivec e ;
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
  ivec b, z ;
  irowvec a, y ;
  int _a [] = {1, 2, 3} ;
  a = irowvec(_a, 3, false) ;
  int _b [] = {4, 5, 6} ;
  b = ivec(_b, 3, false) ;
  f(a, b, y, z) ;
}"""

    assert converted_code == reference_code






def convert(m_code):
    "Convert m-code to cpp-code using matlab2cpp w/suggestions"
    filename = tempfile.mkstemp(suffix=".m", text=True)[1]
    with open(filename, "w") as f:
        f.write(m_code)

    out = Popen(["mconvert", filename], stdout=PIPE).communicate()[0]

    out = str(matlab2cpp.main(filename, True))
    os.remove(filename)
    return out


def _test_get_node():

    m_code = """x(:)
x(1:2:3)
x(1:2:3, :)
x(:, 1:2:3)
x(1:2:3, 4)
x(4, 1:2:3)
x(1,1)"""

    cpp_code = ""

    assert cpp_code == convert(m_code)


def _test_array_indexing():

    m_code = """x(:) = 1:2:3
x(1:2:3) = 1:2:3
x(1:2:3, :) = 1:2:3
x(:, 1:2:3) = 1:2:3
x(1:2:3, 4) = 1:2:3
x(4, 1:2:3) = 1:2:3
x(1,1) = 1:2:3

x(:) = 4
x(1:2:3) = 4
x(1:2:3, :) = 4
x(:, 1:2:3) = 4
x(1:2:3, 4) = 4
x(4, 1:2:3) = 4
x(1,1) = 4"""

    cpp_code = ""

    assert cpp_code == convert(m_code)


def _test_matrix_declaration():

    m_code = """min([1,2;3,4])
x = [1,2]
y = [3;4]
[1, x, x]
[[3, 4]; x]
[[1; 2], y]
[1; y]"""

    cpp_code = ""

    assert cpp_code == convert(m_code)


def _test_implicit_matrix():

    m_code = """min([1 2
3 4])
x = [1 2]
y = [3
4]
[1 x x]
[[3 4]
x]
[[1
2] y]
[1
y]
[1+2]
[1+ 2]
[1 +2]
[1 + 2]
[a() b()
c()]"""

    cpp_code = ""

    assert cpp_code == convert(m_code)


def _test_implicit_transposed():

    m_code = """a'
a.'
a.b'
a()'
a'+'a'+a'
'string' + a'"""

    cpp_code = ""

    assert cpp_code == convert(m_code)



if __name__ == "__main__":
    os.system("py.test")
