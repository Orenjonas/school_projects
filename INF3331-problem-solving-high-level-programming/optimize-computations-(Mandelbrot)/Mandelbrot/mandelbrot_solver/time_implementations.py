import time_implementations.calc_runtime as cr

"""
Computes the runtime of different implementations (pure python, numpy and numba) of mandelbrot_solver.
"""

if __name__=='__main__':
    time_pure_py = cr.time_implementation('mandelbrot_1', n=3, Nx=50, Ny=50)
    time_numpy   = cr.time_implementation('mandelbrot_2', n=3, Nx=50, Ny=50)
    time_numba   = cr.time_implementation('mandelbrot_3', n=3, Nx=50, Ny=50)

    min_py = min(time_pure_py)
    min_np = min(time_numpy)
    min_nb = min(time_numba)

    # print("pure python:                 ", (min_py))
    # print()
    # print("numpy vectorized:            ", (min_np))
    # print("python/numpy implementation: ", (min_py/min_np))
    # print()
    # print("numba optimized:             ", (min_nb))
    # print("python/numba implementation: ", (min_py/min_nb))

    print(f"pure python:                 {min_py}\n\n" \

           f"numpy vectorized:            {min_np}\n" \
           f"python/numpy implementation: {min_py/min_np}\n\n" \

           f"numba optimized:             {min_nb}\n" \
           f"python/numba implementation: {min_py/min_nb}\n\n" \

          f"Numpy is {min_py/min_np} times faster than pure python.\n" \
          f"Numba is {min_py/min_nb} times faster than pure python.")
