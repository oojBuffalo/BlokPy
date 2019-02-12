import Block
import numpy as np
import unittest

class BlockTests(unittest.TestCase):

    def test_block_validity(self):
        #mat not n-by-n
        bad = np.vstack(([1,0,1],[1,1,1]))
        self.assertRaises(AssertionError,Block.Block(bad))

        #dim > card
        bad = np.array([[1,0],[0,0]])
        self.assertRaises(AssertionError,Block.Block(bad))

        #card = 0
        self.assertRaises(AssertionError,Block.Block(np.array([0])))

        #card > 5
        bad = np.ones(9).reshape(3,3)
        self.assertRaises(AssertionError,Block.Block(bad))

        #disjoint parts
        bad = np.vstack(([1,1,1],[0,0,0],[1,0,0]))
        self.assertRaises(AssertionError,Block.Block(bad))

        bad = np.vstack(([1,0,0],[0,1,0],[0,0,1]))
        self.assertRaises(AssertionError,Block.Block(bad))

        bad = np.vstack(([1,0],[0,1]))
        self.assertRaises(AssertionError,Block.Block(bad))

        bad = np.vstack(([1,0,1],[0,0,0],[1,0,1]))
        self.assertRaises(AssertionError,Block.Block(bad))

        bad = np.vstack(([1,0,1],[0,1,0],[1,0,1]))
        self.assertRaises(AssertionError,Block.Block(bad))

        #good block
        good = np.vstack(([1,0,1],[1,1,1],[0,0,0]))
        self.assertIsInstance(Block.Block(good),Block)

        #def test_transformations(self):


if __name__ == '__main__':
    unittest.main()
