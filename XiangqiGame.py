# Author: Max Grier
# Date: 3/12/2020
# Description: Portfolio Project: This program contain code to play Chinese Chess (xiangqi).
# It will contain various functions that will hold the rules to each piece's move abilities
# and keep track of the game state throughout the game until it is finished.
# It will be able to check if a player is in check or checkmate and who the winner is.


# Making a deepcopy function since we cannot import it.
def my_deepcopy(item_to_copy):
    new_copied_item = []
    if isinstance(item_to_copy, list):
        for lst in item_to_copy:
            sub_list = []
            for item in lst:
                sub_list.append(item)
            new_copied_item.append(sub_list)
    else:
        new_copied_item = item_to_copy
    return new_copied_item


class XiangqiGame:
    """
    This is the main class that contains the Chinese chess game.
    It will have multiple functions to help it perform everything that is needed.
    This will include all of the needed moves per piece as well as
    methods to see if generals are in check and checkmate.
    """
    def __init__(self):
        """
        Set the board to it's default status, as well as set game state,
        players turn, if black is in check and if red is in check.
        """

        # Set the initial board with it's pieces.
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

        # Sets the initial game stat, payer's turn, that neither black nor red are in check.
        self._game_state = "UNFINISHED"
        self._players_turn = "RED"
        self._black_in_check = False
        self._red_in_check = False

        # Set red general position.
        self._red_general_row = self.find_red_general_row()
        self._red_general_column = self.find_red_general_column()

        # Set black general position.
        self._black_general_row = self.find_black_general_row()
        self._black_general_column = self.find_black_general_column()

    def find_red_general_row(self):
        """
        Summary: This locates the red general's row position.
        :return: Red general's row position.
        """
        for row in range(10):
            for column in range(9):
                if self._board[row][column] == "RGEN":
                    self._red_general_row = row
        return self._red_general_row

    def find_red_general_column(self):
        """
        Summary: This locates the red general's column position.
        :return: Red general's column position.
        """
        for row in range(10):
            for column in range(9):
                if self._board[row][column] == "RGEN":
                    self._red_general_column = column
        return self._red_general_column

    def find_black_general_row(self):
        """
        Summary: This locates the black general's row position.
        :return: Black general's row position.
        """
        for row in range(10):
            for column in range(9):
                if self._board[row][column] == "BGEN":
                    self._black_general_row = row
        return self._black_general_row

    def find_black_general_column(self):
        """
        Summary: This locates the black general's column position.
        :return: Black general's column position.
        """
        for row in range(10):
            for column in range(9):
                if self._board[row][column] == "BGEN":
                    self._black_general_column = column
        return self._black_general_column

    def print_board(self):
        """
        For testing, prints the game board.
        :return: nothing.
        """
        row_number = 1
        print("  ", "A", "      ", "B", "     ", "C", "     ", "D", "     ", "E", "     ",
              "F", "     ", "G", "    ", "H", "     ", "I")
        for row in self._board:
            print(row, row_number)
            row_number += 1

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
        if self._players_turn == "RED":
            if self.red_checkmate() is True:
                self._game_state = "BLACK_WON"
            else:
                self._game_state = "UNFINISHED"

        if self._players_turn == "BLACK":
            if self.black_checkmate() is True:
                self._game_state = "RED_WON"
            else:
                self._game_state = "UNFINISHED"

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
        players_turn_before = my_deepcopy(self._players_turn)
        is_general_in_check = False
        amount_pieces_can_check = 0
        board_before = my_deepcopy(self._board)

        # Checks each row and then each column to see if any piece can check the opposing general.
        for row in range(10):
            for column in range(9):
                if self._board[row][column] == "RCHA":
                    if self.chariot_move(row, column, self._black_general_row, self._black_general_column) is True:
                        amount_pieces_can_check += 1
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

        # Sets the turn back to the original player after checking the moves.
        self._players_turn = players_turn_before

        # If players can check, set to true.
        if amount_pieces_can_check > 0:
            return True
        else:
            return False

    def red_general_in_check(self):
        """
        This function will cycle through the pieces to determine if the general is in check.
        :return: True or False
        """
        players_turn_before = my_deepcopy(self._players_turn)
        is_general_in_check = False
        amount_pieces_can_check = 0

        # Checks each row and then each column to see if any piece can check the opposing general.
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

        # Sets the turn back to the original player after checking the moves.
        self._players_turn = players_turn_before

        # If a piece can check, return true.
        if amount_pieces_can_check > 0:
            return True
        else:
            return False

    def black_checkmate(self):
        """
        This function will try all possible moves for the remaining pieces and then determine
        if there are any moves that can take the general out of check.
        :return: True or False
        """

        # Set copies of the player's turn, board, and general position prior to checking conditions.
        players_turn_before = my_deepcopy(self._players_turn)
        board_before = my_deepcopy(self._board)
        general_row_before = my_deepcopy(self._black_general_row)
        general_column_before = my_deepcopy(self._black_general_column)
        checkmate = True

        # Cycles through every row and column to check if any piece's move will take to general out of check.
        for row in range(10):
            for column in range(9):

                # If we find a piece in a cell, we run that piece's move. If that stops the general from
                # being in check, then we set checkmate to False, set the board back to how it was and
                # eventually return checkmate.
                if self._board[row][column] == "BGEN":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.general_move(row, column, row_position, column_position) is True:
                                self._black_general_row = row_position
                                self._black_general_column = column_position
                                if self.black_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                                self._black_general_row = general_row_before
                                self._black_general_column = general_column_before
                if self._board[row][column] == "BADV":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.advisor_move(row, column, row_position, column_position) is True:
                                if self.black_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "BELE":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.elephant_move(row, column, row_position, column_position) is True:
                                if self.black_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "BHOR":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.horse_move(row, column, row_position, column_position) is True:
                                if self.black_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "BCHA":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.chariot_move(row, column, row_position, column_position) is True:
                                if self.black_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "BCAN":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.cannon_move(row, column, row_position, column_position) is True:
                                if self.black_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "BSOL":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.soldier_move(row, column, row_position, column_position) is True:
                                if self.black_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
        self._players_turn = players_turn_before
        return checkmate

    def red_checkmate(self):
        """
        This function will try all possible moves for the remaining pieces and then determine
        if there are any moves that can take the general out of check.
        :return: True or False
        """

        # Set copies of the player's turn, board, and general position prior to checking conditions.
        players_turn_before = my_deepcopy(self._players_turn)
        board_before = my_deepcopy(self._board)
        general_row_before = my_deepcopy(self._red_general_row)
        general_column_before = my_deepcopy(self._red_general_column)
        self.red_general_in_check()
        checkmate = True

        # Cycles through every row and column to check if any piece's move will take to general out of check.
        for row in range(10):
            for column in range(9):

                # If we find a piece in a cell, we run that piece's move for every
                # possible move it can make. If that stops the general from being in check,
                # then we set checkmate to False, set the board back to how it was,
                # and eventually return checkmate.
                if self._board[row][column] == "RGEN":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.general_move(row, column, row_position, column_position) is True:
                                self._red_general_row = row_position
                                self._red_general_column = column_position
                                if self.red_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                                self._red_general_row = general_row_before
                                self._red_general_column = general_column_before
                if self._board[row][column] == "RADV":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.advisor_move(row, column, row_position, column_position) is True:
                                if self.red_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "RELE":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.elephant_move(row, column, row_position, column_position) is True:
                                if self.red_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "RHOR":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.horse_move(row, column, row_position, column_position) is True:
                                if self.red_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "RCHA":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.chariot_move(row, column, row_position, column_position) is True:
                                if self.red_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "RCAN":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.cannon_move(row, column, row_position, column_position) is True:
                                if self.red_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
                if self._board[row][column] == "RSOL":
                    for row_position in range(10):
                        for column_position in range(9):
                            if self.soldier_move(row, column, row_position, column_position) is True:
                                if self.red_general_in_check() is False:
                                    checkmate = False
                                self._board = my_deepcopy(board_before)
        self._players_turn = players_turn_before
        return checkmate

    def make_move(self, move_from, move_to):
        """
        Will take the position to move from and to as parameters and make the move if it is legal.
        If it is not legal or the game is over, it will return false.
        :param move_from: The position to move from.
        :param move_to: The position to move to.
        :return: True of False.
        """

        # Set the initial move conditions.
        move_completed = False
        move_from_column = None
        move_from_row = None
        move_to_column = None
        move_to_row = None

        # Converts the alphanumeric parameters into row and column numbers.
        column_values = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
        # Finds the column number.
        for key in column_values:
            if move_from[0].lower() == key:
                move_from_column = column_values[key]
        for key in column_values:
            if move_to[0].lower() == key:
                move_to_column = column_values[key]
        # Finds the row number.
        move_from_row = int(move_from[1:3]) - 1
        move_to_row = int(move_to[1:3]) - 1

        # Creates a copy of the pieces in the to and from positions before anything happens.
        spot_before_move = my_deepcopy(self._board[move_from_row][move_from_column])
        spot_after_move = my_deepcopy(self._board[move_to_row][move_to_column])

        # If the same color piece is in the move_to spot, returns False.
        if self._board[move_from_row][move_from_column][0] == self._board[move_to_row][move_to_column][0]:
            return False

        # Checks to see that the player's turn matches the piece being moved.
        if self._players_turn[0] != self._board[move_from_row][move_from_column][0]:
            return False

        # If the black general is in checkmate, return False.
        if self._board[move_from_row][move_from_column] == "BGEN":
            if self.black_checkmate() is True:
                return False

        # If the red general is in checkmate, return False.
        if self._board[move_from_row][move_from_column] == "RGEN":
            if self.red_checkmate() is True:
                return False

        # If the piece being moved is a general, it will call the general_move function.
        if self._board[move_from_row][move_from_column][1:4] == "GEN":
            move_completed = self.general_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an advisor, it will call the advisor_move function.
        if self._board[move_from_row][move_from_column][1:4] == "ADV":
            move_completed = self.advisor_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an elephant, it will call the elephant_move function.
        if self._board[move_from_row][move_from_column][1:4] == "ELE":
            move_completed = self.elephant_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is a horse, it will call the horse_move function.
        if self._board[move_from_row][move_from_column][1:4] == "HOR":
            move_completed = self.horse_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an chariot, it will call the chariot_move function.
        if self._board[move_from_row][move_from_column][1:4] == "CHA":
            move_completed = self.chariot_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an cannon, it will call the cannon_move function.
        if self._board[move_from_row][move_from_column][1:4] == "CAN":
            move_completed = self.cannon_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the piece being moved is an soldier, it will call the soldier_move function.
        if self._board[move_from_row][move_from_column][1:4] == "SOL":
            move_completed = self.soldier_move(move_from_row, move_from_column, move_to_row, move_to_column)

        # If the move was successful, but the move put the general in check, it will undo
        # the move and return False. Otherwise, complete move and change the player's turn.
        if move_completed is True:
            if spot_before_move[0] == "R":
                if self.red_general_in_check() is True:
                    self._board[move_to_row][move_to_column] = spot_after_move
                    self._board[move_from_row][move_from_column] = spot_before_move
                    move_completed = False
                else:
                    self._players_turn = "BLACK"
            elif spot_before_move[0] == "B":
                if self.black_general_in_check() is True:
                    self._board[move_to_row][move_to_column] = spot_after_move
                    self._board[move_from_row][move_from_column] = spot_before_move
                    move_completed = False
                else:
                    self._players_turn = "RED"

        # If it is a player's turn, but they are in checkmate, we change the game_state accordingly.
        if self._players_turn == "RED":
            if self.red_checkmate() is True:
                self._game_state = "BLACK_WON"
            else:
                self._game_state = "UNFINISHED"

        # If it is a player's turn, but they are in checkmate, we change the game_state accordingly.
        if self._players_turn == "BLACK":
            if self.black_checkmate() is True:
                self._game_state = "RED_WON"
            else:
                self._game_state = "UNFINISHED"

        return move_completed

    def general_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Makes the rules for the general's move, based on the Chinese Chess rules.
        :param move_from_row: Row index of the from row.
        :param move_from_column: Column index of the from column.
        :param move_to_row: Row index of the to row.
        :param move_to_column: Column index of the to column.
        :return: True or False based on if the move was valid.
        """

        # Makes sure the column move isn't greater than one space.
        if abs(move_to_column - move_from_column) > 1:
            return False
        # Makes sure the row move isn't greater than one space.
        if abs(move_to_row - move_from_row) > 1:
            return False

        # Makes sure the move is within the palace.
        if move_from_column < 3 or move_from_column > 5:
            return False
        # Makes sure the move is within the palace.
        if move_to_column < 3 or move_to_column > 5:
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

        # If there is a piece between the generals and it is a legal move, make the move.
        if piece_in_between is True:
            if self._board[move_from_row][move_from_column] == "BGEN":
                self._black_general_row = move_to_row
                self._black_general_column = move_to_column
                self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
                self._board[move_from_row][move_from_column] = "    "
                return True
            if self._board[move_from_row][move_from_column] == "RGEN":
                self._red_general_row = move_to_row
                self._red_general_column = move_to_column
                self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
                self._board[move_from_row][move_from_column] = "    "
                return True

    def advisor_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Makes the rules for the advisor's move, based on the Chinese Chess rules.
        :param move_from_row: Row index of the from row.
        :param move_from_column: Column index of the from column.
        :param move_to_row: Row index of the to row.
        :param move_to_column: Column index of the to column.
        :return: True or False based on if the move was valid.
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

        # Make sure it is an advisor piece.
        if self._board[move_from_row][move_from_column][1:4] != "ADV":
            return False

        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column] == "BADV" and \
                self._board[move_to_row][move_to_column][0] == "B":
            return False
        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column] == "RADV" and \
                self._board[move_to_row][move_to_column][0] == "R":
            return False
        else:
            self._board[move_to_row][move_to_column] = my_deepcopy(self._board[move_from_row][move_from_column])
            self._board[move_from_row][move_from_column] = "    "
            return True

    def elephant_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Makes the rules for the elephant's move, based on the Chinese Chess rules.
        :param move_from_row: Row index of the from row.
        :param move_from_column: Column index of the from column.
        :param move_to_row: Row index of the to row.
        :param move_to_column: Column index of the to column.
        :return: True or False based on if the move was valid.
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
            if move_to_row < 5:
                return False

        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column][0] == "B" and \
                self._board[move_to_row][move_to_column][0] == "B":
            return False
        # Make sure there isn't a similar color piece in the way
        if self._board[move_from_row][move_from_column][0] == "R" and \
                self._board[move_to_row][move_to_column][0] == "R":
            return False

        # If it passes the conditions, make the move
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        return True

    def horse_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Makes the rules for the horse's move, based on the Chinese Chess rules.
        :param move_from_row: Row index of the from row.
        :param move_from_column: Column index of the from column.
        :param move_to_row: Row index of the to row.
        :param move_to_column: Column index of the to column.
        :return: True or False based on if the move was valid.
        """

        # Checks that the move is no more than two squares.
        if abs(move_to_column - move_from_column) > 2:
            return False
        if abs(move_to_row - move_from_row) > 2:
            return False

        # Make sure the move is an not straight.
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
                if abs(move_to_row - move_from_row) == 2:
                    if self._board[move_from_row + 1][move_from_column] != "    ":
                        return False
                if abs(move_to_column - move_to_column) == 2:
                    if self._board[move_from_row][move_from_column + 1] != "    ":
                        return False
        if move_to_column - move_from_column < 1:
            if move_to_row - move_from_row < 1:
                if move_from_column - move_to_column == 2:
                    if self._board[move_from_row][move_from_column - 1] != "    ":
                        return False
                if move_from_row - move_to_row == 2:
                    if self._board[move_from_row - 1][move_from_column] != "    ":
                        return False
        if move_to_column - move_from_column > 0:
            if move_to_row - move_from_row < 1:
                if abs(move_from_column - move_to_column) == 2:
                    if self._board[move_from_row][move_from_column + 1] != "    ":
                        return False
                if abs(move_from_row - move_to_row) == 2:
                    if self._board[move_from_row - 1][move_from_column] != "    ":
                        return False
        if move_to_column - move_from_column < 1:
            if move_to_row - move_from_row > 1:
                if abs(move_from_row - move_to_row) == 2:
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
        # If it passes the conditions, make the move.
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        return True

    def chariot_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Makes the rules for the chariot's move, based on the Chinese Chess rules.
        :param move_from_row: Row index of the from row.
        :param move_from_column: Column index of the from column.
        :param move_to_row: Row index of the to row.
        :param move_to_column: Column index of the to column.
        :return: True or False based on if the move was valid.
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
                for row in range(move_from_row + 1, move_to_row + 1):
                    if self._board[row][move_from_column][0] == "R":
                        return False
            if move_to_row - move_from_row < 0:
                for row in range(move_from_row - 1, move_to_row - 1, -1):
                    if self._board[row][move_from_column][0] == "R":
                        return False
            if move_to_column - move_from_column > 0:
                for column in range(move_from_column + 1, move_to_column + 1):
                    if self._board[move_from_row][column][0] == "R":
                        return False
            if move_to_column - move_from_column < 1:
                for column in range(move_from_column - 1, move_to_column - 1, -1):
                    if self._board[move_from_row][column][0] == "R":
                        return False

        # Makes sure there are no pieces in the way when moving.
        if self._board[move_from_row][move_from_column][0] == "B":
            if move_to_row - move_from_row > 1:
                for row in range(move_from_row + 1, move_to_row + 1):
                    if self._board[row][move_from_column][0] == "B":
                        return False
            if move_to_row - move_from_row < 0:
                for row in range(move_from_row - 1, move_to_row - 1, -1):
                    if self._board[row][move_from_column][0] == "B":
                        return False
            if move_to_column - move_from_column > 0:
                for column in range(move_from_column + 1, move_to_column + 1):
                    if self._board[move_from_row][column][0] == "B":
                        return False
            if move_to_column - move_from_column < 1:
                for column in range(move_from_column - 1, move_to_column - 1, -1):
                    if self._board[move_from_row][column][0] == "B":
                        return False

        # Checks if there is a piece in between to block the chariot.
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
                    for column in range(move_from_column + 1, move_to_column):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if move_to_column - move_from_column < 1:
                    for column in range(move_from_column - 1, move_to_column, -1):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if piece_count > 0:
                    return False

        # Checks if there is a piece in between to block the chariot.
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
                    for column in range(move_from_column + 1, move_to_column):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if move_to_column - move_from_column < 1:
                    for column in range(move_from_column - 1, move_to_column, -1):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if piece_count > 0:
                    return False

        # If it passes all of the conditions, make the move.
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        return True

    def cannon_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Makes the rules for the cannon's move, based on the Chinese Chess rules.
        :param move_from_row: Row index of the from row.
        :param move_from_column: Column index of the from column.
        :param move_to_row: Row index of the to row.
        :param move_to_column: Column index of the to column.
        :return: True or False based on if the move was valid.
        """

        # Makes sure the cannon is moving along the same row or column.
        if move_to_column != move_from_column:
            if move_to_row != move_from_row:
                return False
        if move_to_row != move_from_row:
            if move_to_column != move_from_column:
                return False

        # Make sure the move is within range of the board.
        if abs(move_to_column - move_from_column) > 8:
            return False
        if abs(move_to_row - move_from_row) > 9:
            return False

        # Set piece count to 0 (for attacking).
        piece_count = 0
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
                    for column in range(move_from_column + 1, move_to_column):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if move_to_column - move_from_column < 1:
                    for column in range(move_from_column - 1, move_to_column, -1):
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
                    for column in range(move_from_column + 1, move_to_column):
                        if self._board[move_from_row][column] != "    ":
                            piece_count += 1
                if move_to_column - move_from_column < 1:
                    for column in range(move_from_column - 1, move_to_column, -1):
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
                for row in range(move_from_row + 1, move_to_row + 1):
                    if self._board[row][move_from_column] != "    ":
                        return False
            if move_to_row - move_from_row < 0:
                for row in range(move_from_row - 1, move_to_row + 1, -1):
                    if self._board[row][move_from_column] != "    ":
                        return False
            if move_to_column - move_from_column > 0:
                for column in range(move_from_column + 1, move_to_column + 1):
                    if self._board[move_from_row][column] != "    ":
                        return False
            if move_to_column - move_from_column < 1:
                for column in range(move_from_column - 1, move_to_column - 1, -1):
                    if self._board[move_from_row][column] != "    ":
                        return False
        if self._board[move_from_row][move_from_column][0] == "B":
            if move_to_row - move_from_row > 1:
                for row in range(move_from_row + 1, move_to_row + 1):
                    if self._board[row][move_from_column] != "    ":
                        return False
            if move_to_row - move_from_row < 0:
                for row in range(move_from_row - 1, move_to_row, -1):
                    if self._board[row][move_from_column] != "    ":
                        return False
            if move_to_column - move_from_column > 0:
                for column in range(move_from_column + 1, move_to_column + 1):
                    if self._board[move_from_row][column] != "    ":
                        return False
            if move_to_column - move_from_column < 1:
                for column in range(move_from_column - 1, move_to_column - 1, -1):
                    if self._board[move_from_row][column] != "    ":
                        return False

        # If it passes all the conditions, make the move.
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        return True

    def soldier_move(self, move_from_row, move_from_column, move_to_row, move_to_column):
        """
        Makes the rules for the soldier's move, based on the Chinese Chess rules.
        :param move_from_row: Row index of the from row.
        :param move_from_column: Column index of the from column.
        :param move_to_row: Row index of the to row.
        :param move_to_column: Column index of the to column.
        :return: True or False based on if the move was valid.
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

        # If it passes the conditions, make the move.
        self._board[move_to_row][move_to_column] = self._board[move_from_row][move_from_column]
        self._board[move_from_row][move_from_column] = "    "
        return True
