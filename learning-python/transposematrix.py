def transpose_matrix(matrix):
    for i in xrange(len(matrix)):
        for j in xrange(i, len(matrix)):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    return matrix
            

print(transpose_matrix([[1, 0, 1], [1, 0, 1], [1, 0, 1]]))
