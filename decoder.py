import numpy as np
from linearCode import LinearCode

# реализации методов декодера , подумать о входящих параметрах и прочих ограничениях

lc = LinearCode(5, 2, 2)
for c in lc.codewords:
    print(c)

lc.print_params()