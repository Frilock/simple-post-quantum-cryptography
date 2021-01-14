import time
import numpy as np
import python.utils as utils


def syndrome_decoding_analysis(lin_code, bit_error_array):
    syndrome_table = lin_code.get_syndrome_table()
    errors = []
    rejections = []
    time_array = []

    for bit_error in bit_error_array:
        start_time = time.time()
        error_count = 0
        rejection_count = 0
    
        for codeword in lin_code.codewords:
            error = lin_code.get_error_vector(bit_error)
            received = (codeword + error) % lin_code.q
            syndrome = lin_code.get_syndrome(received)
            syndrome_str = utils.vector_to_str(syndrome)
            if syndrome_str in syndrome_table:
                error_pattern = syndrome_table[syndrome_str]
                decoded = (received + error_pattern) % lin_code.q
                if not np.array_equal(decoded, codeword):
                    error_count += 1
            else:  # Синдрома нет в таблице - отказ от декодирования
                rejection_count += 1
        end_time = time.time()

        time_array.append(end_time - start_time)
        errors.append(error_count)
        rejections.append(rejection_count)

        print("Elapsed:", end_time - start_time,
              ", Bit error:", bit_error,
              ", decoded:", len(lin_code.codewords) - error_count - rejection_count,
              ", count errors:", error_count,
              ", rejection counts:", rejection_count)

    return time_array, errors, rejections
