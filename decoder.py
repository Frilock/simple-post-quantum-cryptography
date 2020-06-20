import numpy as np
from linearCode import LinearCode

# реализации методов декодера , подумать о входящих параметрах и прочих ограничениях

def syndrome_decoding_analysis(lc, bit_error):
    syndrome_table = lc.get_syndrome_table()
    decoding_error_count = 0
    decoding_rejection_count = 0
    
    for codeword in lc.codewords:
        error = lc.get_error_vector(bit_error)
        received = (codeword + error) % lc.q
        syndrome = lc.get_syndrome(received)
        syndrome_str = lc.vector_to_str(syndrome)
        if syndrome_str in syndrome_table:
            error_pattern = syndrome_table[syndrome_str]
            decoded = (received + error_pattern) % lc.q
            if (decoded != codeword).any():
                decoding_error_count += 1
        else:
            # Синдрома нет в таблице - отказ от декодирования
            decoding_rejection_count += 1
    return decoding_error_count, decoding_rejection_count
    
lc = LinearCode(15, 5, 2)
lc.print_params()

errors, rejections = syndrome_decoding_analysis(lc, 0.3)
print("Errors:", errors)
print("Rejections:", rejections)
