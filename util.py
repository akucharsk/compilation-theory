def get_matrix_shape(matrix) :
    checker = matrix
    shape = []
    broken = False
    while not broken :
        try :
            shape.append(len(checker.elements))
            checker = checker.elements[0]
        except :
            broken = True
    return shape

    
def matrix_divide(matrix1, matrix2) :
    n1, m1 = len(matrix1), len(matrix1[0])
    n2, m2 = len(matrix2), len(matrix2[0])
    
    if n1 != n2 : return
    
    matrix3 = [[0 for _ in range(m1)] for _ in range(m2)]
    
    vector = [0] * (n1 * m1)
    for i in range(n1) :
        for j in range(m1) :
            vector[i*m1 + j] = matrix1[i][j]
    print(vector)
    
    print(matrix3)