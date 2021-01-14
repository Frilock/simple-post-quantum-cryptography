import matplotlib.pyplot as plot
import numpy as np

from python.linearCode import LinearCode
from python.decoder.syndromeDecoder import syndrome_decoding_analysis
from python.decoder.minimumDistanceDecoder import minimum_distance_decoder
from python.decoder.informationSetDecoder import information_set_decoder
from python.decoder.coveringPolynomDecoder import polynomial_decoder

bit_error_array = np.arange(0.0, 1.1, 0.1)


def create_plot(syndrome, distance, information, polynomial):
    plot.plot(bit_error_array, syndrome, color='pink', label='syndrome')
    plot.plot(bit_error_array, distance, color='green', label='distance')
    plot.plot(bit_error_array, information, color='yellow', label='information')
    plot.plot(bit_error_array, polynomial, color='blue', label='polynomial')
    plot.legend()
    plot.show()


def time_analyse(syndrome, distance, information, polynomial):
    print("Start analyse time")
    plot.figure()
    plot.xlabel('bit error')
    plot.ylabel('time')
    create_plot(syndrome, distance, information, polynomial)


def error_analyse(syndrome, distance, information, polynomial):
    print("Start analyse errors")
    plot.figure()
    plot.xlabel('bit error')
    plot.ylabel('errors')
    create_plot(syndrome, distance, information, polynomial)


def rejection_analyse(syndrome, distance, information, polynomial):
    print("Start analyse rejections")
    plot.figure()
    plot.xlabel('bit error')
    plot.ylabel('rejections')
    create_plot(syndrome, distance, information, polynomial)


linear_code = LinearCode(20, 7, 2)
linear_code.print_params()

print('\n', "Start syndrome decoding")
syndrome_time, syndrome_errors, syndrome_rejections = syndrome_decoding_analysis(linear_code, bit_error_array)

print('\n', "Start minimum distance decoding")
distance_time, distance_errors, distance_rejections = minimum_distance_decoder(linear_code, bit_error_array)

print('\n', "Start information set decoding")
information_time, information_errors, information_rejections = information_set_decoder(linear_code, bit_error_array)

print('\n', "Start polynomial decoding")
polynomial_time, polynomial_errors, polynomial_rejections = polynomial_decoder(linear_code, bit_error_array)

time_analyse(syndrome_time, distance_time, information_time, polynomial_time)
error_analyse(syndrome_errors, distance_errors, information_errors, polynomial_errors)
rejection_analyse(syndrome_rejections, distance_rejections, information_rejections, polynomial_rejections)
