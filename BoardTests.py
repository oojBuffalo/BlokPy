import Board
import Block
import numpy as np
import unittest

##---------------------------------------------------------------------------------##
#| 000 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 |#
#| 020 021 022 023 024 025 026 027 028 029 030 031 032 033 034 035 036 037 038 039 |#
#| 040 041 042 043 044 045 046 047 048 049 050 051 052 053 054 055 056 057 058 059 |#
#| 060 061 062 063 064 065 066 067 068 069 070 071 072 073 074 075 076 077 078 079 |#
#| 080 081 082 083 084 085 086 087 088 089 090 091 092 093 094 095 096 097 098 099 |#
#| 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 |#


class BoardTests(unittest.TestCase):

    def test_rm_oob_idxs(self):
        theBoard = Board.Board()
        cross_mat = np.vstack(([0,1,0],[1,1,1],[0,1,0]))
        cross_rs,cross_cs = np.nonzero(cross_mat)

        rs_up1 = cross_rs-1
        rs_dn1 = cross_rs+18
        cs_lf1 = cross_cs-1
        cs_rt1 = cross_cs+18

        x = theBoard.rm_oob_idxs(rs_up1,cross_cs)
        #self.assertEqual(len(x),4)
        self.assertEqual(np.equal(x,[0,1,2,21]).all(),True)

        x = theBoard.rm_oob_idxs(cross_rs,cs_lf1)
        self.assertEqual(np.equal(x,[0,20,21,40]).all(),True)

        x = theBoard.rm_oob_idxs(rs_up1,cs_lf1)
        self.assertEqual(np.equal(x,[0,1,20]).all(),True)

        x = theBoard.rm_oob_idxs(cross_rs,cs_rt1)
        self.assertEqual(np.equal(x,[19,38,39,59]).all(),True)

        x = theBoard.rm_oob_idxs(rs_up1,cs_rt1)
        self.assertEqual(np.equal(x,[18,19,39]).all(),True)

        x = theBoard.rm_oob_idxs(rs_dn1,cross_cs)
        self.assertEqual(np.equal(x,[361,380,381,382]).all(),True)

        x = theBoard.rm_oob_idxs(rs_dn1,cs_lf1)
        self.assertEqual(np.equal(x,[360,380,381]).all(),True)

        x = theBoard.rm_oob_idxs(rs_dn1,cs_rt1)
        self.assertEqual(np.equal(x,[379,398,399]).all(),True)
        #print(theBoard.to_string())

    def test_adjacent(self):
        theBoard = Board.Board()
        cross_mat = np.vstack(([0,1,0],[1,1,1],[0,1,0]))
        cross_rs,cross_cs = np.nonzero(cross_mat)

        #all adjacent spots free
        x = theBoard.adjacent(cross_rs+1,cross_cs+1)
        self.assertEqual(np.equal(x,[2,21,23,40,44,61,63,82]).all(),True)

        #no adjacent above
        x = theBoard.adjacent(cross_rs,cross_cs+1)
        self.assertEqual(np.equal(x,[1,3,20,24,41,43,62]).all(),True)

        #no adjacent left
        x = theBoard.adjacent(cross_rs+1,cross_cs)
        self.assertEqual(np.equal(x,[1,20,22,43,60,62,81]).all(),True)

        #no adjacent above or left
        x = theBoard.adjacent(cross_rs,cross_cs)
        self.assertEqual(np.equal(x,[0,2,23,40,42,61]).all(),True)

    def test_vertices(self):
        theBoard = Board.Board()
        cross_mat = np.vstack(([0,1,0],[1,1,1],[0,1,0]))
        cross_rs,cross_cs = np.nonzero(cross_mat)

        #all diagonally adjacent spots free
        x = theBoard.vertices(cross_rs+1,cross_cs+1)
        self.assertEqual(np.equal(x,[1,3,20,24,60,64,81,83]).all(),True)

        #no above diagonally adjacent spots free
        x = theBoard.vertices(cross_rs,cross_cs+1)
        self.assertEqual(np.equal(x,[0,4,40,44,61,63]).all(),True)

        #no left diagonally adjacent spots free
        x = theBoard.vertices(cross_rs+1,cross_cs)
        self.assertEqual(np.equal(x,[0,2,23,63,80,82]).all(),True)

        #no above or left diagonally adjacent spots free
        x = theBoard.vertices(cross_rs,cross_cs)
        self.assertEqual(np.equal(x,[3,43,60,62]).all(),True)

if __name__ == '__main__':
    unittest.main()
