from python.linearCode import LinearCode
import numpy as np
import matplotlib.pyplot as plot


def minimum_distance_decoder(linear_code):
    error_bit_array = np.arange(0.0, 1.1, 0.1)
    array_count_error = []

    for error_bit in error_bit_array:
        count_error = 0
        rejection_count = 0

        codewords = linear_code.codewords
        for codeword in codewords:
            result_codeword = []
            hamming_distance = 100  # инициализируем заведомо большим числом
            error_vector = linear_code.get_error_vector(error_bit)
            # if linear_code.get_weight(error_vector) > linear_code.t:  # сравниваем с корректирующей способностью
            #     rejection_count += 1
            #     continue
            received_message = (error_vector + codeword) % 2
            for any_codeword in codewords:
                temp_hamming_distance = get_hamming_distance(received_message, any_codeword)
                if temp_hamming_distance < hamming_distance:
                    hamming_distance = temp_hamming_distance
                    result_codeword = any_codeword
            if not np.array_equal(codeword, result_codeword):  # сравниваем слова
                count_error += 1
                continue
        array_count_error.append(count_error)
        print("Bit error:", error_bit, "decoded: ", len(codewords) - count_error - rejection_count,
              "count errors:", count_error, ", rejection counts:", rejection_count)

    plot.figure()
    plot.xlabel('bit error')
    plot.ylabel('count error')
    plot.plot(error_bit_array, array_count_error, color='pink', label='count error')
    plot.legend()
    plot.show()


def get_hamming_distance(codeword, any_codeword):
    return np.sum(codeword != any_codeword)


linear_code = LinearCode(30, 10, 2)
minimum_distance_decoder(linear_code)
