from math import floor

# Rounds down the first input argument to the specified decimal digit.
def roundDown(n, d=8):
    d = int('1' + ('0' * d))
    return floor(n * d) / d