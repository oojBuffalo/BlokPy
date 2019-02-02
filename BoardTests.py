import Board
import Block
import numpy as np
import unittest

class BoardTests(unittest.TestCase):

    def test_rm_oob_idxs(self):
        theBoard = Board.Board()
        cross_mat = np.vstack(([0,1,0],[1,1,1],[0,1,0]))
        cross_rs,cross_cs = np.nonzero(cross_mat)
        rs_up1 = cross_rs-1
        x = theBoard.rm_oob_idxs(rs_up1,cross_cs,np.where(rs_up1<0)[0],[])
        self.assertEqual(len(x),4)
        self.assertEqual(np.equal(x,[0,1,2,21]).all(),True)

if __name__ == '__main__':
    unittest.main()
