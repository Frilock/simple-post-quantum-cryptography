import numpy as np
import itertools
import random
from collections import Counter


class LinearCode(object):
    def __init__(self, n, k, q):
        # todo: проверки на размерность поля
        self.k = k  # длина сообщения
        self.n = n  # длина кодового слова
        self.q = q  # размер поля
        matrix_a = np.random.randint(self.q, size=(self.k, self.n - self.k))
        self.G = self.get_generator_matrix(matrix_a)
        self.H = self.get_check_matrix(matrix_a)
        self.codewords = self.get_all_codewords()
        self.d = self.get_min_distance() # Минимальное расстояние
        self.t = int((self.d - 1) / 2) # Корректирующая способность

    def get_spectrum(self):
        weights = Counter()
        for message in itertools.product(list(range(0, self.q)), repeat=self.k):
            weight = self.get_weight(self.get_codeword(message))
            weights[weight] += 1
        return weights

    def get_error_vector(self, bit_error):
        error_vector = np.zeros(self.n, dtype=int)
        for i in range(len(error_vector)):
            if random.random() < bit_error:
                error_vector[i] = 1
        return error_vector
    
    def get_generator_matrix(self, matrix_a):
        identity_matrix = np.eye(self.k, dtype=int)
        return np.hstack((identity_matrix, matrix_a))

    def get_check_matrix(self, matrix_a):
        identity_matrix = np.eye(self.n - self.k, dtype=int)
        return np.hstack((matrix_a.T, identity_matrix))

    def get_codeword(self, message):
        return (message @ self.G) % self.q  # c = i * G

    def get_all_codewords(self):
        codewords = []
        for message in itertools.product(list(range(0, self.q)), repeat=self.k):
            codewords.append(self.get_codeword(message))
        return codewords
    
    def get_syndrome(self, vector):
        return (vector @ self.H.T) % self.q
    
    def get_syndrome_table(self):
        size = 2 ** (self.n - self.k)
        syndrome_table = {}
        iteration_counter = 0
        weight_counter = -1
        for i in range(0, 2 ** self.n):
            error_pattern = self.int_to_vector(i, self.n)
            if self.get_weight(error_pattern) <= self.t:
                syndrome = self.get_syndrome(error_pattern)
                syndrome_str = self.vector_to_str(syndrome)
                syndrome_table[syndrome_str] = error_pattern
        return syndrome_table

    def get_min_distance(self):
        min_distance = self.n
        for codeword in self.codewords:
            codeword_weight = self.get_weight(codeword)
            if codeword_weight < min_distance and codeword_weight != 0:
                min_distance = codeword_weight
        return min_distance

    def get_random_message(self):
        return np.random.randint(self.q, size=self.k)

    def print_params(self):
        print("Field size:", self.q)
        print("Length codeword:", self.n)
        print("Length message:", self.k)
        print("Minimum distance:", self.d)
        print("Correction ability", self.t)

    @staticmethod
    def get_weight(codeword):
        return np.count_nonzero(codeword)
    
    # todo: move this utils methods to other class
    def vector_to_str(self, vector):
        res = ''
        for v in vector:
            res += str(int(v))
        return res
    
    def int_to_vector(self, value, len):
        s = np.binary_repr(value, width=len)
        return np.fromstring(s, 'u1') - ord('0')