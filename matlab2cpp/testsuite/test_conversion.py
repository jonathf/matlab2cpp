import matlab2cpp
import tempfile
import os
import shutil
from subprocess import Popen, PIPE


def setup_module(module):

    path = tempfile.mkdtemp()
    os.chdir(path)
    module.path = path

def teardown_module(module):

    shutil.rmtree(module.path)


def test_suggestion_cpp():

    os.chdir(path)

    m_code = """
a = 1
b = 2.
c = '3'
d = [4, 5]
    """

    f = open("test.m", "w")
    f.write(m_code)
    f.close()

    os.system("mconvert test.m -rs > /dev/null")

    f = open("test.m.cpp", "r")
    converted_code = f.read()
    f.close()

    reference_code = """
    """

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
