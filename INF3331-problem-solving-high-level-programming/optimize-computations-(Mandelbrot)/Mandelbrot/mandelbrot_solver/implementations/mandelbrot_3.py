import numpy as np
from numba import jit
import mandelbrot as mbs


@jit(nopython=True)
def num_of_iterations(z, c, max_escape_time=1000):
    """ Iterates over the differential equation z_n = z_(n-1)**2 + c until
    abs(z_n) >= 2 or i = max_escape_time

    The Mandelbrot set is the set of all c for
    which this sequence does not tend towards infinity.

    Args:
        z (complex): the initial z_0 value
        c (complex): constant number in the equation.

    Returns:
        i (int): number of iterations
    """
    i = 0
    z_size = abs(z)
    while (i < max_escape_time) and (z_size < 2):
        zp = z
        z = z**2 + c
        i += 1
        z_size = abs(z)
    return i

@jit(nopython=True)
def calculate(x_min=-1.7,  x_max=0.7, y_min=-1.2, y_max=1.2, Nx=300, Ny=300, max_escape_time=1000):
    """ Creates an (Nx x Ny) matrix for plotting the madelbrot set.  

    Numba implementation
        
    Args:
        x_min, x_max, y_min, y_max (float):
            The square of real and complex values to compute mandelbrot set over

        Nx, Ny (int):
            Number of points along x (real) and y (imag) axis to compute

        max_escape_time (int):
            Number of iterations before we consider c inside the mandelbrot set

    Returns:
        im (np.array(dtype=float)):
            The elements of the matrix are either:
                * the number of iterations before the absolute value of difference
                  equation z_n = z_(n-1)**2 + c is larger than 2
                * max_escape_time if abs(z_n) has not passed 2 after (max_escape_time) iterations.
            shape: (Nx, Ny)
    """
    x = np.linspace(x_min, x_max, Ny)
    y = np.linspace(y_min, y_max, Nx)

    z_0 = 0+0j
    im = np.zeros((Nx,Ny))

    for i in range(Nx):
        for j in range(Ny):
            c = complex(x[j], y[i])
            im[i,j] = num_of_iterations(z_0, c, max_escape_time)
    return im

if __name__ == '__main__':
    im = calculate()
    mbs.plot(im, outfile='mandelbrot.png')
