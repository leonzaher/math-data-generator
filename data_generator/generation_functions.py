import numpy as np
import math


def function(functions: list):
    return np.random.choice(a=functions)


def number(len: int):
    """
    Generate number whose string representation is of length size. In other words, following stands:
       len(str(num)) == size
    """
    return np.random.randint(
        int(math.pow(10, len - 1)),
        int(math.pow(10, len) - 1))


def variable(variables: list):
    return np.random.choice(a=variables)
