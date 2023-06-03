# four_in_a_row.py

import communicator
import tkinter as tki
import game
import sys
import ai

MIN_NUM_OF_ARGS = 3
MAX_NUM_OF_ARGS = 4
ILL_PROG_ARGS = "Illegal program arguments"
WRNG_PORT_MSG = "port value must be between 0-65535"
PORT_LOCATION = 2
PLAYER_TYPE_LOCATION = 1
MAX_PORT_VALUE = 65535
LOW_PORT_VALUE = 1000


class MyBoard:
    PLAYER_ONE_WON_MSG = "Player One has won the game!"
    PLAYER_TWO_WON_MSG = "Player Two has won the game!"
    DRAW_MSG = "Draw! lets make another one!"
    PLAYER_ONE_TURN_MSG = "Player One turn!\n please choose column"
    PLAYER_TWO_TURN_MSG = "Player Two turn!\n please choose column"
    ILLEGAL_MOVE_MSG = "illegal move!"
    WRONG_TURN_MSG = "Im afraid it is not your turn,\n please wait for opponent"
    PLAYER_ONE_COLOR = "blue"
    PLAYER_TOW_COLOR = "red"
    MARKER_COLOR = "green"
    NUM_OF_CANVASES = 42
    NUM_OF_COLUMNS = 7
    NO_WINNER = "N"
    DRAW = "D"
    ONE_HAS_WON = "O"
    TWO_HAS_WON = "T"

    def __init__(self, parent, port, player_type, ip=None):
        """
        Initializes the GUI and connects the communicator.
        :param parent: the tkinter root.
        :param ip: the ip to connect to.
        :param port: the port to connect to.
        :param player_type: a string which tell if player is 'human' or 'ai'
        """
        self.__server = False
        if ip is None:
            self.__server = True
        self.__parent = parent
        self.__board = game.Game()
        self.__communicator = communicator.Communicator(parent, port, ip)
        self.__communicator.connect()
        self.__canvases_lst = []
        self.__player_type = player_type
        self.__place_widgets()
        self.__communicator.bind_action_to_message(self.__handle_message)
        if self.__player_type == "ai":
            # if an ai was chosen to play
            self.__ai = ai.AI(self.__server)
            # make the first move if you are a server or if other player is
            # also ai
            if self.__server is True:
                row, col = self.__ai.find_legal_move(
                    self.__board, self.__board.make_move
                )
                self.create_oval(self.__board.PLAYER_ONE, row, col)
                self.__communicator.send_message(
                    self.NO_WINNER + str(self.__board.PLAYER_ONE) + str(row) + str(col)
                )

    def __place_widgets(self):
        """
        this method will create the board and all of its contents.
        """
        # frame1 will contain a grid of canvases
        self.frame1 = tki.Frame(self.__parent, width=560, height=480)
        # frame two will contain an informative label
        self.frame2 = tki.Frame(self.__parent, width=560, height=80)
        self.label = tki.Label(self.frame2, text=self.PLAYER_ONE_TURN_MSG)
        self.label.config(font=("ariel", 44))
        self.label.pack()
        self.frame2.pack(side=tki.TOP)
        self.frame1.pack(side=tki.BOTTOM)
        # creating canvases and their functions
        for canvas_num in range(self.NUM_OF_CANVASES):
            self.__canvas = tki.Canvas(
                self.frame1, width=80, height=80, highlightbackground="black"
            )
            canvas_func = self.create(canvas_num)
            if self.__player_type == "human":
                self.__canvas.bind("<Button-1>", canvas_func)
            self.__canvas.grid(
                row=canvas_num // self.NUM_OF_COLUMNS,
                column=canvas_num % self.NUM_OF_COLUMNS,
            )
            self.__canvases_lst.append(self.__canvas)

    def create(self, canvas_num):
        """
        this method will create each canvas and his own function for
        creating oval
        :param canvas_num: an index for specific canvas
        :return canvas func: the matching function for given canvas
        """

        def canvas_func(event):
            try:
                if "won" in self.label["text"] or "Draw" in self.label["text"]:
                    raise game.EndOfGame
                self.action(canvas_num)
            except game.EndOfGame:
                pass

        return canvas_func

    def __handle_message(self, text=None):
        """
        Specifies the event handler for the message getting event in the
        communicator. Prints a message when invoked (and invoked by the
        communicator when a message is received). The message will
        automatically disappear after a fixed interval.
        :param text: the text to be printed.
        :return: None.
        """
        # translating the received message
        win, player, row, col = text[0], int(text[1]), int(text[2]), int(text[3])
        # updating the receiver of the message board too
        if self.__server is True:  # send make_move the opposite for last move
            self.__board.make_move(col)
        else:
            self.__board.make_move(col)
        # if the last move was made by player one paint GUI accordingly
        if player == self.__board.PLAYER_ONE:
            self.__canvases_lst[row * 7 + col].create_oval(
                0, 0, 80, 80, fill=self.PLAYER_ONE_COLOR
            )
        # if the last move was made by player two paint GUI accordingly
        elif player == self.__board.PLAYER_TWO:
            self.__canvases_lst[row * 7 + col].create_oval(
                0, 0, 80, 80, fill=self.PLAYER_TOW_COLOR
            )
        if win == self.NO_WINNER:
            self.change_label()
        elif text[0] == self.ONE_HAS_WON:
            self.label["text"] = self.PLAYER_ONE_WON_MSG
            self.marker_four(text, self.PLAYER_ONE_COLOR)
        elif text[0] == self.TWO_HAS_WON:
            self.label["text"] = self.PLAYER_TWO_WON_MSG
            self.marker_four(text, self.PLAYER_TOW_COLOR)
        elif text[0] == self.DRAW:
            self.label["text"] = self.DRAW_MSG
        try:
            if self.__player_type == "ai":
                if "won" in self.label["text"] or "Draw" in self.label["text"]:
                    raise game.EndOfGame
                self.action()
        except game.EndOfGame:
            pass

    def action(self, canvas_num="ai"):
        """
        executing the move for human or ai.
        :param canvas_num: the number of the cvanvas in case of human player
        or 'ai' in case of ai playing.
        """
        try:
            player = self.__board.get_current_player()
            if self.__player_type == "human":
                if self.__server is True and player == 1:
                    raise game.WrongTurn
                if self.__server is False and player == 0:
                    raise game.WrongTurn
                row, col = self.__board.make_move(canvas_num % 7)
                self.create_oval(player, row, col)
            else:
                row, col = self.__ai.find_legal_move(
                    self.__board, self.__board.make_move
                )
                self.create_oval(player, row, col)
            # check for a winner
            print(self.__board.get_winner())
            winner, coords = self.__board.get_winner()
            if winner is not None:
                if winner == self.__board.PLAYER_ONE:
                    self.label["text"] = self.PLAYER_ONE_WON_MSG
                    # creating the coordinates word of the four-in-a-row
                    # for marking, for client and server.
                    coordinates_word = self.create_coordinates_word(coords)
                    self.marker_four(coordinates_word, self.PLAYER_ONE_COLOR)
                    coordinates_str = (
                        self.ONE_HAS_WON + str(player) + str(row) + str(col)
                    )
                    self.__communicator.send_message(
                        coordinates_str + coordinates_word[4:]
                    )
                elif winner == self.__board.PLAYER_TWO:
                    self.label["text"] = self.PLAYER_TWO_WON_MSG
                    coordinates_word = self.create_coordinates_word(coords)
                    self.marker_four(coordinates_word, self.PLAYER_TOW_COLOR)
                    coordinates_str = (
                        self.TWO_HAS_WON + str(player) + str(row) + str(col)
                    )
                    self.__communicator.send_message(
                        coordinates_str + coordinates_word[4:]
                    )
                if winner == self.__board.DRAW:
                    self.label["text"] = self.DRAW_MSG
                    self.__communicator.send_message(
                        self.DRAW + str(player) + str(row) + str(col)
                    )
            else:
                self.change_label()
                self.__communicator.send_message(
                    self.NO_WINNER + str(player) + str(row) + str(col)
                )
        except game.IllegalMove:
            self.label["text"] = self.ILLEGAL_MOVE_MSG
        except game.WrongTurn:
            self.label["text"] = self.WRONG_TURN_MSG
        except game.EndOfGame:
            pass

    def marker_four(self, text, player_color):
        """
        method for marker the four in a row
        :param text: string which contains the four coordinates to be mark.
        :param player_color: string for the winner's color
        """
        for i in range(0, 8, 2):
            self.__canvases_lst[int(str(text)[4 + i : 6 + i])].create_oval(
                -100, -100, 300, 300, fill=self.MARKER_COLOR
            )
            self.__canvases_lst[int(str(text)[4 + i : 6 + i])].create_oval(
                10, 10, 70, 70, fill=player_color
            )

    def change_label(self):
        """
        method for changing the informative text that indicates which
        player's turn now
        """
        if self.__board.get_current_player() == self.__board.PLAYER_ONE:
            self.label["text"] = self.PLAYER_ONE_TURN_MSG
        if self.__board.get_current_player() == self.__board.PLAYER_TWO:
            self.label["text"] = self.PLAYER_TWO_TURN_MSG

    def create_oval(self, player, row, col):
        """
        this method inserting disk in the graphic board.
        :param player: int for which player did the last move.
        :param row: the number of the row to paint disk in
        :param col: the number of the column to paint disk in
        """
        if player == self.__board.PLAYER_ONE:
            self.__canvases_lst[row * 7 + col].create_oval(
                0, 0, 80, 80, fill=self.PLAYER_ONE_COLOR
            )
        elif player == self.__board.PLAYER_TWO:
            self.__canvases_lst[row * 7 + col].create_oval(
                0, 0, 80, 80, fill=self.PLAYER_TOW_COLOR
            )

    def create_coordinates_word(self, coordinates):
        """
        creating the coordinates word in the right format for marker_four
        :param coordinates: list of the fantastic four coordinates
        :return word: coordinates string
        """
        # this specific string ('NNNN') have no meaning. it is only part of
        # the adaptation for communication.
        word = "NNNN"
        for coord in coordinates:
            if len(str(coord)) < 2:
                word += "0"
            word += str(coord)
        return word


def check_arg(arg_list):
    """
    checking for the validation of args given in command line.
    :param arg_list:
    :return: True if args valid or False otherwise.
    """
    if len(arg_list) > MAX_NUM_OF_ARGS or len(arg_list) < MIN_NUM_OF_ARGS:
        print(ILL_PROG_ARGS)
        return False
    elif int(arg_list[PORT_LOCATION]) > MAX_PORT_VALUE or LOW_PORT_VALUE > int(
        arg_list[PORT_LOCATION]
    ):
        print(WRNG_PORT_MSG)
        return False
    elif (
        arg_list[PLAYER_TYPE_LOCATION] != "human"
        and arg_list[PLAYER_TYPE_LOCATION] != "ai"
    ):
        return False
    return True


def main(sys_argv):
    """
    reading from command line and running the game.
    :param sys_argv: args given in command line
    """
    # assigning the arguments from the command line
    if not check_arg(sys_argv):
        return
    player_type = sys_argv[PLAYER_TYPE_LOCATION]
    port = int(sys_argv[PORT_LOCATION])
    ip = None
    if MAX_NUM_OF_ARGS == len(sys_argv):
        ip = sys_argv[3]
    root = tki.Tk()
    if ip is None:
        MyBoard(root, port, player_type)
        root.title("Server")
    else:
        MyBoard(root, port, player_type, ip)
        root.title("Client")
    root.mainloop()


if __name__ == "__main__":
    main(sys.argv)
