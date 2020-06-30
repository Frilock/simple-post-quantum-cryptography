from python.linearCode import LinearCode
import numpy as np
import matplotlib.pyplot as plot
import python.utils as utils


def syndrome_decoding_analysis(linear_code):
    syndrome_table = linear_code.get_syndrome_table()
    bit_errors = np.arange(0, 1, 0.1)
    errors = []
    rejections = []

    for bit_error in bit_errors:
        error_count = 0
        rejection_count = 0
    
        for codeword in linear_code.codewords:
            error = linear_code.get_error_vector(bit_error)
            received = (codeword + error) % linear_code.q
            syndrome = linear_code.get_syndrome(received)
            syndrome_str = utils.vector_to_str(syndrome)
            if syndrome_str in syndrome_table:
                error_pattern = syndrome_table[syndrome_str]
                decoded = (received + error_pattern) % linear_code.q
                if not np.array_equal(decoded, codeword):
                    error_count += 1
            else:  # Синдрома нет в таблице - отказ от декодирования
                rejection_count += 1
        errors.append(error_count)
        rejections.append(rejection_count)

        print("Bit error:", bit_error,
              "Decoded:", len(linear_code.codewords) - error_count - rejection_count)

    plot.figure()
    plot.xlabel('bit error')
    plot.ylabel('errors amount')
    plot.plot(bit_errors, errors, label='errors')
    plot.plot(bit_errors, rejections, label='rejections')
    plot.legend()
    plot.show()


linear_code = LinearCode(30, 10, 2)
linear_code.print_params()

syndrome_decoding_analysis(linear_code)
