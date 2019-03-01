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
        r,c = mat.shape
        assert r == c
        self.__dim = r
        self.__card = np.count_nonzero(mat)
        assert self.is_valid()

    def __eq__(self,other):
        if isinstance(other,self.__class__):
            return self.__mat.all() == other.get_mat().all()
        else: False

    #Function verifies traditional game pieces.
    #INPUT: void
    #OUTPUT: boolean indicating if polyomino is a traditional game piece
    def is_valid(self):
        if self.__dim > self.__card or self.__card <= 0 or self.__card > 5:
            return False
        rs,cs = np.nonzero(self.__mat)
        if self.__num_connected((rs[0],cs[0]),1,[]) != self.__card:
            return False
        return True

    #Function counts maximum number of connected squares using a modified DFS.
    #Used to catch cases of disjoint clusters of squares (invalid blocks).
    #INPUT: @loc = tuple containing coordinates of a location within the block
    #              matrix that contain a square from which to search outwards
    #       @count = int used to keep a total count of squares while recursing
    #OUTPUT: total count of connected squares with the block matrix
    def __num_connected(self,loc,count,visited):
        r,c = loc
        visited.append(loc)

        #check right
        if c+1 < self.__dim and self.__mat[r][c+1] and not (r,c+1) in visited:
            count = self.__num_connected((r,c+1),count+1,visited)
        #check down
        if r+1 < self.__dim and self.__mat[r+1][c] and not (r+1,c) in visited:
            count = self.__num_connected((r+1,c),count+1,visited)
        #check up
        if r-1 >= 0 and self.__mat[r-1][c] and not (r-1,c) in visited:
            count = self.__num_connected((r-1,c),count+1,visited)
        #check left
        if c-1 >= 0 and self.__mat[r][c-1] and not (r,c-1) in visited:
            count = self.__num_connected((r,c-1),count+1,visited)
        return count

    def rotate(self,rots=1):
        return np.rot90(self.__mat,rots%4)

    def reflect(self,axis=0):
        if axis == 0:
            return np.flipud(self.__mat)
        return np.fliplr(self.__mat)

    #not mem efficient
    #shifts piece to most up-left position, then pads
    def standardize(self,mat):
        new_mat = mat
        while (new_mat[:,0] == 0).all():
            new_mat = np.roll(new_mat,-1,axis=1)
        while (new_mat[0,:] == 0).all():
            new_mat = np.roll(new_mat,-1,axis=0)
        return pad(new_mat)

    def pad(og_mat):
        mat = np.insert(og_mat,0,0,axis=0)
        mat = np.insert(mat,0,0,axis=1)
        if (mat[mat.shape[0]-1,:] != 0).any():
            mat = np.insert(mat,mat.shape[0],0,axis=0)
        if (mat[:,mat.shape[0]-1] != 0).any():
            mat = np.insert(mat,mat.shape[0],0,axis=1)
        return mat

    #not mem nor time efficient - should be better algo that considers symmetry...
    def transformations(self):
        if self.__card == 1 : return [self]
        mat = self.__mat
        ref = np.fliplr(mat)
        rot = lambda m,n : [self.standardize(np.rot90(m,i)) for i in range(n)]
        ts = np.unique(np.concatenate((rot(mat,4),rot(ref,4))),axis=0)
        return [self.__class__.__call__(t) for t in ts]

    def get_mat(self):
        return self.__mat

    def get_card(self):
        return self.__card

    def get_dim(self):
        return self.__dim

    def to_string(self):
        s = ''
        dm = self.__dim
        for i in range(dm*dm):
            #if i == 0: s += '*'*(dm*2+1)+'\n'
            if i%dm == 0: s += '|'
            s += 'X' if self.__mat[int(i/dm)][i%dm] else ' '
            if i%dm == dm-1: s += '|\n'
            #if i == dm*dm-1: s += '*'*(dm*2+1)+'\n'
        return s
