import Block
import numpy as np

def main():
    cross_mat = np.vstack(([0,1,0],[1,1,1],[0,1,0]))
    blok = Block.Block(cross_mat)

    u_mat = np.vstack(([1,0,1],[1,1,1],[0,0,0]))
    blok2 = Block.Block(u_mat)

if __name__ == '__main__':
    main()
