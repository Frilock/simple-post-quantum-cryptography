import numpy as np
import matplotlib.pyplot as plt
from linearCode import LinearCode

# реализации методов декодера , подумать о входящих параметрах и прочих ограничениях

def syndrome_decoding_analysis(lc):
    syndrome_table = lc.get_syndrome_table()
    bit_errors = np.arange(0, 1, 0.1)
    errors = []
    rejections = []
    plt.figure()
    plt.xlabel('bit error')
    plt.ylabel('errors amount')

    for bit_error in bit_errors:
        error_count = 0
        rejection_count = 0
    
        for codeword in lc.codewords:
            error = lc.get_error_vector(bit_error)
            received = (codeword + error) % lc.q
            syndrome = lc.get_syndrome(received)
            syndrome_str = lc.vector_to_str(syndrome)
            if syndrome_str in syndrome_table:
                error_pattern = syndrome_table[syndrome_str]
                decoded = (received + error_pattern) % lc.q
                if not np.array_equal(decoded, codeword):
                    error_count += 1
            else:
                # Синдрома нет в таблице - отказ от декодирования
                rejection_count += 1
        errors.append(error_count)
        rejections.append(rejection_count)
    plt.plot(bit_errors, errors, label='errors')
    plt.plot(bit_errors, rejections, label='rejections')
    plt.legend()
    plt.show()



lc = LinearCode(17, 7, 2)
lc.print_params()

syndrome_decoding_analysis(lc)
