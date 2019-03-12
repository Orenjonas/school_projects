import math as m

class Complex:
    """
    Implementation of complex numbers

    Attributes:
        a (int): Real part
        b (int): Imaginary part
    """

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def conjugate(self):
        """Returns the complex conujgate
        Example:
            >>> z = Complex(1, 1)
            >>> z.conjugate()

        Returns:
            Complex object
        """
        return Complex(self.a, -self.b)

    def modulus(self):
        """ Returns the complex modulus
        if x = (a + b*i), modulus computes: sqrt(a^2 + b^2)

        Example:
            >>> x = Complex(a, b)
            >>> x.modulus()

        Returns:
            Complex object
        """
        return m.sqrt(self.a**2 + self.b**2)

    def __add__(self, other):
        """Complex addition

        Args:
            other (int, float, Complex or complex)

        Returns:
            Complex object
        """
        a = self.a
        b = self.b
        if (type(other) == type(self)):
            A = other.a
            B = other.b
        elif (type(other) == complex):
            A = other.real
            B = other.imag
        elif (type(other) == int or type(other) == float):
            A = other
            B = 0
        return Complex(a + A, b + B)

    def __sub__(self, other):
        """Complex subraction
        Executes self + (-other)
        by converting "other" to "-other"

        Args:
            other (int, float, Complex or complex)

        Returns:
            Complex object
        """
        if (type(other) == type(self)):
            other = Complex(-other.a, -other.b)
        else:
            other = -other
        return self+other

    def __mul__(self, other):
        """ Complex multiplication
        (a+bi)*(A+Bi) = (aA - bB) + (aB + bA)i

        Args:
            other (int, float, Complex or complex)

        Returns:
            Complex object
        """
        a = self.a
        b = self.b
        if (type(other) == type(self)):
            A = other.a
            B = other.b
        elif (type(other) == complex):
            A = other.real
            B = other.imag
        else:
            A = other
            B = 0
        return Complex((a*A - b*B) , (a*B + b*A))

    def __eq__(self, other):
        """Test complex objects for equality

        Args:
            other (Complex): object to be tested for equality to this

        Returns:
            bool: True if real and imaginary parts both are equal,
                  False otherwise
        """
        if (self.a == other.a and self.b == other.b):
            return True
        else:
            return False

    # Assignment 3.4
    def __radd__(self, other):
        """ Right addition same as normal addition

        Args:
            other (int, float, Complex or complex)

        Returns:
            Complex object
        """
        return self + other

    def __rsub__(self, other):
        """ Right subtraction, using that (other - self) = (-self + other)

        Args:
            other (int, float, Complex or complex)

        Returns:
            Complex object
        """
        return -self + other

    def __rmul__(self, other):
        """ Right multiplication using commutativity

        Args:
            other (int, float, Complex or complex)

        Returns:
            Complex object
        """
        return self * other

    def __str__(self):
        """
        Returns:
            String on the form "(a +- bi)
        """
        if (self.b >= 0):
            operator = "+"
        else:
            operator = "-"
        return "({:g}{:s}{:g}i)".format(self.a, operator, abs(self.b))

    def __neg__(self):
        """
        Returns:
            Complex: negated complex, so (a + bi) -> (-a - bi)
        """
        return Complex(-self.a, -self.b)
