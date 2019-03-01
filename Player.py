class Player(object):
    """
    This class will act as one/two of the two/three/four players required to
    play Blokus.  A single instance of this class will have its own set of
    Blocks (polyominoes) that are of cardinality [1,5] and are unique.  By
    "unique", I mean to say that regardless of how a player rotates or
    reflects a unique block, it will never match another (subject to the same
    aforementioned conditions).

    Additionally, every player will have a color assigned to them, which can
    simply be thought of as a UID.  This designates the rotation in which
    each player can place a Block on the Board.
    """

    #player's id : int
    pid = None
    #set of Blocks/game pieces : list of block objects
    block_set = None

    def __init__(self,uid,given_blocks):
        self.pid = uid
        self.block_set = given_blocks


    #player has move if one of their remaining blocks fits on the board
    #i.e. there exists a block within the set of all transformations of all
    #     remaining blocks such that the one of its transformations can be
    #     placed on the board as a valid move.
    def has_move(self,board):
        #Step 1: Find all transformations of remaining blocks.
        rem_ts = []
        rem_ts += [rb.transformations() for rb in self.block_set]
        #Step 2: Find all vertices of players colors blocks on the board
        #        s.t. they are both unfilled and in-bounds.
        board_verts = board.player_vertices(self.pid)

        raise Exception('Unimplemented')

    def possible_moves(self,board):
        raise Exception('Unimplemented')

    def choose_move(self,board):
        raise Exception('Unimplemented')

    def get_pid(self):
        return self.pid

    def get_rem_blocks(self):
        return self.block_set

    def num_rem_blocks(self):
        return len(self.block_set)
    #will consider adding more methods...
