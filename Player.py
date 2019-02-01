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

    # def place_block(self,block,board,loc):
    #     board.place(self.color,block,loc)
    #     block_set = block_set - block

    def get_pid(self):
        return self.pid

    def get_rem_blocks(self):
        return self.block_set

    def num_rem_blocks(self):
        return len(self.block_set)
    #will consider adding more methods...
