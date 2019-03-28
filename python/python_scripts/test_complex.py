import math as m
from complex import *


def test_add():
    """
    Test addition for Complex with Complex, complex, int and float
    """
    z = Complex(1, -2)
    w = Complex(1, 1)
    assert (z + w)      == Complex(2, -1)
    assert (z + (1+1j)) == Complex(2, -1)
    assert (z + 2)      == Complex(3, -2)
    assert (z + 2.0)    == Complex(3, -2)

def test_sub():
    """
    Test subtraction for Complex with Complex, complex, int and float
    """
    z = Complex(1, -2)
    w = Complex(1, 1)
    assert (z - w)      == Complex(0, -3)
    assert (z - (1+1j)) == Complex(0, -3)
    assert (z - 2)      == Complex(-1, -2)
    assert (z - 2.0)    == Complex(-1, -2)

def test_conjugate():
    z = Complex(1, -2)
    assert z.conjugate() == Complex(1, 2)

def test_modulus():
    a = 1
    b = -2
    z = Complex(a, b)
    assert z.modulus() == m.sqrt(a + b**2)

def test_string():
    z = Complex(1, -2)
    assert str(z) == "(1-2i)"

def test_mul():
    """
    (1-2i)*(2+2i) = 2 + 2i - 4i + 4
                  = 6 - 2i
    """
    z = Complex(1, -2)
    v = Complex(2, 2)
    assert z*v      == Complex(6, -2)
    assert v*z      == z*v
    assert z*2      == Complex(2, -4)
    assert z*2.0    == Complex(2, -4)
    assert z*(2+2j) == v*z

def test_radd():
    z = Complex(1, -2)
    w = Complex(1, 1)
    assert ((1+1j) + z) == Complex(2, -1)
    assert (2 + z)      == Complex(3, -2)
    assert (2.0 + z)    == Complex(3, -2)

def test_rsub():
    z = Complex(1, -2)
    w = Complex(1, 1)
    assert ((1+1j) - z) == Complex(0, 3)
    assert (2 - z)      == Complex(1, 2)
    assert (2.0 - z)    == Complex(1, 2)

def test_rmul():
    z = Complex(1, -2)
    v = Complex(2, 2)
    assert 2*z      == Complex(2, -4)
    assert 2.0*z    == Complex(2, -4)
    assert (2+2j)*z == z*v

def test_eq():
    z = Complex(1, -2)
    w = Complex(0, 1)
    assert ( z == z and not z == w )
