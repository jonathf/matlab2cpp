"""
The module contains the following submodules.
"""

from .frontend import Node
import matlab2cpp as mc

__all__ = ["Node"]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
