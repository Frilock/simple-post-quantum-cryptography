from python.linearCode import LinearCode
import time
import numpy as np
import matplotlib.pyplot as plot
import python.utils as utils


def syndrome_decoding_analysis(lin_code):
    syndrome_table = lin_code.get_syndrome_table()
    bit_errors = np.arange(0, 1.1, 0.1)
    errors = []
    rejections = []
    time_array = []

    for bit_error in bit_errors:
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

        print("Elapsed: ", end_time - start_time)
        print("Bit error:", bit_error, "decoded: ", len(lin_code.codewords) - error_count - rejection_count,
              "count errors:", error_count, ", rejection counts:", rejection_count)

    plot.figure()
    plot.xlabel('bit error')
    plot.ylabel('errors amount')
    plot.plot(bit_errors, errors, label='errors')
    plot.plot(bit_errors, rejections, label='rejections')
    plot.legend()
    plot.show()

    return time_array, errors, rejections
