# ai.py

import random
import game


class AI:
    def __init__(self, server):
        """
        :param server: boolean tells if server or not
        """
        self.__server = server

    def find_legal_move(self, board, make_move_func):
        """
        this method is finding some random move and executing it.
        :param board: Game object representation for the board
        :param make_move_func: Game method for executing moves
        :return row and column of the move
        """
        if None not in board[0]:
            raise game.NoPossibleAIMoves
        optional_move = []
        for i, col in enumerate(board[0]):
            if col is None:
                optional_move.append(i)
        col = random.choice(optional_move)
        # find the row
        for row in range(game.Game.BOARD_ROWS - 1, -1, -1):
            if board[row][col] is None:
                break
        make_move_func(col)
        return row, col
