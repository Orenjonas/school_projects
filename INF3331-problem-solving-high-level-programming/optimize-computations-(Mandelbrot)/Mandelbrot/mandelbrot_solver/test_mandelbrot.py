import os, sys

# If module not installed and tests are run with a test framework
# path to testfile needs to be added to python's path:
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath)


import mandelbrot as mb
import numpy as np

def test_compute_outside_mandelbrot():
    n = 10
    computed = mb.compute_mandelbrot(3, 4, 3, 4, n, n)
    expected = np.zeros((n,n))+1  # It always iterates once
    assert np.array_equal(computed, expected), \
    'Computing square outside the mandelbrot set.\n Computed: {} \nExpected {}'.format(computed, expected)

def test_compute_inside_mandelbrot():
    n = 10
    computed = mb.compute_mandelbrot(-0.5, 0.2, -0.2, 0.2, n, n)
    expected = np.zeros((n,n))+1000
    assert np.array_equal(computed, expected), \
    'Computing square inside the mandelbrot set.\n Computed: {} \nExpected {}'.format(computed, expected)


