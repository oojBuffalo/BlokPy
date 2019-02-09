import numpy as np

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
        adj_pstns = self.adjacent(board_rs,board_cs)
        space = np.take(self.__grid,adj_pstns)
        if space.any() == pid:
            raise Exception("Own block adjacent")

        #Condition 4: invalid if all diagonally adjacent grid cells do not
        #             contain the same pid.
        vert_pstns = self.vertices(board_rs,board_cs)
        space = np.take(self.__grid,vert_pstns)
        if (space != pid).all() and np.isin(pid,self.__grid.flatten()):
            raise Exception("No diagonally adjacent blocks")

        #-------------------------Move is valid---------------------------#
        np.put(self.__grid,board_pstns,pid)

    def rm_oob_idxs(self,rs,cs):

        oob_up = np.where(rs < 0)[0]
        oob_dn = np.where(rs >= self.__size)[0]
        oob_lf = np.where(cs < 0)[0]
        oob_rt = np.where(cs >= self.__size)[0]

        if (len(oob_up) == 0
            and len(oob_dn) == 0
            and len(oob_lf) == 0
            and len(oob_rt) == 0):
            return rs*self.__size+cs

        oob_idxs = np.unique(np.concatenate((oob_up,oob_dn,oob_lf,oob_rt)))
        new_rs = np.delete(rs,oob_idxs)
        new_cs = np.delete(cs,oob_idxs)
        return new_rs*self.__size+new_cs

    def adjacent(self,board_rs,board_cs):
        board_pstns = board_rs*self.__size+board_cs

        raw_up = board_rs-1
        raw_dn = board_rs+1
        raw_lf = board_cs-1
        raw_rt = board_cs+1

        up = self.rm_oob_idxs(raw_up,board_cs)
        dn = self.rm_oob_idxs(raw_dn,board_cs)
        lf = self.rm_oob_idxs(board_rs,raw_lf)
        rt = self.rm_oob_idxs(board_rs,raw_rt)

        all_pstns = np.unique(np.concatenate((up,lf,rt,dn)))
        final = all_pstns[np.isin(all_pstns,board_pstns,invert=True)]
        final.sort()
        return final

    def vertices(self,board_rs,board_cs):
        board_pstns = board_rs*self.__size+board_cs

        up = board_rs-1
        dn = board_rs+1
        lf = board_cs-1
        rt = board_cs+1

        up_lf = self.rm_oob_idxs(up,lf)
        up_rt = self.rm_oob_idxs(up,rt)
        dn_lf = self.rm_oob_idxs(dn,lf)
        dn_rt = self.rm_oob_idxs(dn,rt)

        raw_pstns = np.concatenate((up_lf,up_rt,dn_lf,dn_rt))
        no_block_pstns = raw_pstns[np.isin(raw_pstns,board_pstns,invert=True)]
        adj_pstns = self.adjacent(board_rs,board_cs)
        final = no_block_pstns[np.isin(no_block_pstns,adj_pstns,invert=True)]
        final.sort()
        return final

    def get_grid(self):
        return self.__grid.copy()

    def to_string(self):
        s = ''
        sz = self.__size
        dgts = lambda n : len(str(int(n)))
        sz_dgts = dgts(sz)
        for i in range(sz*sz):
            if i == 0: s += '-'*(sz*2+sz_dgts+5)+'\n'
            if i%sz == 0: s += ' '*(sz_dgts-dgts(i/sz))+str(int(i/sz))+': | '
            if i == 0: s += str(self.__grid[0][0])+' '
            else: s += str(self.__grid[int(i/sz)][i%sz])+' '
            if i%sz == sz-1: s += '|\n'
            if i == sz*sz-1: s += '-'*(sz*2+sz_dgts+5)+'\n'
        return s
