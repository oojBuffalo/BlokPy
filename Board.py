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

  board = None
  size = None

    def __init__(self,size=20):
        self.board = np.zeros(size*size).reshape(size,size)
        self.size = size

    def place_block(self,pid,block,loc):
        r,c = loc
        block_rs,block_cs = np.nonzero(block.get_mat())
        board_idxs = (block_rs+r)*self.size+(block_cs+c)
        board_coords = np.vstack((block_rs+r),(block_cs+c)).T

        #------Check if this is a valid move------#
        #Case 1: valid if the space is unoccupied
        space = np.take(self.board,board_idxs)
        if space.any() != 0:
            raise Exception("Space is occupied")

        #Case 2: valid if the block is (exclusively) diagonally adjacent
        #        to a previously placed block of its own color
        verts = self.vertices(block_rs+r,block_cs+c)

        np.put(self.board,board_idxs,pid)

    def rm_oob_idxs(self,ud,lr,oob_ud_idxs,oob_lr_idxs):
        if len(oob_ud_idxs) == 0 and len(oob_lr_idxs) == 0:
            return ud*self.size+lr
        oob_idxs = np.unique(np.concatenate((oob_ud_idxs,oob_lr_idxs)))
        new_ud = np.delete(ud,oob_idxs)
        new_lr = np.delete(lr,oob_idxs)
        return new_ud*self.size+new_lr

    def adjacent(self,board_rs,board_cs):
        s = self.size
        #fix oob problem here
        #Imagine one entry of bd_idxs (i.e. one square of one block) is at
        #index 10 on the board.  This means shifting left would result in a
        #value of 9.  This is NOT NEGATIVE and will not be caught in the return
        #statement.
        bd_idxs = board_rs*s+board_cs

        up_idxs = bd_idxs-s
        dn_idxs = bd_idxs+s
        lf_idxs = bd_idxs-1
        rt_idxs = bd_idxs+1

        idxs = np.concatenate((up_idxs,lf_idxs,rt_idxs,dn_idxs))
        no_block_idxs = idxs[np.isin(idxs,board_idxs,invert=True)]
        return no_block_idxs[np.where(no_block_idxs >= 0)]

    def vertices(self,board_rs,board_cs):
        s = self.size
        board_idxs = board_rs*s+board_cs

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

        raw_idxs = np.concatenate((up_lf,up_rt,dn_lf,dn_rt))
        no_block_idxs = raw_idxs[np.isin(raw_idxs,board_idxs,invert=True)]
        # no_neg_idxs = no_block_idxs[np.where(no_block_idxs >= 0)]
        # no_oob_idxs = no_neg_idxs[np.where(no_neg_idxs < self.size)]
        adj_idxs = self.adjacent(board_rs,board_cs)
        return no_block_idxs[np.isin(no_block_idxs,adj_idxs,invert=True)]
