"""Test simple assignment."""
import pytest

from matlab2cpp import qcpp, qhpp, qtree


@pytest.fixture(params=[
    "simple_assignment",
])
def cpp_filename(request):
    return request.param


def test_cpp_executables(cpp_filename):
    """Test basic variable types."""

    with open("%s.m" % cpp_filename) as src:
        source_code = src.read().strip()
    translation = qcpp(source_code, suggest=True)

    with open("%s.cpp" % cpp_filename) as src:
        cpp_reference = src.read().strip()

    assert translation == cpp_reference


@pytest.fixture(params=[
    "function_reference",
    "function_reference_2",
])
def hpp_filename(request):
    return request.param


def test_hpp_executables(hpp_filename):
    """Test basic variable types."""

    with open("%s.m" % hpp_filename) as src:
        source_code = src.read().strip()
    translation = qhpp(source_code, suggest=True)

    with open("%s.hpp" % hpp_filename) as src:
        hpp_reference = src.read().strip()

    assert translation == hpp_reference
