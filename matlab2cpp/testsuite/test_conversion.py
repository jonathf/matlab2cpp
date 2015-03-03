import matlab2cpp

def test_get_node(tmpdir):

    m_code = """x(:)
x(1:2:3)
x(1:2:3, :)
x(:, 1:2:3)
x(1:2:3, 4)
x(4, 1:2:3)
x(1,1)"""

    cpp_code = ""

    filename = tmpdir.join("tmp.m").strpath
    with open(filename, "w") as f:
        f.write(m_code)

    cpp_code_compare = str(matlab2cpp.main(filename, True))
    assert cpp_code == cpp_code_compare
