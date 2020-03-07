# Author: Max Grier
# Date: 2/29/2020
# Description: Portfolio Project: This program contain code to play Chinese Chess (xiangqi).
# It will contain various functions that will hold the rules to each piece's move abilities
# and keep track of the game state throughout the game until it is finished.


class XiangqiGame:
    """
    This is the main class that contains the Chinese chess game.  It will have multiple functions
    to help it perform everything that is needed.
    """
    def __init__(self):
        """
        Set the board to it's default status, as well as set game state, players turn, if black is in check
        and if red is in check.
        """
        self._board = [['RCHA', 'RHOR', 'RELE', 'RADV', 'RGEN', 'RADV', 'RELE', 'RHOR', 'RCHA'],
                       ['    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    '],
                       ['    ', 'RCAN', '    ', '    ', '    ', '    ', '    ', 'RCAN', '    '],
                       ['RSOL', '    ', 'RSOL', '    ', 'RSOL', '    ', 'RSOL', '    ', 'RSOL'],
                       ['    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    '],
                       ['    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    '],
                       ['BSOL', '    ', 'BSOL', '    ', 'BSOL', '    ', 'BSOL', '    ', 'BSOL'],
                       ['    ', 'BCAN', '    ', '    ', '    ', '    ', '    ', 'BCAN', '    '],
                       ['    ', '    ', '    ', '    ', '    ', '    ', '    ', '    ', '    '],
                       ['BCHA', 'BHOR', 'BELE', 'BADV', 'BGEN', 'BADV', 'BELE', 'BHOR', 'BCHA']]
        self._game_state = "UNFINISHED"
        self._players_turn = "RED"
        self._black_in_check = False
        self._red_in_check = False

        # # Set the red general position.
        self._red_general_row = 0
        self._red_general_column = 4

        # # Set black general position.
        self._black_general_row = 9
        self._black_general_column = 4

    def print_board(self):
        """
        For testing, prints the game board.
        :return: nothing.
        """
        for row in self._board:
            print(row)

    def get_turn(self):
        """
        For testing purposes, prints whose turn it is.
        :return: nothing.
        """
        print(self._players_turn)

    def get_game_state(self):
        """
        Just returns the current game state.
        :return: current game state.
        """
        return self._game_state

    def is_in_check(self, player_color):
        """
        Takes the player's color as a parameter and returns true
        if they are in check or false if they are not.
        :param player_color: Which player.
        :return: True or False.
        """
        if player_color.lower() == "red":
            return self.red_general_in_check()
        elif player_color.lower() == "black":
            return self.black_general_in_check()

    def black_general_in_check(self):
        """
        This function will cycle through the pieces to determine if the general is in check.
        :return: True or False
        """
        is_general_in_check = False
        amount_pieces_can_check = 0
        pieces_can_check = []
        # Check if black general is in check
        for row in range(10):
            for column in range(9):
                if self._board[row][column] == "RCHA":
                    if self.chariot_move(row, column, self._black_general_row, self._black_general_column) is True:
                        amount_pieces_can_check += 1
                        pieces_can_check += "RCHA"
                        self._board[row][column] = "RCHA"
                        self._board[self._black_general_row][self._black_general_column] = "BGEN"
                if self._board[row][column] == "RHOR":
                    if self.horse_move(row, column, self._black_general_row, self._black_general_column) is True:
                        amount_pieces_can_check += 1
                        self._board[row][column] = "RHOR"
                        self._board[self._black_general_row][self._black_general_column] = "BGEN"
                if self._board[row][column] == "RCAN":
                    if self.cannon_move(row, column, self._black_general_row, self._black_general_column) is True:
                        amount_pieces_can_check += 1
                        self._board[row][column] = "RCAN"
                        self._board[self._black_general_row][self._black_general_column] = "BGEN"
                if self._board[row][column] == "RSOL":
                    if self.soldier_move(row, column, self._black_general_row, self._black_general_column) is True:
                        amount_pieces_can_check += 1
                        self._board[row][column] = "RSOL"
                        self._board[self._black_general_row][self._black_general_column] = "BGEN"
        if amount_pieces_can_check > 0:
            return True
        else:
            return False

    def red_general_in_check(self):
        """
        This function will cycle through the pieces to determine if the general is in check.
        :return: True or False
        """
        is_general_in_check = False
        amount_pieces_can_check = 0
        for row in range(10):
            for column in range(9):
                if self._board[row][column] == "BCHA":
                    if self.chariot_move(row, column, self._red_general_row, self._red_general_column) is True:
                        amount_pieces_can_check += 1
                        self._board[row][column] = "BCHA"
                        self._board[self._red_general_row][self._red_general_column] = "RGEN"
                if self._board[row][column] == "BHOR":
                    if self.horse_move(row, column, self._red_general_row, self._red_general_column) is True:
                        amount_pieces_can_check += 1
                        self._board[row][column] = "BHOR"
                        self._board[self._red_general_row][self._red_general_column] = "RGEN"
                if self._board[row][column] == "BCAN":
                    if self.cannon_move(row, column, self._red_general_row, self._red_general_column) is True:
                        amount_pieces_can_check += 1
                        self._board[row][column] = "BCAN"
                        self._board[self._red_general_row][self._red_general_column] = "RGEN"
                if self._board[row][column] == "BSOL":
                    if self.soldier_move(row, column, self._red_general_row, self._red_general_column) is True:
                        amount_pieces_can_check += 1
                        self._board[row][column] = "BSOL"
                        self._board[self._red_general_row][self._red_general_column] = "BGEN"
        if amount_pieces_can_check > 0:
            return True
        else:
            return False

    def checkmate(self):
        """
        This function will try all possible moves for the remaining pieces and then determine
        if there are any moves that can take the general out of check.
        :return: True or False
        """

    def make_move(self, move_from, move_to):
        """
        Will take the position to move from and to as parameters and make the move if it is legal.
        If it is not legal or the game is over, it will return false.
        :param move_from: The position to move from.
        :param move_to: The position to move to.
        :return: True of False.
        """
        move_completed = False
        move_from_column = None
        move_from_row = None
        move_to_column = None
        move_to_row = None
        column_values = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
        for key in column_values:
            if move_from[0].lower() == key:
                move_from_column = column_values[key]
        for key in column_values:
            if move_to[0].lower() == key:
                move_to_column = column_values[key]
        move_from_row = int(move_from[1:3]) - 1
        move_to_row = int(move_to[1:3]) - 1

        # Checks to see that the player's turn matches the piece being moved.
        if self._players_turn[0] != self._board[move_from_row][move_from_column][0]:
            return False

        # If the player is in check, see if they are in checkmate. *unfinished*
        if self._players_turn == "RED":
            if self._red_in_check is True:
                self.checkmate()

        # If the player is in check, see if they are in checkmate. *unfinished*
        if self._players_turn == "BLACK":
            if self._black_in_check is True:
                self.checkmate()

        # If the piece being moved is a general, it will call the general_move function.
        if self._board[move_from_row][move_from_column][1:4] == "GEN":
            self.general_move(move_from_row, move_from_column, move_to_row, move_to_column)
            move_completed = self.general_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an advisor, it will call the advisor_move function.
        if self._board[move_from_row][move_from_column][1:4] == "ADV":
            self.advisor_move(move_from_row, move_from_column, move_to_row, move_to_column)
            move_completed = self.advisor_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an elephant, it will call the elephant_move function.
        if self._board[move_from_row][move_from_column][1:4] == "ELE":
            self.elephant_move(move_from_row, move_from_column, move_to_row, move_to_column)
            move_completed = self.elephant_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is a horse, it will call the horse_move function.
        if self._board[move_from_row][move_from_column][1:4] == "HOR":
            self.horse_move(move_from_row, move_from_column, move_to_row, move_to_column)
            move_completed = self.horse_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an chariot, it will call the chariot_move function.
        if self._board[move_from_row][move_from_column][1:4] == "CHA":
            self.chariot_move(move_from_row, move_from_column, move_to_row, move_to_column)
            move_completed = self.chariot_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an cannon, it will call the cannon_move function.
        if self._board[move_from_row][move_from_column][1:4] == "CAN":
            self.cannon_move(move_from_row, move_from_column, move_to_row, move_to_column)
            move_completed = self.cannon_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an soldier, it will call the soldier_move function.
        if self._board[move_from_row][move_from_column][1:4] == "SOL":
            self.soldier_move(move_from_row, move_from_column, move_to_row, move_to_column)
            move_completed = self.soldier_move(move_from_row, move_from_column, move_to_row, move_to_column)

        return move_completed

        # if self.red_general_in_check() is True:
        #     self._red_in_check = True
        # if self.black_general_in_check() is True:
        #     self._black_in_check = True
        #return True

        # MAKE A SELF._MOVE_COMPLETED AND IF IT WAS COMPLETED AND THE GENERAL IS IN THE MOVE TO LOCATION
        # THEN MAKE THAT GENERAL IN CHECK.  THIS MIGHT ELIMINATE THE NEED FOR THE IN CHECK METHOD.
        # THEN WE JUST NEED THE IN CHECKMATE METHOD TO DETERMINE IF THERE IS ANY MOVE THAT CAN TAKE THE
        # GENEREAL OUT OF CHECK.



    # MAKE A FUNCTION TO CHECK IF THERE ARE PIECES THAT WILL BE ABLE TO TAKE THE GENERAL
    # AKA A MOVE THAT WOULD PUT THE GENERAL IN CHECK.
    # ALSO IF THE PLAYER IS IN CHECK THEY HAVE TO MOVE TO GET OUT OF CHECK OR THE LOSE.
    # MAKE A RULE THAT WON'T LET A PLAYER MOVE IF IT PUTS THE GENERAL IN CHECK (MAYBE MAKE A FUNCTION general_check? TO
        # SEE IF THE GENERAL IS IN CHECK AFTER THE MOVE.) - IF A GENERAL IS ACROSS THE WAY, IF A CANNON CAN GET HIM ETC.
        # OR MAKE A FUNCTION THAT SEES IF EACH PIECE CAN CHECK THE GENERAL IF A PIECE IS MOVED?

        # OR A CHECK FUNCTION THAT MAKES THE MOVE THEN CHECKS EVERY OPPOSING PIECE ON THE BOARD, IF ANY PIECE
        # CAN PUT THE GENERAL IN CHECK, THEN IT WILL UNDO THE MOVE AND RETURN FALSE.
        # MAKE ONE FOR EACH COLOR TO RUN TO CHECK IF A RED MOVE LETS THE BLACK CHECK THE GENERAL AND VISA VERSA.
        # SOMEHOW MAKE A CHECK MATE FUNCTION THAT CHECKS IF NO MOVES CAN BE MADE BY ONE TEAM WITHOUT HAVING THE
        # OTHER TEAM CHECK YOUR GENERAL. THEN SET THE GAME TO WON****
        # Hmm, only now do I realize that "checkmate" and "stalemate" are the same thing, "player X has no allowable moves"
        # If player X has no available moves and IS in check == checkmate
        # if player X has no available moves and IS NOT in check == stalemate

    # NEED TO CHANGE IS IN CHECK AT THE END OF EACH MOVE IF THAT PIECES NEXT MOVE OR OTHER PIECES NEXT MOVE
    # PUTS THE KING IN CHECK.

    def general_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Makes the rules for the general's move.
        :param move_from_row:
        :param move_from_column:
        :param move_to_row:
        :param move_to_column:
        :return:
        """
        # Makes sure the column move isn't greater than one space.
        if abs(move_to_column - move_from_column) > 1:
            return False
        # Makes sure the row move isn't greater than one space.
        if abs(move_to_row - move_from_row) > 1:
            return False
        # Makes sure the move is within the palace.
        if move_from_column < 3 or move_from_column > 6:
            return False
        # Makes sure the move is within the palace.
        if move_to_column < 3 or move_to_column > 6:
            return False
        # Makes sure the move is within the palace.
        if self._board[move_from_row][move_from_column] == "BGEN":
            if move_to_row < 7:
                return False
        # Makes sure the move is within the palace.
        if self._board[move_from_row][move_from_column] == "RGEN":
            if move_to_row > 2:
                return False
        # Check if it is a general piece
        if self._board[move_from_row][move_from_column][1:4] != "GEN":
            return False
        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column] == "BGEN" and \
                self._board[move_to_row][move_to_column][0] == "B":
            return False
        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column] == "RGEN" and \
                self._board[move_to_row][move_to_column][0] == "R":
            return False
        # Make sure the general doesn't move diagonally.
        if move_to_column != move_from_column:
            if move_to_row != move_from_row:
                return False
        # Makes sure there is a piece between the two generals in the new position.
        piece_in_between = True
        if self._board[move_from_row][move_from_column] == "RGEN":
            if move_to_column == self._black_general_column:
                piece_in_between = False
                row = move_to_row + 1
                while row < self._black_general_row:
                    if self._board[row][move_to_column] != "    ":
                        piece_in_between = True
                    row += 1
        # Makes sure there is a piece between the two generals in the new position.
        if self._board[move_from_row][move_from_column] == "BGEN":
            if move_to_column == self._red_general_column:
                piece_in_between = False
                row = move_to_row - 1
                while row > self._red_general_row:
                    if self._board[row][move_to_column] != "    ":
                        piece_in_between = True
                    row -= 1
        if piece_in_between is True:
            if self._board[move_from_row][move_from_column] == "BGEN":
                self._black_general_row = move_to_row
                self._black_general_column = move_to_column
                self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
                self._board[move_from_row][move_from_column] = "    "
                self._players_turn = "RED"
                return True
            if self._board[move_from_row][move_from_column] == "RGEN":
                self._red_general_row = move_to_row
                self._red_general_column = move_to_column
                self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
                self._board[move_from_row][move_from_column] = "    "
                self._players_turn = "BLACK"
                return True

    def advisor_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Controls the moves for an advisor piece.
        :param move_from_row:
        :param move_from_column:
        :param move_to_row:
        :param move_to_column:
        :return:
        """
        # Makes sure the column move isn't greater than one space.
        if abs(move_to_column - move_from_column) > 1:
            return False
        # Makes sure the row move isn't greater than one space.
        if abs(move_to_row - move_from_row) > 1:
            return False
        # Makes sure it is diagonal move.
        if move_to_column == move_from_column:
            return False
        # Makes sure the move is within the palace.
        if move_from_column < 3 or move_from_column > 6:
            return False
        # Makes sure the move is within the palace.
        if move_to_column < 3 or move_to_column > 6:
            return False
        # Makes sure the move is within the palace.
        if self._board[move_from_row][move_from_column] == "BADV":
            if move_to_row < 7:
                return False
        # Makes sure the move is within the palace.
        if self._board[move_from_row][move_from_column] == "RADV":
            if move_to_row > 2:
                return False
        if self._board[move_from_row][move_from_column][1:4] != "ADV":
            return False
        # Makes sure the move to space is empty.
        if self._board[move_to_row][move_to_column] != "    ":
            return False
        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column] == "BADV" and \
                self._board[move_to_row][move_to_column][0] == "B":
            return False
        # Make sure there isn't a similar color piece in the way
        print("move to", self._board[move_to_row][move_to_column])
        if self._board[move_from_row][move_from_column] == "RADV" and \
                self._board[move_to_row][move_to_column][0] == "R":
            return False
        else:
            self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
            self._board[move_from_row][move_from_column] = "    "
            if self._players_turn == "RED":
                self._players_turn = "BLACK"
            elif self._players_turn == "BLACK":
                self._players_turn = "RED"
            return True

    def elephant_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Creates a function for the elephants' move.
        :param move_from_row:
        :param move_from_column:
        :param move_to_row:
        :param move_to_column:
        :return:
        """
        # Checks that the move is no more than two squares.
        if abs(move_to_column - move_from_column) != 2:
            return False
        if abs(move_to_row - move_from_row) != 2:
            return False
        if move_to_column - move_from_column > 1:
            if move_to_row - move_from_row > 1:
                if self._board[move_from_row + 1][move_from_column + 1] != "    ":
                    return False
        if move_to_column - move_from_column < 1:
            if move_to_row - move_from_row < 1:
                if self._board[move_from_row - 1][move_from_column - 1] != "    ":
                    return False
        if move_to_column - move_from_column > 1:
            if move_to_row - move_from_row < 1:
                if self._board[move_from_row - 1][move_from_column + 1] != "    ":
                    return False
        if move_to_column - move_from_column < 1:
            if move_to_row - move_from_row < 1:
                if self._board[move_from_row - 1][move_from_column - 1] != "    ":
                    return False
        # Make it so the elephants can't cross the river.
        if self._board[move_from_row][move_from_column][0] == "R":
            if move_to_row > 5:
                return False
        if self._board[move_from_row][move_from_column][0] == "B":
            if move_to_row < 6:
                return False
        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column][0] == "B" and \
                self._board[move_to_row][move_to_column][0] == "B":
            return False
        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column][0] == "R" and \
                self._board[move_to_row][move_to_column][0] == "R":
            return False
        # Else.
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        if self._players_turn == "RED":
            self._players_turn = "BLACK"
        elif self._players_turn == "BLACK":
            self._players_turn = "RED"
        return True

    def horse_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Creates the function for the horses' move.
        :param move_from_row:
        :param move_from_column:
        :param move_to_row:
        :param move_to_column:
        :return:
        """
        # Checks that the move is no more than two squares.
        if abs(move_to_column - move_from_column) > 2:
            return False
        if abs(move_to_row - move_from_row) > 2:
            return False
        if move_to_row == move_from_row:
            return False
        if move_from_column == move_to_column:
            return False
        if abs(move_to_column - move_from_column) < 2:
            if abs(move_to_row - move_from_row) < 2:
                return False
        if abs(move_to_row - move_from_row) < 2:
            if abs(move_to_column - move_from_column) < 2:
                return False
        # Checks to see if a piece is blocking the horse
        if move_to_column - move_from_column > 0:
            if move_to_row - move_from_row > 1:
                if self._board[move_from_row + 1][move_from_column] != "    ":
                    return False
        if move_to_column - move_from_column < 1:
            if move_to_row - move_from_row < 1:
                if self._board[move_from_row - 1][move_from_column] != "    ":
                    return False
                # elif self._board[move_from_row][move_from_column - 1] != "    ":
                #     return False
        if move_to_column - move_from_column > 0:
            if move_to_row - move_from_row < 1:
                if self._board[move_from_row - 1][move_from_column] != "    ":
                    return False
        if move_to_column - move_from_column < 1:
            if move_to_row - move_from_row > 1:
                if self._board[move_from_row + 1][move_from_column] != "    ":
                    return False
        # if there is a piece to the left.
        if move_to_column - move_from_column == -2:
            if self._board[move_from_row][move_from_column - 1] != "    ":
                return False
        if move_to_column - move_from_column == 2:
            if self._board[move_from_row][move_from_column + 1] != "    ":
                return False
        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column][0] == "B" and \
                self._board[move_to_row][move_to_column][0] == "B":
            return False
        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column][0] == "R" and \
                self._board[move_to_row][move_to_column][0] == "R":
            return False
        # Else.
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        if self._players_turn == "RED":
            self._players_turn = "BLACK"
        elif self._players_turn == "BLACK":
            self._players_turn = "RED"
        return True

    def chariot_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Creates the function for the chariots' move.
        :param move_from_row:
        :param move_from_column:
        :param move_to_row:
        :param move_to_column:
        :return:
        """
        # Makes sure the chariot is moving along the same row or column.
        if move_to_column != move_from_column:
            if move_to_row != move_from_row:
                return False
        if move_to_row != move_from_row:
            if move_to_column != move_from_column:
                return False
        if abs(move_to_column - move_from_column) > 8:
            return False
        if abs(move_to_row - move_from_row) > 9:
            return False
        # Makes sure there are no pieces in the way when moving.
        if self._board[move_from_row][move_from_column][0] == "R":
            if move_to_row - move_from_row > 0:
                row_distance = move_to_row - move_from_row
                for row in range(move_from_row + 1, move_to_row + 1):
                    if self._board[row][move_from_column][0] == "R":
                        return False
            if move_to_row - move_from_row < 0:
                row_distance = move_to_row - move_from_row
                for row in range(move_from_row - 1, move_to_row - 1, -1):
                    if self._board[row][move_from_column][0] == "R":
                        return False
            if move_to_column - move_from_column > 0:
                column_distance = move_to_column - move_from_column
                for column in range(move_from_column + 1, move_to_column + 1):
                    if self._board[move_from_row][column][0] == "R":
                        return False
            if move_to_column - move_from_column < 1:
                column_distance = move_to_column - move_from_column
                for column in range(move_from_column - 1, move_to_column - 1, -1):
                    if self._board[move_from_row][column][0] == "R":
                        return False
        if self._board[move_from_row][move_from_column][0] == "B":
            if move_to_row - move_from_row > 1:
                row_distance = move_to_row - move_from_row
                for row in range(move_from_row + 1, move_to_row + 1):
                    if self._board[row][move_from_column][0] == "B":
                        return False
            if move_to_row - move_from_row < 0:
                row_distance = move_to_row - move_from_row
                for row in range(move_from_row - 1, move_to_row - 1, -1):
                    if self._board[row][move_from_column][0] == "B":
                        return False
            if move_to_column - move_from_column > 0:
                column_distance = move_to_column - move_from_column
                for column in range(move_from_column + 1, move_to_column + 1):
                    if self._board[move_from_row][column][0] == "B":
                        return False
            if move_to_column - move_from_column < 1:
                column_distance = move_to_column - move_from_column
                for column in range(move_from_column - 1, move_to_column - 1, -1):
                    if self._board[move_from_row][column][0] == "B":
                        return False
        # Else.
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        if self._players_turn == "RED":
            self._players_turn = "BLACK"
        elif self._players_turn == "BLACK":
            self._players_turn = "RED"
        return True

    def cannon_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Creates the function for the cannons' move.
        :param move_from_row:
        :param move_from_column:
        :param move_to_row:
        :param move_to_column:
        :return:
        """
        piece_count = 0
        # Makes sure the cannon is moving along the same row or column.
        if move_to_column != move_from_column:
            if move_to_row != move_from_row:
                return False
        if move_to_row != move_from_row:
            if move_to_column != move_from_column:
                return False
        if abs(move_to_column - move_from_column) > 8:
            return False
        if abs(move_to_row - move_from_row) > 9:
            return False
        # Checks if there is a piece in between to allow a capture.
        if self._board[move_from_row][move_from_column][0] == "R":
            if self._board[move_to_row][move_to_column][0] == "B":
                piece_count = 0
                if move_to_row - move_from_row > 0:
                    for row in range(move_from_row + 1, move_to_row):
                        if self._board[row][move_from_column] != "    ":
                            piece_count += 1
                if move_to_row - move_from_row < 0:
                    for row in range(move_from_row - 1, move_to_row - 1, -1):
                        if self._board[row][move_from_column] != "    ":
                            piece_count += 1
                if move_to_column - move_from_column > 0:
                    for column in range(move_from_column + 1, move_to_column + 1):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if move_to_column - move_from_column < 1:
                    for column in range(move_from_column - 1, move_to_column - 1, -1):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if piece_count == 1:
                    self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
                    self._board[move_from_row][move_from_column] = "    "
                    if self._players_turn == "RED":
                        self._players_turn = "BLACK"
                    elif self._players_turn == "BLACK":
                        self._players_turn = "RED"
                    return True
                else:
                    return False
        # Checks if there is a piece in between to allow a capture.
        if self._board[move_from_row][move_from_column][0] == "B":
            if self._board[move_to_row][move_to_column][0] == "R":
                piece_count = 0
                if move_to_row - move_from_row > 0:
                    for row in range(move_from_row + 1, move_to_row + 1):
                        if self._board[row][move_from_column] != "    ":
                            piece_count += 1
                if move_to_row - move_from_row < 0:
                    for row in range(move_from_row - 1, move_to_row, -1):
                        if self._board[row][move_from_column] != "    ":
                            piece_count += 1
                if move_to_column - move_from_column > 0:
                    for column in range(move_from_column + 1, move_to_column + 1):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if move_to_column - move_from_column < 1:
                    for column in range(move_from_column - 1, move_to_column - 1, -1):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if piece_count == 1:
                    self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
                    self._board[move_from_row][move_from_column] = "    "
                    if self._players_turn == "RED":
                        self._players_turn = "BLACK"
                    elif self._players_turn == "BLACK":
                        self._players_turn = "RED"
                    return True
                else:
                    return False
        # Makes sure there are no pieces in the way when moving.
        if self._board[move_from_row][move_from_column][0] == "R":
            if move_to_row - move_from_row > 0:
                row_distance = move_to_row - move_from_row
                for row in range(move_from_row + 1, move_to_row + 1):
                    if self._board[row][move_from_column][0] == "R":
                        return False
            if move_to_row - move_from_row < 0:
                row_distance = move_to_row - move_from_row
                for row in range(move_from_row - 1, row_distance + 1, -1):
                    if self._board[row][move_from_column][0] == "R":
                        return False
            if move_to_column - move_from_column > 0:
                column_distance = move_to_column - move_from_column
                for column in range(move_from_column + 1, move_to_column + 1):
                    if self._board[move_from_row][column][0] == "R":
                        return False
            if move_to_column - move_from_column < 1:
                column_distance = move_to_column - move_from_column
                for column in range(move_from_column - 1, move_to_column - 1, -1):
                    if self._board[move_from_row][column][0] == "R":
                        return False
        if self._board[move_from_row][move_from_column][0] == "B":
            if move_to_row - move_from_row > 1:
                row_distance = move_to_row - move_from_row
                for row in range(move_from_row + 1, move_to_row + 1):
                    if self._board[row][move_from_column][0] == "B":
                        return False
            if move_to_row - move_from_row < 0:
                row_distance = move_to_row - move_from_row
                for row in range(move_from_row - 1, move_to_row, -1):
                    if self._board[row][move_from_column][0] == "B":
                        return False
            if move_to_column - move_from_column > 0:
                column_distance = move_to_column - move_from_column
                for column in range(move_from_column + 1, move_to_column + 1):
                    if self._board[move_from_row][column][0] == "B":
                        return False
            if move_to_column - move_from_column < 1:
                column_distance = move_to_column - move_from_column
                for column in range(move_from_column - 1, move_to_column - 1, -1):
                    if self._board[move_from_row][column][0] == "B":
                        return False
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        if self._players_turn == "RED":
            self._players_turn = "BLACK"
        elif self._players_turn == "BLACK":
            self._players_turn = "RED"
        return True

    def soldier_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Creates the function for the soldiers' move.
        :param move_from_row:
        :param move_from_column:
        :param move_to_row:
        :param move_to_column:
        :return:
        """
        # Makes sure the column move isn't greater than one space.
        if abs(move_to_column - move_from_column) > 1:
            return False
        # Makes sure the row move isn't greater than one space.
        if abs(move_to_row - move_from_row) > 1:
            return False
        # Makes rules for red soldiers.
        if self._board[move_from_row][move_from_column][0] == "R":
            # Makes sure the soldier does not retreat.
            if move_to_row < move_from_row:
                return False
            # If the soldier has not crossed the river, it cannot move horizontally.
            if move_from_row < 5:
                if abs(move_from_column - move_to_column) > 0:
                    return False
            # Doesn't allow to hit own piece.
            if self._board[move_to_row][move_to_column][0] == "R":
                return False
        # Makes rules for black soldiers.
        if self._board[move_from_row][move_from_column][0] == "B":
            # Makes sure the soldier does not retreat.
            if move_to_row > move_from_row:
                return False
            # If the soldier has not crossed the river, it cannot move horizontally.
            if move_from_row < 4:
                if abs(move_from_column - move_to_column) > 0:
                    return False
            # Doesn't allow to hit own piece.
            if self._board[move_to_row][move_to_column][0] == "B":
                return False
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        if self._players_turn == "RED":
            self._players_turn = "BLACK"
        elif self._players_turn == "BLACK":
            self._players_turn = "RED"
        return True


# game = XiangqiGame()
# game.print_board()
# print(game.get_game_state())
# # game.print_board()
# print(game.is_in_check("REd"))
# print(game.is_in_check("black"))
# print(game.is_in_check("RE"))
# word = "b1"
# print(word[1:3])
# game.make_move("b5", "c10")
# game.print_board()
# print()
# game.make_move("e1", "e2")
# game.make_move("e2", "f2")
# game.make_move("e10", "e9")
# game.make_move("e9", "f9")
# game.make_move("e9", "d9")
# game.make_move("d10", "e9")
# game.make_move("e10", "D10")
# game.make_move("d10", "e9")
# game.print_board()
# game.get_turn()
# game.make_move("f1", "e2")
# game.get_turn()
#game.make_move("e10", "e9")
# game.make_move("f10", "e9")


# Soldier moves
# game.make_move("e4", "e5")
# print()
# game.print_board()
# game.make_move("e7", "e6")
# print()
# game.print_board()
# game.get_turn()
# game.make_move("e5", "e6")
# print()
# game.print_board()
# game.make_move("a7", "a6")
# print()
# game.print_board()
# game.make_move("e6", "f6")
# print()
# game.print_board()
# game.make_move("a6", "a5")
# print()
# game.print_board()
# game.make_move("a6", "a5")
# print()
# game.print_board()
# game.make_move("f6", "g6")
# print()
# game.print_board()
# game.make_move("a5", "a4")
# print()
# game.print_board()

# test elephant moves
# game.make_move("c1", "a3")
# print()
# game.print_board()
#
# game.make_move("c10", "a8")
# print()
# game.print_board()
#
# game.make_move("a3", "c5")
# print()
# game.print_board()
#
# game.make_move("a8", "c6")
# print()
# game.print_board()
#
# game.make_move("c5", "a7")
# print()
# game.print_board()

# Horse stuff
# game.make_move("b1", "c3")
# # print()
# # game.print_board()
#
# game.make_move("b10", "a8")
# print()
# game.print_board()
#
# game.make_move("c3", "e2")
# print()
# game.print_board()
#
# game.make_move("a8", "b10")
# print()
# game.print_board()


# game = XiangqiGame()
# move_result = game.make_move('c1', 'e3')
# black_in_check = game.is_in_check('black')
# game.make_move('e7', 'e6')
# state = print(game.get_game_state())

# Chariot moves
# game.make_move("a1", "a2")
# print()
# game.print_board()
#
# game.make_move("a10", "a9")
# print()
# game.print_board()
#
# game.make_move("a2", "g2")
# print()
# game.print_board()
#
# game.make_move("a9", "a8")
# print()
# game.print_board()
#
# game.make_move("g2", "g1")
# print()
# game.print_board()

# Cannon moves
# game.make_move("b3", "b10")
# print()
# game.print_board()
#
# game.make_move("h8", "h1")
# print()
# game.print_board()
#
# game.make_move("e5", "e10")
# print()
# game.print_board()

# game.make_move("e8", "e9")
# print()
# game.print_board()

# print(game.is_in_check("black"))
# print()
# game.print_board()

# game = XiangqiGame()
# move_result = game.make_move('c1', 'e3')
# print(move_result)
# black_in_check = game.is_in_check('black')
# print(game.make_move('e7', 'e6'))
# state = game.get_game_state()
#
# game.print_board()