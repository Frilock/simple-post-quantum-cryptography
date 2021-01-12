import numpy as np
import itertools
import python.utils as utils
import matplotlib.pyplot as plot
import time
from python.linearCode import LinearCode


def decoder(lin_code):
    start = time.time_ns()
    print("Hello world")
    #time.sleep(2)
    for i in range(0, 10):
        time.sleep(1)
    end = time.time_ns()
    elapsed = end - start
    print("Elapsed", elapsed)


linear_code = LinearCode(15, 8, 2)
linear_code.print_params()
decoder(linear_code)
