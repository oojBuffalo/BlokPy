import numpy as np
import Util
class Board(object):
    """
    This class will store the data of where each player has placed their pieces
    at any given point during the game.  Traditionally the board is a 20x20 grid
    (i.e. when blocks of cardinality five are used).
    """
    #--------------------------------------------------------------------#
    #The board will be a 20x20 ndarray with an inital state of every cell
    #containing a zero.  A game class will control game play and call
    #methods from this class whenever and however a player wants to interact
    #with the game board.  This class is responsible for SOME of the game
    #state data.
    #--------------------------------------------------------------------#

    #board matrix : ndarray
    __grid = None
    #board size : int
    __size = None

    #Board class constructor.
    #INPUT: @n : int = the size in terms of n of an nxn board; default is 20.
    def __init__(self,n=20):
        self.__grid = np.zeros(n*n,dtype=int).reshape(n,n)
        self.__size = n

    #Function indicate whether a block placed on the board at a specific
    #location is a valid move.
    #INPUT: @pid : int = the player's id
    #       @board_rs : int-ndarray : block's row indices on board
    #       @board_cs : int-ndarray : block's column indices on board
    #OUTPUT: if valid move then void
    #        else throws an exception
    def is_valid_placement(self,pid,board_rs,board_cs):
        #---------------------Check if move is valid----------------------#
        #Condition 1: invalid if any squares in the block are off the grid.
        if ((board_rs < 0).any()
            or (board_rs >= self.__size).any()
            or (board_rs < 0).any()
            or (board_rs >= self.__size).any()):
            raise Exception("Block not on grid")

        #Condition 2: invalid if the space is already occupied
        board_pstns = (board_rs)*self.__size+(board_cs)
        space = np.take(self.__grid,board_pstns)
        if (space != 0).any():
            raise Exception("Space already occupied")

        #Condition 3: invalid if any adjacent grid cells contain the same pid.
        adj_idxs = adjacent(board_rs,board_cs)
        space = np.take(self.__grid,adj_idxs)
        if space.any() == pid:
            raise Exception("Own block adjacent")

        #Condition 4: invalid if all diagonally adjacent grid cells do not
        #             contain the same pid.
        vert_idxs = diagonal(board_rs,board_cs)
        space = np.take(self.__grid,vert_idxs)
        if (space != pid).all() and np.isin(pid,self.__grid.flatten()):
            raise Exception("No diagonally adjacent blocks")
        #-------------------------Move is valid---------------------------#


    #Function allows a player to place any (transformed) block onto the board.
    #INPUT: @pid : int = the player's id
    #       @block : Block = the (transformed) block
    #       @loc : list = the location in which the [0][0]th entry of the
    #                      matrix underlying the block object is to be placed
    #OUTPUT: void
    def place_block(self,pid,block,loc):
        block_rs,block_cs = np.nonzero(block.get_mat())
        board_rs = block_rs+loc[0]
        board_cs = block_cs+loc[1]
        self.is_valid_placement(pid,board_rs,board_cs,loc)
        board_idxs = board_rs*self.__size+board_cs
        np.put(self.__grid,board_idxs,pid)
        print(self.to_string())

    #Function returns all open diagonally adjacent cells.
    #INPUT: @pid : int = the player's id
    #OUTPUT: 1D-ndarray = flattened indices of diagonally adjacent open cells
    def player_vertices(self,pid):
        plyr_rs,plyr_cs = np.where(self.__grid == pid)
        plyr_verts = vertices(plyr_rs,plyr_cs,self.__size)
        open_verts = np.where(self.__grid.flatten(plyr_verts) == 0)
        return open_verts[0]

    #Function returns a copy of the matrix that stores the board data.
    #INPUT: void
    #OUTPUT: 2D-ndarray = (shallow) copy of self.__grid
    def get_grid(self):
        return self.__grid.copy()

    #Function converts board data into a string
    #INPUT: void
    #OUTPUT: string = representation of board data
    def to_string(self):
        s = ''
        sz = self.__size
        dgts = lambda n : len(str(int(n)))
        sz_dgts = dgts(sz)
        for i in range(sz*sz):
            if i == 0: s += '-'*(sz*2+sz_dgts+5)+'\n'
            if i%sz == 0: s += ' '*(sz_dgts-dgts(i/sz))+str(i//sz)+': | '
            if i == 0: s += str(self.__grid[0][0])+' '
            else: s += str(self.__grid[i//sz][i%sz])+' '
            if i%sz == sz-1: s += '|\n'
            if i == sz*sz-1: s += '-'*(sz*2+sz_dgts+5)+'\n'
        return s
