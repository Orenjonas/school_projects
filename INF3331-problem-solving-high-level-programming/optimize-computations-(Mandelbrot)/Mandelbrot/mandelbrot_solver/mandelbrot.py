import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


"""
Computes and draws a representation of the Mandelbrot set.

For usage help:
    >>> python3 mandelbrot.py -h

Usage:
    To paint the contest image i used the parameters:
    >>> python3 mandelbrot.py --region -0.10639 -0.10634 0.92313 0.92317 -n 2500 2500 --colors universe
"""




def compute_mandelbrot(xmin, xmax, ymin, ymax, Nx, Ny, max_escape_time=1000, plot_filename=None):
    """ Compute an array of iterations chere the axes correspond to real numbers inside or outside of the mandelbrot set.
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
    import implementations.mandelbrot_3 as mb3

    im = mb3.calculate(xmin, xmax, ymin, ymax, Nx, Ny, max_escape_time=1000)
    if plot_filename:
        plot(im, filename=plot_filename, Nx=Nx, Ny=Ny, x_min=xmin, x_max=xmax, y_min=ymin, y_max=ymax)
    return im

def plot(im, x_min=-1.7,  x_max=0.7, y_min=-1.2, y_max=1.2, Nx=None, Ny=None, outfile=None, colors='blackhole'):
    """ Plot an array of iterations where the axes correspond to real numbers
    inside or outside of the mandelbrot set.
    Args:
        im (np.array(dtype=float)):
            array of iterations that represent mandelbrot plot.

        outfile (string):
            Optional image filename. To store image, write name (and optionally path) of image

        x_min, x_max, y_min, y_max (float):
            Used to set the axis of image

        colors (str):
            Colormap to use for image
            optns.: 'blackhole', 'sun', 'universe'
    """
    cdict_sun = {
        #looks like the sun, most stuff happens around 0 - 30 iterations
        'red':   ((0.000, 0.000, 0.000),
                  (0.005, 0.000, 0.000),
                  (0.030, 1.000, 1.000),
                  (1.000, 1.000, 1.000)),

        'green':  ((0.000, 0.000, 0.000),
                   (0.070, 1.000, 1.000),
                   (1.000, 1.000, 1.000)),

        'blue':   ((0.000, 0.000, 0.000),
                   (0.030, 0.000, 0.000),
                   (1.000, 1.000, 1.000))}

    cdict_black_hole = {
        #  Black center
        'red':     [(0.000, 1.000, 1.000),
                    (0.070, 0.000, 0.000),
                    (1.000, 0.000, 0.000)],

        'green':    ((0.000, 1.000, 1.000),
                     (0.005, 1.000, 1.000),
                     (0.030, 0.000, 0.000),
                     (1.000, 0.000, 0.000)),

        'blue':   ((0.000, 1.000, 1.000),
                   (0.030, 1.000, 1.000),
                   (1.000, 0.000, 0.000))}

    cdict_contest_colors = { 
        # The interesting stuff happens between 0.025 and 1.000
        # Green kicking in at 0.25 cancels out the red
        # The colormap i used for the contest_image
        
        'red':   ((0.000, 0.000, 0.000),
                  (0.010, 0.000, 0.000),
                  (0.018, 0.500, 0.000),
                  (0.90, 1.000, 1.000),
                  (1.000, 1.000, 1.000)),

        'green': ((0.000, 0.000, 0.000),
                  (0.250, 0.000, 0.000),
                  (0.800, 1.000, 1.000),
                  (1.000, 1.000, 1.000)),

        'blue':  ((0.000, 0.000, 0.000),
                  (0.800, 0.000, 0.000),
                  (1.000, 1.000, 1.000))}

    if (colors == 'sun'):
        cdict = cdict_sun
    if (colors == 'blackhole'):
        cdict = cdict_black_hole
    if (colors == 'universe'):
        cdict = cdict_contest_colors

    colmap = LinearSegmentedColormap('Mandelmap', cdict)
    if (Nx == None or Ny == None): (Nx, Ny) = im.shape
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.imshow(im, origin='bottom', extent=(x_min, x_max, y_min, y_max), aspect="equal", cmap=colmap, interpolation='nearest')
    if outfile:
        plt.savefig(outfile, dpi=1000)
    plt.show()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Plot the mandelbrot set over a given square.')
    parser.add_argument( '--region'
                        , type=float
                        , help='Square region to be computed (defaults to show entire Mandelbrot set).'
                        , nargs=4
                        , default=(-1.7,  0.7, -1.2, 1.2)
                        , metavar=('MIN_X', 'MAX_X', 'MIN_Y', 'MAX_Y'))

    parser.add_argument('--outfile', nargs='?'
                        , type=str
                        , help='File to write the image to.')

    parser.add_argument('-n'
                        , type=int
                        , nargs=2
                        , metavar=('Nx', 'Ny')
                        , default=(300, 300)
                        , help='Resolution of image (defaults to 300x300)')

    parser.add_argument('--implementation'
                        , type=str
                        , choices=['python', 'numpy', 'numba']
                        , help='Python implementation for doing the calculations (defaults to numba)'
                        , default='numba')

    parser.add_argument('--colors'
                        , type=str
                        , choices=['sun', 'blackhole', 'universe']
                        , help='Color palette used to paint image'
                        , default='blackhole')

    class C:
        """ Dummy class to create a namespace for the parser """
        pass
    c = C()
    arguments = parser.parse_args(namespace=c)

    Nx = c.n[0]
    Ny = c.n[1]

    xmin = c.region[0]
    xmax = c.region[1]
    ymin = c.region[2]
    ymax = c.region[3]

    from implementations import mandelbrot_1
    from implementations import mandelbrot_2
    from implementations import mandelbrot_3
    if (c.implementation=='python'):
        im = mandelbrot_1.calculate(xmin, xmax, ymin, ymax, Nx, Ny)
    elif (c.implementation=='numpy'):
        im = mandelbrot_2.calculate(xmin, xmax, ymin, ymax, Nx, Ny)
    else:
        im = mandelbrot_3.calculate(xmin, xmax, ymin, ymax, Nx, Ny)

    plot(im, Nx=Nx, Ny=Ny, outfile=c.outfile, x_min=xmin, x_max=xmax, y_min=ymin, y_max=ymax, colors=c.colors)
