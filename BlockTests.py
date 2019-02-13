import Block
import numpy as np
import unittest

class BlockTests(unittest.TestCase):

    def test_block_validity(self):
        #mat not n-by-n
        bad = np.vstack(([1,0,1],[1,1,1]))
        self.assertRaises(AssertionError,Block.Block,bad)

        #dim > card
        bad = np.array([[1,0],[0,0]])
        self.assertRaises(AssertionError,Block.Block,bad)

        #card = 0
        bad = np.zeros(1).reshape(1,1)
        self.assertRaises(AssertionError,Block.Block,bad)

        #card > 5
        bad = np.ones(9).reshape(3,3)
        self.assertRaises(AssertionError,Block.Block,bad)

        #disjoint parts
        bad = np.vstack(([1,1,1],[0,0,0],[1,0,0]))
        self.assertRaises(AssertionError,Block.Block,bad)

        bad = np.vstack(([1,0,0],[0,1,0],[0,0,1]))
        self.assertRaises(AssertionError,Block.Block,bad)

        bad = np.vstack(([1,0],[0,1]))
        self.assertRaises(AssertionError,Block.Block,bad)

        bad = np.vstack(([1,0,1],[0,0,0],[1,0,1]))
        self.assertRaises(AssertionError,Block.Block,bad)

        bad = np.vstack(([1,0,1],[0,1,0],[1,0,1]))
        self.assertRaises(AssertionError,Block.Block,bad)

        #good block
        good = np.vstack(([1,0,1],[1,1,1],[0,0,0]))
        self.assertIsInstance(Block.Block(good),Block.Block)

        #print(Block.Block(good).to_string())

    def test_transformations(self):
        #block of card 1 - base case
        blok = Block.Block(np.ones(1).reshape(1,1))
        expected = [blok]
        self.assertEqual(expected,blok.transformations())

        #block of card 2 - 6 dups rm'd
        blok = Block.Block(np.array([[1,1],[0,0]]))
        exp_mats = np.array([[[1,0],[1,0]],[[1,0],[1,0]]])
        expected = [Block.Block(em) for em in exp_mats]
        self.assertEqual(expected,blok.transformations())

        #block of card 3 - 4 dups rm'd
        blok = Block.Block(np.array([[1,1],[1,0]]))
        exp_mats = np.array([[[1,1],[1,0]],[[1,0],[1,1]],[[0,1],[1,1]],[[1,1],[0,1]]])
        expected = [Block.Block(em) for em in exp_mats]
        self.assertEqual(expected,blok.transformations())

        #block of card 4 - 0 dups rm'd, but 4 standardized
        blok = Block.Block(np.array([[1,1,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]]))
        m1 = np.array([[1,1,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]])
        m2 = np.array([[1,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]])
        m3 = np.array([[0,1,0,0],[0,1,0,0],[0,1,0,0],[1,1,0,0]])
        m4 = np.array([[1,1,1,1],[0,0,0,1],[0,0,0,0],[0,0,0,0]])
        m5 = np.array([[1,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]])
        m6 = np.array([[1,1,1,1],[1,0,0,0],[0,0,0,0],[0,0,0,0]])
        m7 = np.array([[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,1,0,0]])
        m8 = np.array([[0,0,0,1],[1,1,1,1],[0,0,0,0],[0,0,0,0]])
        exp_mats = np.array((m1,m2,m3,m4,m5,m6,m7,m8))
        expected = [Block.Block(em) for em in exp_mats]
        self.assertEqual(expected,blok.transformations())



if __name__ == '__main__':
    unittest.main()
