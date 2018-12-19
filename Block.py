import numpy as np

class Block(object):

    """
    This class will represent a unique polyomino of an arbitrary size.
    More clearly, a single block may represent the polyomino in any
    permutation.
    """

    ##Blocks represented within 2D matrix space
    ##If 1 in spot [i][j], unit of block exists,
    ##otherwise if 0 in spot [i][j] then free space exists.
    cardinality = 0
    matrix_rep = None

    def __init__(self,matrix):
        matrix_rep = matrix
        cardinality = np.count_nonzero(matrix)
        matrix_size = matrix.shape

    def is_valid(self,matrix):
        xs,ys = np.nonzero(matrix)
        

    def rotate(self,dir=-1,rots=1):
        true_rots = rots % 4
        new_mat = np.rot90(self.matrix_rep,true_rots)

    def reflect(self,axis=0):
        if axis == 0:
            return np.flipud(self.matrix_rep)
        return np.fliplr(self.matrix_rep)
