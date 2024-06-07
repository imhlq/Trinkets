# A Small Library Related to Big Number
# Copyright (c) 2024 xHou

import math

class Decimal():
    base = None
    exponent = None

    def __init__(self, base: str | int | float, exponent=None) -> None:
        if isinstance(base, str) and exponent is None:
            self.base, self.exponent = self.parse_from_string(base)
        elif isinstance(base, (int, float)) and isinstance(exponent, int):
            self.base = float(base)
            self.exponent = exponent
        else:
            raise TypeError("Invalid types for base and exponent")
        self.normalize()

    def normalize(self):
        if self.base >= 10:
            c_exponent =  math.floor(math.log10(abs(self.base)))
            self.base = self.base / (10 ** c_exponent)
            self.exponent += c_exponent
        return self

    def __repr__(self) -> str:
        self.normalize()
        return f"{self.base}e{self.exponent}"
    
    def __mul__(self, other):
        if isinstance(other, Decimal):
            new_base = self.base  * other.base
            new_exponent = self.exponent + other.exponent
            return Decimal(new_base, new_exponent)
        else:
            raise ValueError("Not a Decimal")

    def __add__(self, other):
        if not isinstance(other, Decimal):
            raise ValueError("Addition is only supported between LargeNumber instances")
        # Align exponents for addition
        if self.exponent > other.exponent:
            aligned_base_other = other.base * 10**(self.exponent - other.exponent)
            return Decimal(self.base + aligned_base_other, self.exponent)
        else:
            aligned_base_self = self.base * 10**(self.exponent - other.exponent)
            return Decimal(aligned_base_self + other.base, other.exponent)

    def factorials(self):
        pass