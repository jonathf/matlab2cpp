"""Test fx_decon script."""
import os


def test_fx_decon():
    """Test fx_decon script."""
    os.system("m2cpp fx_decon.m -s > /dev/null")
    with open("fx_decon.cpp", "r") as src:
        reference_code = src.read().strip()
    with open("fx_decon.m.hpp", "r") as src:
        converted_code = "\n".join(src.read().split("\n")[2:]).strip()
    assert converted_code == reference_code
