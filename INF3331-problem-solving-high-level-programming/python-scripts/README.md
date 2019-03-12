# wc.py
Prints the number of lines, words and characters in a file

## Usage:
```bash
$ python3 wc.py [input file]
```

## Examples:

**One argument:**
```bash
>>> python3 wc.py wc.py

file:  wc.py
-----------
lines: 53
words: 123
chars: 1152
```

**Two arguments:**

```bash
>>> python3 wc.py wc.py wc.py

file:  wc.py
-----------
lines: 53
words: 123
chars: 1152


file:  wc.py
-----------
lines: 53
words: 123
chars: 1152
```

# complex.py
Create complex object and perform arithmetic:

## Examples:
```pytohn
>>>z = Complex(2, -1)
>>> print(z)
(2-1i)
>>> print(z + z)
(4-2i)
>>> print(z - z)
(0+0i)
>>> print(z * z)
(3-4i)
>>> print(z.modulus())
2.23606797749979
>>> print(z.conjugate())
(2+1i)
```

## Running tests:
Using the pytest framework:

```bash
$ pytest
================================== test session starts ==================================
platform linux -- Python 3.6.5, pytest-3.8.0, py-1.6.0, pluggy-0.7.1
rootdir: /home/jonas/UiO/INF3331-jonasore/assignment3, inifile:
collected 10 items

test_complex.py ..........                                                        [100%]

=============================== 10 passed in 0.10 seconds ===============================
```
