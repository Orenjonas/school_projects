A module for visualizing the Mandelbrot set.

The computations have three different implementations:
- Pure python
- numpy
- numba

The `time_implementation.py` script compares the runtime of the different
implementations.

## Usage:
For usage help:
```bash
    >>> python3 mandelbrot.py -h
```

Paint a low-rez standard image using the numba implementations:
```bash
    >>> python3 mandelbrot.py
```

To paint the `contest_image.jpg` i used the parameters:
```bash
    >>> python3 mandelbrot.py --region -0.10639 -0.10634 0.92313 0.92317 -n 2500 2500 --colors universe
```

Compute the different runtimes:
```bash
    >>> python3 time_implementation.py
```
