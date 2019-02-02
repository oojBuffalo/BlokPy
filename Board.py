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
    grid = None
    #board size : int
    size = None

    #Board class constructor.
    #INPUT: @n : int = the size in terms of n of an nxn board; default is 20.
    def __init__(self,n=20):
        self.grid = np.zeros(n*n).reshape(n,n)
        self.size = n

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
        if ((board_rs).any() < 0
            or (board_rs).any() >= self.size
            or (board_cs).any() < 0
            or (board_cs).any() >= self.size):
            raise Exception("Block not on grid")

        #Condition 2: invalid if the space is already occupied
        board_pstns = (board_rs)*self.size+(board_cs)
        space = np.take(self.grid,board_pstns)
        if space.any() != 0:
            raise Exception("Space already occupied")

        #Condition 3: invalid if any adjacent grid cells contain the same pid.
        adj_pstns = self.adjacent()
        space = np.take(self.grid,adj_pstns)
        if space.any() == pid:
            raise Exception("Own block adjacent")

        #Condition 4: invalid if all diagonally adjacent grid cells do not
        #             contain the same pid.
        vert_pstns = self.vertices(board_rs,board_cs)
        space = np.take(self.grid,vert_pstns)
        if space.all() != pid:
            raise Exception("No diagonally adjacent blocks")

        #-------------------------Move is valid---------------------------#

        np.put(self.grid,board_pstns,pid)

    #why ask for out of bounds indices as params?
    def rm_oob_idxs(self,ud,lr,oob_ud_idxs,oob_lr_idxs):
        if len(oob_ud_idxs) == 0 and len(oob_lr_idxs) == 0:
            return ud*self.size+lr
        oob_idxs = np.unique(np.concatenate((oob_ud_idxs,oob_lr_idxs)))
        new_ud = np.delete(ud,oob_idxs)
        new_lr = np.delete(lr,oob_idxs)
        return new_ud*self.size+new_lr

    def adjacent(self,board_rs,board_cs):
        board_pstns = board_rs*self.size+board_cs

        raw_up = board_rs-1
        raw_dn = board_rs+1
        raw_lf = board_cs-1
        raw_rt = board_cs+1

        oob_up_idxs = np.where(raw_up < 0)
        oob_dn_idxs = np.where(raw_dn >= self.size)
        oob_lf_idxs = np.where(raw_lf < 0)
        oob_rt_idxs = np.where(raw_rt >= self.size)

        up_pstns = self.rm_oob_idxs(raw_up,board_cs,oob_up_idxs,[])
        dn_pstns = self.rm_oob_idxs(raw_dn,board_cs,oob_dn_idxs,[])
        lf_pstns = self.rm_oob_idxs(board_rs,raw_lf,[],oob_lf_idxs)
        rt_pstns = self.rm_oob_idxs(board_rs,raw_rt,[],oob_rt_idxs)

        all_pstns = np.concatenate((up_pstns,lf_pstns,rt_pstns,dn_pstns))
        return all_pstns[np.isin(all_pstns,board_pstns,invert=True)]

    def vertices(self,board_rs,board_cs):
        board_pstns = board_rs*self.size+board_cs

        up = board_rs-1
        dn = board_rs+1
        lf = board_cs-1
        rt = board_cs+1

        oob_up_idxs = np.where(up < 0)
        oob_dn_idxs = np.where(dn >= self.size)
        oob_lf_idxs = np.where(lf < 0)
        oob_rt_idxs = np.where(rt >= self.size)

        up_lf = self.rm_oob_idxs(up,lf,oob_up_idxs,oob_lf_idxs)
        up_rt = self.rm_oob_idxs(up,rt,oob_up_idxs,oob_rt_idxs)
        dn_lf = self.rm_oob_idxs(dn,lf,oob_dn_idxs,oob_lf_idxs)
        dn_rt = self.rm_oob_idxs(dn,rt,oob_dn_idxs,oob_rt_idxs)

        raw_pstns = np.concatenate((up_lf,up_rt,dn_lf,dn_rt))
        no_block_pstns = raw_pstns[np.isin(raw_pstns,board_pstns,invert=True)]
        adj_pstns = self.adjacent(board_rs,board_cs)
        return no_block_pstns[np.isin(no_block_idxs,adj_idxs,invert=True)]
