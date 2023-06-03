# game.py


class IllegalMove(Exception):
    def __init__(self):
        Exception.__init__(self)


class WrongTurn(Exception):
    def __init__(self):
        Exception.__init__(self)


class EndOfGame(Exception):
    def __init__(self):
        Exception.__init__(self)


class NoPossibleAIMoves(Exception):
    def __init__(self):
        Exception.__init__(self)


class Game:
    PLAYER_ONE = 0
    PLAYER_TWO = 1
    DRAW = 2
    BOARD_ROWS = 6
    BOARD_COLUMNS = 7
    NUMBER_OF_CHECKS = 3
    VICTORY_LENGTH = 4

    def __init__(self):
        """building the board"""
        self.__board = [
            [None for i in range(Game.BOARD_COLUMNS)] for j in range(Game.BOARD_ROWS)
        ]

    def make_move(self, column):
        """this method putting a disk in a given column.
        :param column: number of column
        :return True if move was legal and IllegalMove exception otherwise.
        """
        for i in range(Game.BOARD_ROWS - 1, -1, -1):
            if self.__board[i][column] is None:
                self.__board[i][column] = self.get_current_player()
                return i, column
            elif i == 0 or None not in self.__board[0]:
                raise IllegalMove

    def get_current_player(self):
        """finding out which player is the current player by counting number
        of disks in board
        :return for player two - 1 and 0 for player one.
        """
        counter = 0
        for row in range(Game.BOARD_ROWS):
            for col in range(Game.BOARD_COLUMNS):
                if self.__board[row][col] is not None:
                    counter += 1
        if counter % 2 == 0:
            return Game.PLAYER_ONE
        else:
            return Game.PLAYER_TWO

    def get_player_at(self, row, col):
        """
        method for getting the player in place in board.
        :param row: index for row
        :param col: index for column
        :return: integer for the player in case of player and None otherwise
        """
        return self.__board[row][col]

    def get_winner(self):
        """this method checks for a winner
        :return for draw - 2 and None, for winning of player two - 2 and 0 for
        winning of player one.
        in case of winning it also returns the coordinate of the four.
        """
        # check rows 0-2 columns 0-3 right diagonals
        coordinates = []
        for check in range(self.NUMBER_OF_CHECKS):
            for row in range(self.BOARD_COLUMNS - self.VICTORY_LENGTH):
                for col in range(self.VICTORY_LENGTH):
                    player = self.get_player_at(row, col)
                    if player is None:
                        continue
                    coordinates.append([row, col])
                    for seq in range(1, self.VICTORY_LENGTH):
                        if check == 0:  # check rows
                            if self.get_player_at(row, col + seq) == player:
                                coordinates.append([row, col + seq])
                            else:
                                coordinates = []
                                break
                        if check == 1:  # check columns
                            if self.get_player_at(row + seq, col) == player:
                                coordinates.append([row + seq, col])
                            else:
                                coordinates = []
                                break
                        if check == 2:  # check right diagonal
                            if self.get_player_at(row + seq, col + seq) == player:
                                coordinates.append([row + seq, col + seq])
                            else:
                                coordinates = []
                                break
                    if len(coordinates) == self.VICTORY_LENGTH:
                        new_coordinates = self.traslate_coordinates(coordinates)
                        return player, new_coordinates
                    else:
                        coordinates = []
        coordinates = []
        # checking rows 3-5 and left diagonals
        for check in range(self.NUMBER_OF_CHECKS - 1):
            for row in range(3, 6):
                for col in range(0, 4):
                    player = self.get_player_at(row, col)
                    if player is None:
                        continue
                    coordinates.append([row, col])
                    for seq in range(1, self.VICTORY_LENGTH):
                        if check == 0:  # check rows
                            if self.get_player_at(row, col + seq) == player:
                                coordinates.append([row, col + seq])
                            else:
                                coordinates = []
                                break
                        if check == 1:  # check left diagonal
                            if self.get_player_at(row - seq, col + seq) == player:
                                coordinates.append([row - seq, col + seq])
                            else:
                                coordinates = []
                                break
                    if len(coordinates) == self.VICTORY_LENGTH:
                        new_coordinates = self.traslate_coordinates(coordinates)
                        return player, new_coordinates
                    else:
                        coordinates = []
        # check columns 4-6
        for row in range(3, 6):
            for col in range(4, 7):
                player = self.get_player_at(row, col)
                if player is None:
                    continue
                coordinates.append([row, col])
                for seq in range(1, self.VICTORY_LENGTH):
                    if self.get_player_at(row - seq, col) == player:
                        coordinates.append([row - seq, col])
                    else:
                        coordinates = []
                        break
                if len(coordinates) == self.VICTORY_LENGTH:
                    new_coordinates = self.traslate_coordinates(coordinates)
                    return player, new_coordinates
                else:
                    coordinates = []
        if None not in self.__board[0]:
            return None, self.DRAW
        return None, None

    def traslate_coordinates(self, coordinates):
        """
        translate the coordinates of the four in a row from (row,col) format to
        canvas number format.
        :param coordinates: list of the four coordinates in (row,col) format
        :return: list of coordinates in canvas num format (int)
        """
        new_coordinates = []
        for coordinate in coordinates:
            row = coordinate[0]
            col = coordinate[1]
            new_coordinates.append(row * 7 + col)
        return new_coordinates

    def __getitem__(self, index):
        """
        for getting access to the board items
        :param index: index for board
        :return: the value for wanted index.
        """
        return self.__board[index]
