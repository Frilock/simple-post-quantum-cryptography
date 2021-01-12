import numpy as np
import time
import itertools
import python.utils as utils
import matplotlib.pyplot as plot
from python.linearCode import LinearCode


'''
1. Составить множество информационных совокупностей
Инф. совокупность (y) - множество (массив) из уникальных
возрастающих элементов в диапазоне от 0 до n - 1 длины k.
Например, [0, 1, 2, 3]. При этом G(y) должна быть несингулярной.
2. 
'''


def information_set_decoding(lin_code):
    information_sets = get_all_information_sets(lin_code.n, lin_code.k, lin_code.G)
    H_gamma_array = []
    for inf_set in information_sets:
        inf_set_h = get_information_set_h(inf_set, lin_code.n)
        Hi = utils.matrix_from_columns(lin_code.H, inf_set_h)
        Hi_inv = utils.inverse_matrix(Hi)
        H_gamma = (Hi_inv @ lin_code.H) % lin_code.q
        H_gamma_array.append(H_gamma)

    error_count_array = []
    rejection_count_array = []
    bit_error_array = np.arange(0.0, 1.1, 0.1)
    for bit_error in bit_error_array:
        start_time = time.time_ns()
        rejection_count = 0
        error_count = 0
        print("Number of codewords", len(lin_code.codewords))
        for codeword in lin_code.codewords:
            error_vector = lin_code.get_error_vector(bit_error)
            received_message = (error_vector + codeword) % 2
            counter = 0
            for i, inf_set in enumerate(information_sets):
                H_gamma = H_gamma_array[i]
                syndrome = (received_message @ H_gamma.T) % lin_code.q
                if LinearCode.get_weight(syndrome) <= lin_code.t:
                    Gi = utils.matrix_from_columns(lin_code.G, inf_set)
                    Gi_inv = utils.inverse_matrix(Gi)
                    G_gamma = (Gi_inv @ lin_code.G) % lin_code.q
                    bi = np.zeros(lin_code.k, dtype=int)
                    for i, value in enumerate(inf_set):
                        bi[i] = received_message[value]
                    decoded = (bi @ G_gamma) % lin_code.q

                    if not np.array_equal(codeword, decoded):
                        error_count += 1
                    break
                counter += 1
            if counter == len(information_sets):
                rejection_count += 1
        end_time = time.time_ns()
        print("Elapsed: ", end_time - start_time)
        error_count_array.append(error_count)
        rejection_count_array.append(rejection_count)
        print("Bit error:", bit_error,
              "decoded: ", len(lin_code.codewords) - error_count - rejection_count,
              "count errors:", error_count,
              ", rejection counts:", rejection_count)
    plot.figure()
    plot.xlabel('bit error')
    plot.ylabel('count error')
    plot.plot(bit_error_array, error_count_array, color='pink', label='count error')
    plot.plot(bit_error_array, rejection_count_array, color='green', label='rejection error')
    plot.legend()
    plot.show()

def get_all_information_sets(n, k, matrix_g):
    information_sets = []
    candidates = itertools.combinations(list(range(0, n)), k)
    for candidate in candidates:
        Gi = utils.matrix_from_columns(matrix_g, list(candidate))
        try:
            Gi_inv = utils.inverse_matrix(Gi)
        except RuntimeError:
            continue
        information_sets.append(list(candidate))
    return information_sets


def get_information_set_h(information_set_g, n):
    inf_set_h = []
    for i in range(0, n):
        if i not in information_set_g:
            inf_set_h.append(i)
    return inf_set_h


linear_code = LinearCode(15, 8, 2)

linear_code.print_params()
information_set_decoding(linear_code)
