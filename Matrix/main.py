# skończone
from typing import Tuple, List, Union


class Matrix:

    def __init__(self, data: Union[Tuple[int, int], List[List[float]]], value_zero: float = 0):
        if isinstance(data, Tuple):
            self.matrix: List[List[float]] = [[value_zero] * data[1] for i in range(data[0])]
        else:
            self.matrix = data

    def __add__(self, other):
        if self.size() == other.size():
            result = Matrix(self.size())
            for i in range(self.size()[0]):
                for j in range(self.size()[1]):
                    result[i][j] = self[i][j] + other[i][j]
            return result
        else:
            raise Exception("Matrices are different sizes!")

    def __mul__(self, other):
        if self.size()[1] == other.size()[0]:
            result = Matrix((self.size()[0], other.size()[1]))
            for j in range(other.size()[1]):
                for i in range(self.size()[0]):
                    partial_result: float = 0
                    for k in range(self.size()[1]):
                        partial_result += self[i][k] * other[k][j]
                    result[i][j] = partial_result
            return result
        else:
            raise Exception("Matrices must have sizes N x M and M x K.")

    def __getitem__(self, item):
        return self.matrix[item]

    def __str__(self):
        result = ""
        for i in range(self.size()[0]):
            for j in range(self.size()[1]):
                if j == 0 and i == 0:
                    result += f"[[{self[i][j]}, "
                elif j == 0 and i != 0:
                    result += f" [{self[i][j]}, "
                elif j == self.size()[1] - 1 and i != self.size()[0] - 1:
                    result += f"{self[i][j]}]\n"
                elif j == self.size()[1] - 1 and i == self.size()[0] - 1:
                    result += f"{self[i][j]}]]"
                else:
                    result += f"{self[i][j]}, "
        return result

    def size(self):
        return len(self.matrix), len(self.matrix[0])


def transpose(matrix: Matrix) -> Matrix:
    if not isinstance(matrix, Matrix):
        raise Exception("Only matrices can be transposed!")
    else:
        result = Matrix((matrix.size()[1], matrix.size()[0]))
        for i in range(matrix.size()[0]):
            for j in range(matrix.size()[1]):
                result[j][i] = matrix[i][j]
        return result


# dodatkowe

def chio(matrix: Matrix) -> float:
    if matrix.size()[0] != matrix.size()[1]:
        raise Exception("Matrix must be square!")
    elif matrix.size()[0] < 2 or matrix.size()[1] < 2:
        return matrix[0][0]
    else:
        reduced_matrix = Matrix((matrix.size()[0] - 1, matrix.size()[1] - 1))
        if matrix[0][0] != 0:
            for i in range(1, matrix.size()[0]):
                for j in range(1, matrix.size()[0]):
                    reduced_matrix[i - 1][j - 1] = matrix[0][0] * matrix[i][j] - matrix[0][j] * matrix[i][0]

            return chio(reduced_matrix) / (matrix[0][0] ** (matrix.size()[0] - 2))
        else:
            help_matrix = [[0] * matrix.size()[0] for i in range(matrix.size()[0])]
            for i in range(matrix.size()[0]):
                help_matrix[i] = matrix[i]
            for i in range(matrix.size()[0]):
                if matrix[i][0] == 0 and i == matrix.size()[0] - 1:
                    return 0
                elif matrix[i][0] == 0:
                    continue
                else:
                    help_matrix[0], help_matrix[i] = help_matrix[i], help_matrix[0]
                    break
            for i in range(1, matrix.size()[0]):
                for j in range(1, matrix.size()[0]):
                    reduced_matrix[i - 1][j - 1] = help_matrix[0][0] * help_matrix[i][j] - help_matrix[0][j] * \
                                                   help_matrix[i][0]
            return -chio(reduced_matrix) / (help_matrix[0][0] ** (matrix.size()[0] - 2))


def main():
    matrix1 = Matrix([[1, 0, 2], [-1, 3, 1]])
    matrix1_t = transpose(matrix1)
    print("Transpozycja:\n", matrix1_t)
    matrix2 = Matrix((2, 3), 1)
    sum_matrix = matrix1 + matrix2
    print("Dodawanie:\n", sum_matrix)
    matrix3 = Matrix([[3, 1], [2, 1], [1, 0]])
    mul_matrix = matrix1 * matrix3
    print("Mnożenie:\n", mul_matrix)

    matrix4 = Matrix([[5, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9, 1, 0, 7, 0], [1, 4, 7, 2, 2]])
    wyznacznik1 = chio(matrix4)
    print(wyznacznik1)

    matrix5 = Matrix([[0, 1, 1, 2, 3], [4, 2, 1, 7, 3], [2, 1, 2, 4, 7], [9, 1, 0, 7, 0], [1, 4, 7, 2, 2]])
    wyznacznik2 = chio(matrix5)
    print(wyznacznik2)

    matrix5 = Matrix([[0, 1, 1, 2, 3], [0, 2, 1, 7, 3], [0, 1, 2, 4, 7], [0, 1, 0, 7, 0], [0, 4, 7, 2, 2]])
    wyznacznik2 = chio(matrix5)
    print(wyznacznik2)


if __name__ == '__main__':
    main()
