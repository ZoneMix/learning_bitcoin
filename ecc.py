from typing import Type, TypeVar

class FieldElement:
    ## Takes in a number within the range 0..p-1 with p being a prime number
    def __init__(self, num:int, prime:int) -> None:
        if num >= prime or num < 0:
            error = f"Num {num} not in field range 0 to {prime} - 1"
            raise ValueError(error)
        self.num = num
        self.prime = prime

    ## Return the representation of a Field Element
    def __repr__(self) -> str:
        return f"FieldElement_{self.prime}({self.num})"

    ## Overload the equality of two Field Elements
    def __eq__(self, __o: object) -> bool:
        if __o is None:
            return False
        return self.num == __o.num and self.prime == __o.prime

    ## Overload the inequality of two Field Elements
    def __ne__(self, __o: object) -> bool:
        if __o is None:
            return True
        return self.num != __o.num and self.prime != __o.prime

    ## Overload the addition of two Field Elements
    def __add__(self, __o: object) -> object:
        if self.prime != __o.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num + __o.num) % self.prime
        return self.__class__(num, self.prime)

    ## Overload the subtraction of two Field Elements
    def __sub__(self, __o: object) -> object:
        if self.prime != __o.prime:
            raise TypeError('Cannot subtract two numbers in different Fields')
        num = (self.num - __o.num) % self.prime
        return self.__class__(num, self.prime)

    ## Overload the multiplication of two Field Elements
    def __mul__(self, __o: object) -> object:
        if self.prime != __o.prime:
            raise TypeError('Cannot multiply two numbers in different Fields')
        num = (self.num * __o.num) % self.prime
        return self.__class__(num, self.prime)
    
    ## Overload the power of a Field Element
    def __pow__(self, exponent: int) -> object:
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    ## Division following the rules of Fermat's Little Theorem and multiplicative inverse operation
    def __truediv__(self, __o: object) -> object:
        if self.prime != __o.prime:
            raise TypeError('Cannot divide two numbers in different Fields')
        num = self.num * (__o.num ** (self.prime - 2)) % self.prime
        return self.__class__(num, self.prime)


class Point:
    def __init__(self, x, y, a, b) -> None:
        self.a = a
        self.b = b
        self.x = x
        self.y = y

        # Infinity
        if self.x is None and self.y is None:
            return

        # Check if point is valid on the elliptical curve
        if self.y**2 != self.x**3 + a * x + b:
            raise ValueError(f"({x}, {y}) is not on the curve")

    ## Return the representation of a point
    def __repr__(self) -> str:
        if self.x is None:
            return f"Point(infinity)"
        elif not isinstance(self.x, FieldElement):
            return f"Point({self.x}, {self.y})_{self.a}_{self.b}"
        else:
            return f"Point({self.x.num}, {self.y.num})_{self.a.num}_{self.b.num} FieldElement({self.x.prime})"

    ## Overload equality of two points have the same x and y values
    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y \
            and self.a == __o.a and self.b == __o.b

    ## Overload inequality of two points either do not have the same x or y values             
    def __ne__(self, __o: object) -> bool:
        return self.x != __o.x or self.y != __o.y \
            or self.a != __o.a or self.b != __o.b

    ## Point Addition
    def __add__(self, __o: object) -> object:
        if self.a != __o.a or self.b != __o.b:
            raise TypeError(f"({__o.a}, {__o.b}) are not on the same curve")

        # Return the other point if one is infinity
        if self.x is None:
            return __o
        if __o.x is None:
            return self

        # Return infinity point if the x values are the same and y is different
        if self.x == __o.x and self.y != __o.y:
            return self.__class__(None, None, self.a, self.b)

        # Find intersection of third point within the slope of 
        #   two points with different x values and return the
        #   reflected third point
        if self.x != __o.x:
            # Find slope
            m = (__o.y - self.y) / (__o.x - self.x)
            x = (m**2) - self.x - __o.x
            y = m(self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        # If points are the same, but y == 0, then return infinity
        # TODO: Maybe add the self.y == 0 * self.x?
        if self == __o and self.y == 0:
            return self.__class__(None, None, self.a, self.b)

        # If points are the same, use a tangent slope to add two points
        #   then return the reflected third point
        if self == __o:
            m = (3 * (self.x**2) + self.a) / (2 * self.y)
            x = (m**2) - (2 * self.x)
            y = m(self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        
