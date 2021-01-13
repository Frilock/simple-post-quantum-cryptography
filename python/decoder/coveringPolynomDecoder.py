import numpy as np
import time
import matplotlib.pyplot as plot
from python.linearCode import LinearCode
import python.utils as utils


def polynomial_decoder(lin_code):
    information_sets = utils.get_all_information_sets(lin_code.n, lin_code.k, lin_code.G)
    H_gamma_array = []

    for inf_set in information_sets:
        inf_set_h = utils.get_information_set_h(inf_set, lin_code.n)
        Hi = utils.matrix_from_columns(lin_code.H, inf_set_h)
        Hi_inv = utils.inverse_matrix(Hi)
        H_gamma = (Hi_inv @ lin_code.H) % lin_code.q
        H_gamma_array.append(H_gamma)

    time_array = []
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
            decoded_flag = False
            for i, inf_set in enumerate(information_sets):
                H_gamma = H_gamma_array[i]
                for k in range(0, len(inf_set) + 1):
                    theta = np.zeros(lin_code.n, dtype=int)
                    if k != 0:
                        theta[inf_set[k - 1]] = 1

                    received_message_theta = (received_message + theta) % lin_code.q
                    syndrome = (received_message_theta @ H_gamma.T) % lin_code.q
                    if LinearCode.get_weight(syndrome) <= lin_code.t - LinearCode.get_weight(theta):
                        decoded_flag = True
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
                if decoded_flag:
                    break
            if not decoded_flag:
                rejection_count += 1
        end_time = time.time_ns()

        time_array.append(end_time - start_time)
        error_count_array.append(error_count)
        rejection_count_array.append(rejection_count)

        print("Elapsed:", end_time - start_time,
              "Bit error:", bit_error,
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


linear_code = LinearCode(30, 10, 2)
linear_code.print_params()
polynomial_decoder(linear_code)
