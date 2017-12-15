from math import floor

def roundDown(n, d=8):
    d = int('1' + ('0' * d))
    return floor(n * d) / d