import numpy as np
import itertools
from collections import Counter


class LinearCode(object):
    def __init__(self, n, k, q):
        # todo: проверки на размерность поля
        self.k = k  # длина сообщения
        self.n = n  # длина кодового слова
        self.q = q  # размер поля

    def get_spectrum(self):
        weights = Counter()
        for message in itertools.product(list(range(0, self.q)), repeat=self.k):
            weight = self.get_weight(self.get_codeword(message))
            weights[weight] += 1
        return weights

    def get_generating_matrix(self):
        identity_matrix = np.eye(self.k, dtype=int)
        matrix_a = np.random.randint(self.q, size=(self.k, self.n - self.k))
        return np.hstack((identity_matrix, matrix_a))

    def get_codeword(self, message):
        return (message @ self.get_generating_matrix()) % self.q  # c = i * G

    def get_random_message(self):
        return np.random.randint(self.q, size=self.k)

    def print_params(self):
        print("Field size:", self.q)
        print("Length codeword:", self.n)
        print("Length message:", self.k)

    @staticmethod
    def get_weight(codeword):
        return np.count_nonzero(codeword)
