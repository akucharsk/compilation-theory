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
