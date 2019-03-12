import timeit

def time_implementation(implementation, n, Nx, Ny,\
                        xmin=-1.7,  xmax=0.7, ymin=-1.2, ymax=1.2, maxescapetime=1000):
    """ Computes the runtime of different implementations of mandelbrot_solver.

    Args:
        implementation (str):
            What implementation to use: 'mandelbrot_1', 'mandelbrot_2' or 'mandelbrot_3'

        n (int):
            Number og times timeit.repeat() runs the implementation.

        Nx, Ny (int):
            Nymber of points along x and y axis to compute with implementation

        x_min,  x_max, y_min, y_max (int):
           What square to compute, standard covers the entire mandelbrot set

        max_escape_time (int):
            See docstring for the calculate() method.

    Returns:
        Runtime (str):
            Output from the timeit module
    """
    time = timeit.repeat(stmt='%s.calculate(x_min=%f, x_max=%f, y_min=%f, y_max=%f, Nx=%d, Ny=%d)' % \
                         (implementation, xmin, xmax, ymin, ymax, Nx, Ny),\
                         setup='from implementations import %s' % implementation,\
                         number=n, repeat=4) #, repeat=4)
    return time

if __name__=='__main__':
    time_pure_py = time_implementation('mandelbrot_1', n=3, Nx=500, Ny=500)
    time_numpy   = time_implementation('mandelbrot_2', n=3, Nx=500, Ny=500)
    time_numba   = time_implementation('mandelbrot_3', n=3, Nx=500, Ny=500)

    min_py = min(time_pure_py)
    min_np = min(time_numpy)
    min_nb = min(time_numba)

    print("pure python:                 ", (min_py))
    print()
    print("numpy vectorized:            ", (min_np))
    print("python/numpy implementation: ", (min_py/min_np))
    print()
    print("numba optimized:             ", (min_nb))
    print("python/numba implementation: ", (min_py/min_nb))

"""
Scriptet mandelbrot_solver/time/calc_runtime.py bruker timeit modulen til å
teste tiden på implementasjonene.  Hver implementasjon kjøres 3 ganger, med
Nx=500
Ny=500 
xmin=-1.7
xmax=0.7
ymin=-1.2
ymax=1.2
max_escape_time=1000.

pure python:                  59.07586499399986 

numpy vectorized:             14.243524458000138
python/numpy implementation:  4.14755948699332  

numba optimized:              2.6734792590000325
python/numba implementation:  22.09699768387062
"""
