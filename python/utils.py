import numpy as np
import itertools


def vector_to_str(vector):
    result = ''
    for v in vector:
        result += str(int(v))
    return result


def int_to_vector(value, length):
    s = np.binary_repr(value, width=length)
    return np.fromstring(s, 'u1') - ord('0')


def matrix_from_columns(matrix, columns):
    size = len(columns)
    result_matrix = np.zeros((size, size), dtype=int)
    for j, column in enumerate(columns):
        result_matrix[:, j] = matrix[:, column]
    return result_matrix


def RREF_binary(matrix_a):
    n_rows, n_cols = matrix_a.shape
    current_row = 0

    for j in range(n_cols):
        if current_row >= n_rows:
            break

        pivot_row = current_row
        while pivot_row < n_rows and matrix_a[pivot_row, j] == 0:
            pivot_row += 1

        if pivot_row == n_rows:
            continue

        matrix_a[[current_row, pivot_row]] = matrix_a[[pivot_row, current_row]]

        pivot_row = current_row
        current_row += 1

        for i in range(current_row, n_rows):
            if matrix_a[i, j] == 1:
                matrix_a[i] = (matrix_a[i] + matrix_a[pivot_row]) % 2

    for i in reversed(range(current_row)):
        pivot_col = 0
        while pivot_col < n_cols and matrix_a[i, pivot_col] == 0:
            pivot_col += 1
        if pivot_col == n_cols:
            continue
        for j in range(i):
            if matrix_a[j, pivot_col] == 1:
                matrix_a[j] = (matrix_a[j] + matrix_a[i]) % 2

    return matrix_a


def inverse_matrix(matrix):
    n_rows, n_cols = matrix.shape

    if n_rows != n_cols:
        raise RuntimeError("Matrix has to be square")
    if np.around(np.linalg.det(matrix), 3) % 2 == 0:
        raise RuntimeError("Singular matrix")
    augmented_matrix = np.hstack([matrix, np.eye(n_rows)])
    rref_form = RREF_binary(augmented_matrix)
    return rref_form[:, n_rows:]


def get_all_information_sets(n, k, matrix_g):
    information_sets = []
    candidates = itertools.combinations(list(range(0, n)), k)
    for candidate in candidates:
        Gi = matrix_from_columns(matrix_g, list(candidate))
        try:
            Gi_inv = inverse_matrix(Gi)
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


def get_hamming_distance(codeword, any_codeword):
    return np.sum(codeword != any_codeword)
