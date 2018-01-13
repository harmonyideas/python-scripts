def transpose_matrix(matrix):
    for i in xrange(len(matrix)):
        for j in xrange(i, len(matrix)):
            temp = matrix[i][j]
            matrix[i][j] = matrix[j][i]
            matrix[j][i] = temp


transpose_matrix([[1, 0, 1], [1, 0, 1], [1, 0, 1]])
