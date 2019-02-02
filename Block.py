import numpy as np
#from scipy.sparse import csr_matrix
#from scipy.sparse.csgraph import connected_components

class Block(object):
    """
    This class will represent a unique polyomino of an arbitrary size.
    More clearly, a single instance of "block" may represent the distinct
    polyomino in any of its permutations.
    """
    #--------------------------------------------------------------------#
    #Blocks represented within 2D matrix space.
    #If value 1 at location [i][j], then a single atomic unit of a block
    #(aka a "square") exists at that location.
    #Conversely, if value 0 at location [i][j], then free space exists.
    #--------------------------------------------------------------------#
    #Example: ndarray([[0,1,0]
    #                  [1,1,1]      <---represents block shaped like
    #                  [0,1,0]])        a "plus" or a "cross"
    #--------------------------------------------------------------------#

    #block matrix
    __mat = None
    #cardinality of block
    __card = None
    #dimension(s) of block matrix
    __dim = None

    def __init__(self,mat):
        self.__mat = mat
        self.__dim,_ = mat.shape
        self.__card = np.count_nonzero(mat)
        assert self.is_valid()

    #Function verifies traditional game pieces.
    #INPUT: void
    #OUTPUT: boolean indicating if polyomino is a traditional game piece
    def is_valid(self):
        if self.__dim > self.__card or self.__card <= 0 or self.__card > 5:
            return False
        rs,cs = np.nonzero(self.__mat)
        if self.num_connected((rs[0],cs[0]),1,[]) != self.__card:
            return False
        return True

    #Function counts maximum number of connected squares using a modified DFS.
    #Used to catch cases of disjoint clusters of squares (invalid blocks).
    #INPUT: @loc = tuple containing coordinates of a location within the block
    #              matrix that contain a square from which to search outwards
    #       @count = int used to keep a total count of squares while recursing
    #OUTPUT: total count of connected squares with the block matrix
    def num_connected(self,loc,count,visited):
        r,c = loc
        visited.append(loc)

        #print(visited)

        #check right
        if c+1 < self.__dim and self.__mat[r][c+1] and not (r,c+1) in visited:
            count = self.num_connected((r,c+1),count+1,visited)
        #check down
        if r+1 < self.__dim and self.__mat[r+1][c] and not (r+1,c) in visited:
            count = self.num_connected((r+1,c),count+1,visited)
        #check up
        if r-1 >= 0 and self.__mat[r-1][c] and not (r-1,c) in visited:
            count = self.num_connected((r-1,c),count+1,visited)
        #check left
        if c-1 >= 0 and self.__mat[r][c-1] and not (r,c-1) in visited:
            count = self.num_connected((r,c-1),count+1,visited)
        return count

    def rotate(self,dir=-1,rots=1):
        true_rots = rots % 4
        return np.rot90(self.__mat,true_rots)

    def reflect(self,axis=0):
        if axis == 0:
            return np.flipud(self.__mat)
        return np.fliplr(self.__mat)

    def get_mat(self):
        return self.__mat

    def get_card(self):
        return self.__card

    def get_dim(self):
        return self.__dim
