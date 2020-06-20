import numpy as np


def vector_to_str(vector):
    result = ''
    for v in vector:
        result += str(int(v))
    return result


def int_to_vector(value, length):
    s = np.binary_repr(value, width=length)
    return np.fromstring(s, 'u1') - ord('0')
