import numpy as np
from linearCode import LinearCode

# реализации методов декодера , подумать о входящих параметрах и прочих ограничениях

lc = LinearCode(5, 2, 2)
lc.print_params()
syndrome_table = lc.get_syndrome_table()
for k, v in syndrome_table.items():
    print(k, v)
# n = 100 k = 30 2 ** 70 - 1)
