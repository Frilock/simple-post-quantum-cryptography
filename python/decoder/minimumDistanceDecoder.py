from python.linearCode import LinearCode
import numpy as np
import time
import matplotlib.pyplot as plot
import python.utils as utils


def minimum_distance_decoder(lin_code):
    error_bit_array = np.arange(0.0, 1.1, 0.1)
    errors = []
    rejections = []
    time_array = []

    for error_bit in error_bit_array:
        start_time = time.time()
        count_error = 0
        rejection_count = 0

        codewords = lin_code.codewords
        for codeword in codewords:
            copy_codewords = codewords.copy()
            temp_index = 0
            flag_rejection_error = False
            result_codeword = []
            hamming_distance = 100  # инициализируем заведомо большим числом
            error_vector = lin_code.get_error_vector(error_bit)

            received_message = (error_vector + codeword) % 2  # передали сообщение, начинаем декодирование
            for index, any_codeword in enumerate(codewords):  # ищем минимальное расстояние
                temp_hamming_distance = utils.get_hamming_distance(received_message, any_codeword)
                if temp_hamming_distance < hamming_distance:
                    hamming_distance = temp_hamming_distance
                    result_codeword = any_codeword
                    temp_index = index
            del copy_codewords[temp_index]

            for some_codeword in copy_codewords:  # проверяем существует ли несколько код.слов с мин расстоянием
                if utils.get_hamming_distance(some_codeword, received_message) == hamming_distance:
                    rejection_count += 1
                    flag_rejection_error = True
                    break

            if not np.array_equal(codeword, result_codeword) and not flag_rejection_error:
                # сравниваем слова если не было отказа
                count_error += 1
                continue

        end_time = time.time()

        time_array.append(end_time - start_time)
        errors.append(count_error)
        rejections.append(rejection_count)
        print("Elapsed:", end_time - start_time,
              ", bit error:", error_bit,
              ", decoded:", len(codewords) - count_error - rejection_count,
              ", count errors:", count_error,
              ", rejection counts:", rejection_count)

    plot.figure()
    plot.xlabel('bit error')
    plot.ylabel('count error')
    plot.plot(error_bit_array, errors, color='pink', label='count error')
    plot.plot(error_bit_array, rejections, color='green', label='rejection error')
    plot.legend()
    plot.show()

    return time_array, errors, rejections


linear_code = LinearCode(30, 10, 2)
linear_code.print_params()
minimum_distance_decoder(linear_code)
