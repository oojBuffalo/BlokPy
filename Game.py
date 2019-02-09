import Block
import Player
import Board

class Game(object):

    __board = None
    __players = [None,None,None,None]

    def __init__(self,board_size,max_block_card):
        self.__board = Board.Board(board_size)
        blocks = lambda n : self.gen_blocks(n)
        self.__players[0] = Player.Player(1,blocks(max_block_card))
        self.__players[1] = Player.Player(2,blocks(max_block_card))
        self.__players[2] = Player.Player(3,blocks(max_block_card))
        self.__players[3] = Player.Player(4,blocks(max_block_card))

    def gen_blocks(self,n):
        #this is gonna be tricky...
        raise Exception('Unimplemented')

    def take_turn(self,p):
        #player take 1 turn
        raise Exception('Unimplemented')

    def play(self):
        while (self.__players.has_move()).any():
            raise Exception('Unimplemented')
