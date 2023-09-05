def transpose_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(i, len(matrix)):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix


print(transpose_matrix([[1, 0, 1], [1, 0, 1], [1, 0, 1]]))
