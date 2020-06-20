from python.linearCode import LinearCode
import python.utils as utils


def syndrome_decoding_analysis(linear_code, bit_error):
    syndrome_table = linear_code.get_syndrome_table()
    decoding_error_count = 0
    decoding_rejection_count = 0
    
    for codeword in linear_code.codewords:
        error = linear_code.get_error_vector(bit_error)
        received = (codeword + error) % linear_code.q
        syndrome = linear_code.get_syndrome(received)
        syndrome_str = utils.vector_to_str(syndrome)
        if syndrome_str in syndrome_table:
            error_pattern = syndrome_table[syndrome_str]
            decoded = (received + error_pattern) % linear_code.q
            if (decoded != codeword).any():
                decoding_error_count += 1
        else:  # Синдрома нет в таблице - отказ от декодирования
            decoding_rejection_count += 1
    return decoding_error_count, decoding_rejection_count


lc = LinearCode(15, 5, 2)
lc.print_params()

errors, rejections = syndrome_decoding_analysis(lc, 0.3)
print("Errors:", errors)
print("Rejections:", rejections)
