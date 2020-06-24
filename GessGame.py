# author: Jing Wang
# data 5/17/2020
# description: a game simulator for the Gess game

class GessGame:
    """
    Class that allows players to play Gess.
    It includes change player, make move, movement validation, resign, game state"""

    def __init__(self):
        """Creates GessGame
        Initializes game data members. """
        self._game_state = "UNFINISHED"
        self._current_player = 'black'
        self._board = Board()

    def update_turn(self):
        """Sets turns"""
        if self._current_player == 'black':
            self._current_player = 'white'
        else:
            self._current_player = 'black'

    def get_game_state(self):
        """Returns the status of the game
        returns 'UNFINISHED', 'BLACK_WON' or 'WHITE_WON'"""
        return self._game_state

    def get_player(self):
        """Returns current player"""
        return self._current_player

    def game_result_validation(self):
        """Returns current game status"""

        black_ring_count, black_ring_index = self._board.black_last_ring_pos()
        white_ring_count, white_ring_index = self._board.white_last_ring_pos()

        if black_ring_count == 0:
            self._game_state = 'WHITE_WON'
        elif white_ring_count == 0:
            self._game_state = 'BLACK_WON'

        return self._game_state

    def resign_game(self):
        """
        lets the current player concede the game, giving the other player the win
        :return:the opponent's win
        """
        current_player = self.get_player()

        if current_player == 'black':
            self._game_state = 'WHITE_WON'

        elif current_player == 'white':
            self._game_state = 'BLACK_WON'

        return self._game_state

    def check_square(self, from_pos):
        """
        Returns False if this square has opponent pieces. True if otherwise
        a piece is not valid if it has stone of both colors in it
        """
        current_player = self.get_player()

        pos_list = self._board.footprint(from_pos)
        if current_player == 'black':

            for pos in pos_list:
                if self._board._board[pos[0]][pos[1]] == 'w':
                    return False  # This is not a piece because there are stones of both colors in it.
            return True

        if current_player == 'white':

            for pos in pos_list:
                if self._board._board[pos[0]][pos[1]] == 'b':
                    return False  # This is not a piece because there are stones of both colors in it.
            return True

    def check_piece_at_center(self, from_pos):
        """
        Determines if the piece this player wants to move there is a stone at 'C'
        :return True if there is a stone at 'C'; False if otherwise
        """
        current_player = self.get_player()
        from_pos_index = self._board.get_location(from_pos)

        # when player is from the black side:
        if current_player == 'black':
            if self._board._board[from_pos_index[0]][from_pos_index[1]] == 'b':
                return True
            else:
                return False
        # when player is from the white side:
        if current_player == 'white':
            if self._board._board[from_pos_index[0]][from_pos_index[1]] == 'w':
                return True
            else:
                return False

    def check_piece_at_center_direction(self, from_pos):
        """
        :param from_pos: strings that represent the center square of the piece being moved
        :return: return direction list if there is a piece at the direction of player wants to move to
        return False if there is only a piece at center but no piece in any other direction of the footprint,
        that means a player can not make a move

        if there is a stone at 'C' in center, this 'piece' can move any unobstructed distance.
        this 'piece' can move any unobstructed distance diagonally or upper or lower position
        """

        if not self.check_square(from_pos):
            return False

        # an empty list to store directions
        direction_list = []

        from_index = self._board.get_location(from_pos)
        pos_list = self._board.footprint(from_pos)

        for pos in pos_list:

            row_diff = pos[0] - from_index[0]
            col_diff = pos[1] - from_index[1]
            # # validate if there is a piece at the direction this player wants to move to
            # # store to direction list if a piece is presented
            if (self._board._board[pos[0]][pos[1]] == 'w') or (self._board._board[pos[0]][pos[1]] == 'b'):
                direction_list.append([row_diff, col_diff])

        # if the direction list only contains the center piece, return False
        if (len(direction_list) == 1 and (direction_list[0][0] == 0 and direction_list[0][1] == 0)) or len(
                direction_list) == 0:
            return False
        else:
            return direction_list

    def no_piece_at_center_direction(self, from_pos, to_pos):
        """
        :param from_pos: strings that represent the center square of the piece being moved
        :param to_pos: strings that represent the desired new location of the center square
        :return: return direction list if there is a piece at the direction of player wants to move to
        return False if there is direction list is empty,that means a player can not make a move
        check if there is a stone at 'C' in center. If there is a stone at 'C',
        This 'piece' can move up to 3 squares.
        return False if a player wants to move more than up to 3 squares
        """

        if not self.check_square(from_pos):
            return False

        # an empty list to store directions
        direction_list = []

        from_index = self._board.get_location(from_pos)  # get board index of the player move from
        to_index = self._board.get_location(to_pos)  # get board index of the player move to
        pos_list = self._board.footprint(from_pos)  # get board index of the entire footprint of move from

        # calculate the difference between move to position and move from position
        row_difference = to_index[0] - from_index[0]
        col_difference = to_index[1] - from_index[1]

        # validate if the move is only up to 3 squares
        # if yes return the direction list
        # else return False
        if abs(row_difference) <= 3 and abs(col_difference) <= 3:

            for pos in pos_list:

                row_diff = pos[0] - from_index[0]
                col_diff = pos[1] - from_index[1]

                # validate if there is a piece at the direction this player wants to move to
                # store the piece to the direction list if a piece is presented
                if self._board._board[pos[0]][pos[1]] == 'w' or self._board._board[pos[0]][pos[1]] == 'b':
                    direction_list.append([row_diff, col_diff])

            if len(direction_list) == 0:
                return False
            else:
                return direction_list

        else:
            return False

    def make_move(self, from_pos, to_pos):
        """
        :param from_pos: strings that represent the center square of the piece being moved
        :param to_pos: strings that represent the desired new location of the center square
        :return: return True if move is successful, and updates game state, turn, and board.
        return False if move unsuccessful.
        """
        from_index = self._board.get_location(from_pos)
        to_index = self._make_move(from_pos, to_pos)

        if from_index and to_index:
            # tempepory store the from_to square
            new_upper_left = self._board._board[from_index[0] - 1][from_index[1] - 1]
            new_left = self._board._board[from_index[0]][from_index[1] - 1]
            new_lower_left = self._board._board[from_index[0] + 1][from_index[1] - 1]
            new_upper = self._board._board[from_index[0] - 1][from_index[1]]
            new_lower = self._board._board[from_index[0] + 1][from_index[1]]
            new_upper_right = self._board._board[from_index[0] - 1][from_index[1] + 1]
            new_right = self._board._board[from_index[0]][from_index[1] + 1]
            new_lower_right = self._board._board[from_index[0] + 1][from_index[1] + 1]
            new_center = self._board._board[from_index[0]][from_index[1]]

            # clear board and remove current square
            self._board.clear_pos(from_pos)

            # move current square to move_to position
            self._board._board[to_index[0] - 1][to_index[1] - 1] = new_upper_left
            self._board._board[to_index[0]][to_index[1] - 1] = new_left
            self._board._board[to_index[0] + 1][to_index[1] - 1] = new_lower_left
            self._board._board[to_index[0] - 1][to_index[1]] = new_upper
            self._board._board[to_index[0] + 1][to_index[1]] = new_lower
            self._board._board[to_index[0] - 1][to_index[1] + 1] = new_upper_right
            self._board._board[to_index[0]][to_index[1] + 1] = new_right
            self._board._board[to_index[0] + 1][to_index[1] + 1] = new_lower_right
            self._board._board[to_index[0]][to_index[1]] = new_center

            # check if there is piece on the border of the board and clean it
            self._board.clear_border_pieces()

            # update game_state
            self._game_state = self.game_result_validation()
            # print(self._game_state)
            # change turns
            self.update_turn()
            # current_player = self.get_player()
            # print("Next player:", current_player)
            return True
            # return self._board.board_display()
        # else:
        #     current_player = self.get_player()
        #     # print("Next player:", current_player)
        #     return False

    def _make_move(self, from_pos, to_pos):
        """
        :param from_pos: strings that represent the center square of the piece being moved
        :param to_pos: strings that represent the desired new location of the center square
        If game has already been won, return False;
        If a player's next move to will break it's own last ring, return False;
        If a player's move from will break it's own last ring, return False;
        If a player picks a piece that contains it's opponent's piece, return False;
        If a player's next move is out of range, return False;
        If a player's move from position is out of range, return False'
        Otherwise it should make the move, remove any pieces that fall outside of the board
        :return return the legal movement that a player can make
        """
        current_player = self.get_player()
        # print("Current player:", current_player)

        game_state = self.get_game_state()

        if game_state != 'UNFINISHED':  # if the game has already been won, return False
            return False

        if from_pos == to_pos:
            return False

        if not self._board.check_move_from_ring_black(from_pos, current_player):
            return False

        if not self._board.check_move_from_ring_white(from_pos, current_player):
            return False

        if not self._board.check_move_to_ring_black(from_pos, to_pos, current_player):
            return False

        if not self._board.check_move_to_ring_white(from_pos, to_pos, current_player):
            return False

        # check if from_pos is in range: 18x18 board. Can only continue if it's in range
        if not self._board.check_current_position_valid(from_pos):
            return False

        # check if to_pos is in range: 18x18 board. Can only continue if it's in range
        if not self._board.check_move_position_valid(to_pos):
            return False

        # check if this square has opponent pieces
        if not self.check_square(from_pos):
            return False

        # if there is a piece at the center of the square, make the following move
        if self.check_piece_at_center(from_pos):

            direction_list = self.check_piece_at_center_direction(from_pos)

            if not direction_list:
                return False

            # determine the direction a player wants to move to and validate that move
            for index in direction_list:

                if self.SW_direction(from_pos, to_pos) == index:
                    return self.check_stone_SW(from_pos, to_pos)

                elif self.NE_direction(from_pos, to_pos) == index:
                    return self.check_stone_NE(from_pos, to_pos)

                elif self.NW_direction(from_pos, to_pos) == index:
                    return self.check_stone_NW(from_pos, to_pos)

                elif self.SE_direction(from_pos, to_pos) == index:
                    return self.check_stone_SE(from_pos, to_pos)

                elif self.E_direction(from_pos, to_pos) == index:
                    return self.check_stone_E(from_pos, to_pos)

                elif self.W_direction(from_pos, to_pos) == index:
                    return self.check_stone_W(from_pos, to_pos)

                elif self.N_direction(from_pos, to_pos) == index:
                    return self.check_stone_N(from_pos, to_pos)

                elif self.S_direction(from_pos, to_pos) == index:
                    return self.check_stone_S(from_pos, to_pos)

        else:
            # if no piece at the center of this square, make the following piece
            direction_list = self.no_piece_at_center_direction(from_pos, to_pos)

            if not direction_list:
                return False

            for index in direction_list:

                if self.SW_direction(from_pos, to_pos) == index:
                    return self.check_stone_SW(from_pos, to_pos)

                elif self.NE_direction(from_pos, to_pos) == index:
                    return self.check_stone_NE(from_pos, to_pos)

                elif self.NW_direction(from_pos, to_pos) == index:
                    return self.check_stone_NW(from_pos, to_pos)

                elif self.SE_direction(from_pos, to_pos) == index:
                    return self.check_stone_SE(from_pos, to_pos)

                elif self.E_direction(from_pos, to_pos) == index:
                    return self.check_stone_E(from_pos, to_pos)

                elif self.W_direction(from_pos, to_pos) == index:
                    return self.check_stone_W(from_pos, to_pos)

                elif self.N_direction(from_pos, to_pos) == index:
                    to_index = self.check_stone_N(from_pos, to_pos)
                    return to_index

                elif self.S_direction(from_pos, to_pos) == index:
                    return self.check_stone_S(from_pos, to_pos)

    def check_stone_SW(self, from_pos, to_pos):
        """
        Check if there is block piece on the SW direction for both players
        :return: return the legal move_to index for a player
        """
        current_player = self.get_player()

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]  # difference is positive
        col_diff = to_index[1] - from_index[1]  # difference is negative

        if row_diff == 0 or col_diff == 0:
            return False

        row_diff_abs = int((to_index[0] - from_index[0]) / abs(to_index[0] - from_index[0]))
        col_diff_abs = int((to_index[1] - from_index[1]) / abs(to_index[1] - from_index[1]))

        if [row_diff_abs, col_diff_abs] != [1, -1]:
            return False

        if current_player == 'black':

            # i representing the direction of SW: [1, -1]
            for i in range(1, abs(row_diff)):
                new_upper_left = self._board._board[i + from_index[0] - 1][-i + from_index[1] - 1]
                new_left = self._board._board[i + from_index[0]][-i + from_index[1] - 1]
                new_lower_left = self._board._board[i + from_index[0] + 1][-i + from_index[1] - 1]
                new_lower = self._board._board[i + from_index[0] + 1][-i + from_index[1]]
                new_lower_right = self._board._board[i + from_index[0] + 1][-i + from_index[1] + 1]

                if new_upper_left == 'b' or new_left == 'b' or new_lower_left == 'b' or new_lower == 'b' or new_lower_right == 'b':
                    to_index[0] = i + from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

                elif new_upper_left == 'w' or new_left == 'w' or new_lower_left == 'w' or new_lower == 'w' or new_lower_right == 'w':
                    to_index[0] = i + from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

        elif current_player == 'white':

            for i in range(1, abs(row_diff)):

                new_upper_left = self._board._board[i + from_index[0] - 1][-i + from_index[1] - 1]
                new_left = self._board._board[i + from_index[0]][-i + from_index[1] - 1]
                new_lower_left = self._board._board[i + from_index[0] + 1][-i + from_index[1] - 1]
                new_lower = self._board._board[i + from_index[0] + 1][-i + from_index[1]]
                new_lower_right = self._board._board[i + from_index[0] + 1][-i + from_index[1] + 1]

                if new_upper_left == 'b' or new_left == 'b' or new_lower_left == 'b' or new_lower == 'b' or new_lower_right == 'b':
                    to_index[0] = i + from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

                elif new_upper_left == 'w' or new_left == 'w' or new_lower_left == 'w' or new_lower == 'w' or new_lower_right == 'w':
                    to_index[0] = i + from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

        return to_index

    def check_stone_NE(self, from_pos, to_pos):
        """
        Check if there is block piece on the NE direction for both players
        :return: return the legal move_to index for a player
        """
        current_player = self.get_player()

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]  # difference is negative
        col_diff = to_index[1] - from_index[1]  # difference is positive

        if row_diff == 0 or col_diff == 0:
            return False

        row_diff_abs = int((to_index[0] - from_index[0]) / abs(to_index[0] - from_index[0]))
        col_diff_abs = int((to_index[1] - from_index[1]) / abs(to_index[1] - from_index[1]))

        if [row_diff_abs, col_diff_abs] != [-1, 1]:
            return False

        if current_player == 'black':
            # i representing the direction of NE: [-1, 1]
            for i in range(1, abs(row_diff)):
                new_upper_left = self._board._board[-i + from_index[0] - 1][i + from_index[1] - 1]
                new_upper = self._board._board[-i + from_index[0] - 1][i + from_index[1]]
                new_upper_right = self._board._board[-i + from_index[0] - 1][i + from_index[1] + 1]
                new_right = self._board._board[-i + from_index[0]][i + from_index[1] + 1]
                new_lower_right = self._board._board[-i + from_index[0] + 1][i + from_index[1] + 1]

                if new_upper_left == 'w' or new_upper == 'w' or new_upper_right == 'w' or new_right == 'w' or new_lower_right == 'w':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

                elif new_upper_left == 'b' or new_upper == 'b' or new_upper_right == 'b' or new_right == 'b' or new_lower_right == 'b':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

        elif current_player == 'white':
            for i in range(1, abs(row_diff)):
                new_upper_left = self._board._board[-i + from_index[0] - 1][i + from_index[1] - 1]
                new_upper = self._board._board[-i + from_index[0] - 1][i + from_index[1]]
                new_upper_right = self._board._board[-i + from_index[0] - 1][i + from_index[1] + 1]
                new_right = self._board._board[-i + from_index[0]][i + from_index[1] + 1]
                new_lower_right = self._board._board[-i + from_index[0] + 1][i + from_index[1] + 1]

                if new_upper_left == 'w' or new_upper == 'w' or new_upper_right == 'w' or new_right == 'w' or new_lower_right == 'w':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

                elif new_upper_left == 'b' or new_upper == 'b' or new_upper_right == 'b' or new_right == 'b' or new_lower_right == 'b':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

        return to_index

    def check_stone_SE(self, from_pos, to_pos):
        """
        Check if there is block piece on the SE direction for both players
        :return: return the legal move_to index for a player
        """
        current_player = self.get_player()

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]  # difference is positive
        col_diff = to_index[1] - from_index[1]  # difference is positive

        if row_diff == 0 or col_diff == 0:
            return False

        row_diff_abs = int((to_index[0] - from_index[0]) / abs(to_index[0] - from_index[0]))
        col_diff_abs = int((to_index[1] - from_index[1]) / abs(to_index[1] - from_index[1]))

        if [row_diff_abs, col_diff_abs] != [1, 1]:
            return False

        if current_player == 'black':
            # i representing the direction of SE: [1, 1]
            for i in range(1, abs(row_diff)):
                new_lower_left = self._board._board[i + from_index[0] + 1][i + from_index[1] - 1]
                new_lower = self._board._board[i + from_index[0] + 1][i + from_index[1]]
                new_upper_right = self._board._board[i + from_index[0] - 1][i + from_index[1] + 1]
                new_right = self._board._board[i + from_index[0]][i + from_index[1] + 1]
                new_lower_right = self._board._board[i + from_index[0] + 1][i + from_index[1] + 1]

                if new_upper_right == 'w' or new_right == 'w' or new_lower_right == 'w' or new_lower == 'w' or new_lower_left == 'w':
                    to_index[0] = i + from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

                elif new_upper_right == 'b' or new_right == 'b' or new_lower_right == 'b' or new_lower == 'b' or new_lower_left == 'b':
                    to_index[0] = i + from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

        elif current_player == 'white':
            for i in range(1, abs(row_diff)):
                new_lower_left = self._board._board[i + from_index[0] + 1][i + from_index[1] - 1]
                new_lower = self._board._board[i + from_index[0] + 1][i + from_index[1]]
                new_upper_right = self._board._board[i + from_index[0] - 1][i + from_index[1] + 1]
                new_right = self._board._board[i + from_index[0]][i + from_index[1] + 1]
                new_lower_right = self._board._board[i + from_index[0] + 1][i + from_index[1] + 1]

                if new_upper_right == 'w' or new_right == 'w' or new_lower_right == 'w' or new_lower == 'w' or new_lower_left == 'w':
                    to_index[0] = i + from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

                elif new_upper_right == 'b' or new_right == 'b' or new_lower_right == 'b' or new_lower == 'b' or new_lower_left == 'b':
                    to_index[0] = i + from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

        return to_index

    def check_stone_NW(self, from_pos, to_pos):
        """
        Check if there is block piece on the NW direction for both players
        :return: return the legal move_to index for a player
        """
        current_player = self.get_player()

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]  # difference is negative
        col_diff = to_index[1] - from_index[1]  # difference is negative

        if row_diff == 0 or col_diff == 0:
            return False

        row_diff_abs = int((to_index[0] - from_index[0]) / abs(to_index[0] - from_index[0]))
        col_diff_abs = int((to_index[1] - from_index[1]) / abs(to_index[1] - from_index[1]))

        if [row_diff_abs, col_diff_abs] != [-1, -1]:
            return False

        if current_player == 'black':
            # i representing the direction of NW: [-1, -1]
            for i in range(1, abs(row_diff)):
                new_upper_left = self._board._board[-i + from_index[0] - 1][-i + from_index[1] - 1]
                new_left = self._board._board[-i + from_index[0]][-i + from_index[1] - 1]
                new_lower_left = self._board._board[-i + from_index[0] + 1][-i + from_index[1] - 1]
                new_upper = self._board._board[-i + from_index[0] - 1][-i + from_index[1]]
                new_upper_right = self._board._board[-i + from_index[0] - 1][-i + from_index[1] + 1]

                if new_upper_left == 'w' or new_left == 'w' or new_lower_left == 'w' or new_upper == 'w' or new_upper_right == 'w':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

                elif new_upper_left == 'b' or new_left == 'b' or new_lower_left == 'b' or new_upper == 'b' or new_upper_right == 'b':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

        elif current_player == 'white':
            for i in range(1, abs(row_diff)):
                new_upper_left = self._board._board[-i + from_index[0] - 1][-i + from_index[1] - 1]
                new_left = self._board._board[-i + from_index[0]][-i + from_index[1] - 1]
                new_lower_left = self._board._board[-i + from_index[0] + 1][-i + from_index[1] - 1]
                new_upper = self._board._board[-i + from_index[0] - 1][-i + from_index[1]]
                new_upper_right = self._board._board[-i + from_index[0] - 1][-i + from_index[1] + 1]

                if new_upper_left == 'w' or new_left == 'w' or new_lower_left == 'w' or new_upper == 'w' or new_upper_right == 'w':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

                elif new_upper_left == 'b' or new_left == 'b' or new_lower_left == 'b' or new_upper == 'b' or new_upper_right == 'b':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

        return to_index

    def check_stone_W(self, from_pos, to_pos):
        """
        Check if there is block piece on the W direction for both players
        :return: return the legal move_to index for a player
        """
        current_player = self.get_player()

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]  # difference is 0
        col_diff = to_index[1] - from_index[1]  # difference is negative

        col_diff_abs = int((col_diff) / abs(col_diff))

        if [row_diff, col_diff_abs] != [0, -1]:
            return False

        if current_player == 'black':
            # i representing the direction of W: [0, -1]
            for i in range(1, abs(col_diff)):
                new_upper_left = self._board._board[from_index[0] - 1][-i + from_index[1] - 1]
                new_left = self._board._board[from_index[0]][-i + from_index[1] - 1]
                new_lower_left = self._board._board[from_index[0] + 1][-i + from_index[1] - 1]

                if new_upper_left == 'w' or new_left == 'w' or new_lower_left == 'w':
                    to_index[0] = from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

                elif new_upper_left == 'w' or new_left == 'w' or new_lower_left == 'w':
                    to_index[0] = from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

        elif current_player == 'white':
            for i in range(1, abs(col_diff)):
                new_upper_left = self._board._board[from_index[0] - 1][-i + from_index[1] - 1]
                new_left = self._board._board[from_index[0]][-i + from_index[1] - 1]
                new_lower_left = self._board._board[from_index[0] + 1][-i + from_index[1] - 1]

                if new_upper_left == 'w' or new_left == 'w' or new_lower_left == 'w':
                    to_index[0] = from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

                elif new_upper_left == 'w' or new_left == 'w' or new_lower_left == 'w':
                    to_index[0] = from_index[0]
                    to_index[1] = -i + from_index[1]

                    return to_index

        return to_index

    def check_stone_E(self, from_pos, to_pos):
        """
        Check if there is block piece on the E direction for both players
        :return: return the legal move_to index for a player
        """
        current_player = self.get_player()

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]  # difference is 0
        col_diff = to_index[1] - from_index[1]  # difference is positive

        col_diff_abs = int((col_diff) / abs(col_diff))

        if [row_diff, col_diff_abs] != [0, 1]:
            return False

        if current_player == 'black':
            # i representing the direction of E: [0, 1]
            for i in range(1, abs(col_diff)):
                new_upper_right = self._board._board[from_index[0] - 1][i + from_index[1] + 1]
                new_right = self._board._board[from_index[0]][i + from_index[1] + 1]
                new_lower_right = self._board._board[from_index[0] + 1][i + from_index[1] + 1]

                if new_upper_right == 'w' or new_right == 'w' or new_lower_right == 'w':
                    to_index[0] = from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

                elif new_upper_right == 'b' or new_right == 'b' or new_lower_right == 'b':
                    to_index[0] = from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

        elif current_player == 'white':
            for i in range(1, abs(col_diff)):
                new_upper_right = self._board._board[from_index[0] - 1][i + from_index[1] + 1]
                new_right = self._board._board[from_index[0]][i + from_index[1] + 1]
                new_lower_right = self._board._board[from_index[0] + 1][i + from_index[1] + 1]

                if new_upper_right == 'w' or new_right == 'w' or new_lower_right == 'w':
                    to_index[0] = from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

                elif new_upper_right == 'b' or new_right == 'b' or new_lower_right == 'b':
                    to_index[0] = from_index[0]
                    to_index[1] = i + from_index[1]

                    return to_index

        return to_index

    def check_stone_N(self, from_pos, to_pos):
        """
        Check if there is block piece on the N direction for both players
        :return: return the legal move_to index for a player
        """
        current_player = self.get_player()

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]  # difference is negative
        col_diff = to_index[1] - from_index[1]  # difference is 0

        row_diff_abs = int((row_diff) / abs(row_diff))

        if [row_diff_abs, col_diff] != [-1, 0]:
            return False

        if current_player == 'black':
            # i representing the direction of N: [-1, 0]
            for i in range(1, abs(row_diff)):
                new_upper_left = self._board._board[-i + from_index[0] - 1][from_index[1] - 1]
                new_upper = self._board._board[-i + from_index[0] - 1][from_index[1]]
                new_upper_right = self._board._board[-i + from_index[0] - 1][from_index[1] + 1]

                if new_upper_right == 'w' or new_upper == 'w' or new_upper_left == 'w':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = from_index[1]

                    return to_index

                elif new_upper_right == 'b' or new_upper == 'b' or new_upper_left == 'b':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = from_index[1]

                    return to_index

        if current_player == 'white':
            for i in range(1, abs(row_diff)):
                new_upper_left = self._board._board[-i + from_index[0] - 1][from_index[1] - 1]
                new_upper = self._board._board[-i + from_index[0] - 1][from_index[1]]
                new_upper_right = self._board._board[-i + from_index[0] - 1][from_index[1] + 1]

                if new_upper_right == 'w' or new_upper == 'w' or new_upper_left == 'w':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = from_index[1]

                elif new_upper_right == 'b' or new_upper == 'b' or new_upper_left == 'b':
                    to_index[0] = -i + from_index[0]
                    to_index[1] = from_index[1]

                    return to_index

        return to_index

    def check_stone_S(self, from_pos, to_pos):
        """
        Check if there is block piece on the S direction for both players
        :return: return the legal move_to index for a player
        """
        current_player = self.get_player()

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]  # difference is positive
        col_diff = to_index[1] - from_index[1]  # difference is 0

        row_diff_abs = int((row_diff) / abs(row_diff))

        if [row_diff_abs, col_diff] != [1, 0]:
            return False

        if current_player == 'black':
            # i representing the direction of S: [1, 0]
            for i in range(1, abs(row_diff)):
                new_lower_left = self._board._board[i + from_index[0] + 1][from_index[1] - 1]
                new_lower = self._board._board[i + from_index[0] + 1][from_index[1]]
                new_lower_right = self._board._board[i + from_index[0] + 1][from_index[1] + 1]

                if new_lower_right == 'w' or new_lower == 'w' or new_lower_left == 'w':
                    to_index[0] = i + from_index[0]
                    to_index[1] = from_index[1]

                    return to_index

                elif new_lower_right == 'b' or new_lower == 'b' or new_lower_left == 'b':
                    to_index[0] = i + from_index[0]
                    to_index[1] = from_index[1]

                    return to_index

        elif current_player == 'white':
            for i in range(1, abs(row_diff)):

                new_lower_left = self._board._board[i + from_index[0] + 1][from_index[1] - 1]
                new_lower = self._board._board[i + from_index[0] + 1][from_index[1]]
                new_lower_right = self._board._board[i + from_index[0] + 1][from_index[1] + 1]

                if new_lower_right == 'w' or new_lower == 'w' or new_lower_left == 'w':
                    to_index[0] = i + from_index[0]
                    to_index[1] = from_index[1]

                elif new_lower_right == 'b' or new_lower == 'b' or new_lower_left == 'b':
                    to_index[0] = i + from_index[0]
                    to_index[1] = from_index[1]

                    return to_index

        return to_index

    def SW_direction(self, from_pos, to_pos):
        """
        Returns the direction a player wants to move to"""

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]  # difference is positive
        col_diff = to_index[1] - from_index[1]  # difference is 0

        if row_diff != 0 and col_diff != 0:

            row_diff_abs = int((row_diff) / abs(row_diff))
            col_diff_abs = int((col_diff) / abs(col_diff))

            if [row_diff_abs, col_diff_abs] == [1, -1]:
                return [1, -1]

    def NW_direction(self, from_pos, to_pos):
        """
        Returns the direction a player wants to move to"""

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]
        col_diff = to_index[1] - from_index[1]

        if row_diff != 0 and col_diff != 0:

            row_diff_abs = int((row_diff) / abs(row_diff))
            col_diff_abs = int((col_diff) / abs(col_diff))

            if [row_diff_abs, col_diff_abs] == [-1, -1]:
                return [-1, -1]

    def NE_direction(self, from_pos, to_pos):
        """
        Returns the direction a player wants to move to"""

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]
        col_diff = to_index[1] - from_index[1]

        if row_diff != 0 and col_diff != 0:
            row_diff_abs = int((row_diff) / abs(row_diff))
            col_diff_abs = int((col_diff) / abs(col_diff))

            if [row_diff_abs, col_diff_abs] == [-1, 1]:
                return [-1, 1]

    def SE_direction(self, from_pos, to_pos):
        """
        Returns the direction a player wants to move to"""

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]
        col_diff = to_index[1] - from_index[1]

        if row_diff != 0 and col_diff != 0:

            row_diff_abs = int((row_diff) / abs(row_diff))
            col_diff_abs = int((col_diff) / abs(col_diff))

            if [row_diff_abs, col_diff_abs] == [1, 1]:
                return [1, 1]

    def N_direction(self, from_pos, to_pos):
        """
        Returns the direction a player wants to move to"""

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]
        col_diff = to_index[1] - from_index[1]

        row_diff_abs = int((row_diff) / max(abs(row_diff), abs(col_diff)))

        if [row_diff_abs, col_diff] == [-1, 0]:
            return [-1, 0]

    def S_direction(self, from_pos, to_pos):
        """
        Returns the direction a player wants to move to"""

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]
        col_diff = to_index[1] - from_index[1]

        row_diff_abs = int((row_diff) / max(abs(row_diff), abs(col_diff)))

        if [row_diff_abs, col_diff] == [1, 0]:
            return [1, 0]

    def W_direction(self, from_pos, to_pos):
        """
        Returns the direction a player wants to move to"""

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]
        col_diff = to_index[1] - from_index[1]

        col_diff_abs = int((col_diff) / max(abs(row_diff), abs(col_diff)))

        if [row_diff, col_diff_abs] == [0, -1]:
            return [0, -1]

    def E_direction(self, from_pos, to_pos):
        """
        Returns the direction a player wants to move to"""

        from_index = self._board.get_location(from_pos)
        to_index = self._board.get_location(to_pos)

        row_diff = to_index[0] - from_index[0]
        col_diff = to_index[1] - from_index[1]

        col_diff_abs = int((col_diff) / max(abs(row_diff), abs(col_diff)))

        if [row_diff, col_diff_abs] == [0, 1]:
            return [0, 1]

    @property
    def board(self):
        return self._board


########################################################################################################################
########################################################################################################################

class Board:
    """Creats Board setups for Gess game"""

    def __init__(self):
        """
        Locations on the board will be specified using columns labeled a-t and rows labeled 1-20, with row 1 being
        the Black side and row 20 the White side. The actual board is only columns b-s and rows 2-19. The center of
        the piece being moved must stay within those boundaries. An edge of the piece may go into columns a or t,
        or rows 1 or 20, but any pieces there are removed at the end of the move. Black goes first.
        """
        self._board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w', ' ', 'w', ' ', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', ' ', 'w', ' ', 'w', ' ', ' '],
            [' ', 'w', 'w', 'w', ' ', 'w', ' ', 'w', 'w', 'w', 'w', ' ', 'w', ' ', 'w', ' ', 'w', 'w', 'w', ' '],
            [' ', ' ', 'w', ' ', 'w', ' ', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', ' ', 'w', ' ', 'w', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ', 'w', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b', ' ', ' ', 'b', ' ', ' ', 'b', ' ', ' ', 'b', ' ', ' ', 'b', ' ', ' ', 'b', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'b', ' ', 'b', ' ', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', ' ', 'b', ' ', 'b', ' ', ' '],
            [' ', 'b', 'b', 'b', ' ', 'b', ' ', 'b', 'b', 'b', 'b', ' ', 'b', ' ', 'b', ' ', 'b', 'b', 'b', ' '],
            [' ', ' ', 'b', ' ', 'b', ' ', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', ' ', 'b', ' ', 'b', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

        self._rows = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]  # row numbers

        self._columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't']  # column letters

        self._length_row = len(self._board) - 1  # get row length

        self._length_col = len(self._board[0]) - 1  # get col length

    def board_display(self):
        """
        Displays board"""
        space = '  '
        print((space * 22), "WHITE")
        print(' ', space, ("  " + space).join(self._columns))
        for row in reversed(self._rows):
            board_piece = self._board[abs(row - 20)]
            line = str(row).rjust(2) + space
            for piece in board_piece:
                line += repr(piece) + space
            print(line.center(20))
        print(' ', space, ("  " + space).join(self._columns))
        print(space * 21, "BLACK")

    def footprint(self, pos):
        """Footprint setup
        Returns a list of footprint position"""

        center_index = self.get_location(pos)

        upper_left = [center_index[0] - 1, center_index[1] - 1]
        left = [center_index[0], center_index[1] - 1]
        lower_left = [center_index[0] + 1, center_index[1] - 1]
        upper = [center_index[0] - 1, center_index[1]]
        lower = [center_index[0] + 1, center_index[1]]
        upper_right = [center_index[0] - 1, center_index[1] + 1]
        right = [center_index[0], center_index[1] + 1]
        lower_right = [center_index[0] + 1, center_index[1] + 1]
        center = [center_index[0], center_index[1]]

        return [upper_left, left, lower_left, upper, lower, upper_right, right, lower_right, center]

    def get_position_str(self, loc):
        """Take position index and converts into a string"""
        row_str = str(20 - loc[0])
        column_str = str(self._columns[loc[1]])
        return column_str + row_str

    def get_location(self, pos):
        """Take string and converts into integer index"""
        row_index = abs(int(pos[1:]) - 20)
        col_index = self._columns.index(pos[0].lower())
        return [row_index, col_index]  # return [row,col] corresponding to pos in self._board

    def clear_pos(self, pos):
        """
        Clears move_from footprint after a move has been made"""

        pos_list = self.footprint(pos)
        for pos in pos_list:
            self._board[pos[0]][pos[1]] = ' '

    def clear_border_pieces(self):
        """
        Clears any piece that is outside of the 18x18 board after a move has been made"""

        for i in range(self._length_col):
            if self._board[0][i] == 'w' or 'b':
                self._board[0][i] = ' '

        for i in range(self._length_col):
            if self._board[19][i] == 'w' or 'b':
                self._board[19][i] = ' '

        for j in range(self._length_row):
            if self._board[j][0] == 'w' or 'b':
                self._board[j][0] = ' '

        for j in range(self._length_row):
            if self._board[j][19] == 'w' or 'b':
                self._board[j][19] = ' '

    def check_current_position_valid(self, from_pos):
        """
        Determines if from_pos is not out of range
        from_pos should be in the range of 18x18 board
        """
        if 0 < self.get_location(from_pos)[0] < self._length_row and 0 < self.get_location(from_pos)[
            1] < self._length_col:
            return True
        else:
            return False

    def check_move_position_valid(self, to_pos):
        """
        Determines if to_pos is in valid spot
        to_pos should be in the range of 18x18 board
        """
        to_index = self.get_location(to_pos)

        if 0 < to_index[0] < self._length_row and 0 < to_index[1] < self._length_col:
            return True
        else:
            return False

    def check_move_from_ring_black(self, from_pos, current_player):
        """
        Returns True if this is not the last ring
        False if this is the last ring and player can make this move so that breaks the last ring
        """
        black_ring_count, ring_center_index = self.black_last_ring_pos()

        if black_ring_count != 1:
            return True

        if current_player != 'black':
            return True

        # check if black player's next move will break it's own last ring
        # black cant break it's on
        # get the index of 9 pieces of from_pos
        ring_center = self.get_position_str(ring_center_index[0])

        # if the from_to square is identical to the ring square
        # we are still able to move the entire piece
        if ring_center_index[0] == self.get_location(from_pos):
            return True

        from_pos_index_list = self.footprint(from_pos)
        black_ring_index_list = self.footprint(ring_center)

        for i in from_pos_index_list:
            for j in black_ring_index_list:
                if i == j:
                    return False
        return True

    def check_move_from_ring_white(self, from_pos, current_player):
        """
        Returns True if this is not the last ring
        False if this is the last ring and player can make this move so that breaks the last ring
        """
        white_ring_count, ring_center_index = self.white_last_ring_pos()

        if white_ring_count != 1:
            return True

        if current_player != 'white':
            return True

        # check if white player's next move will break it's own last ring
        # white cant break it's only ring
        ring_center = self.get_position_str(ring_center_index[0])

        # if the from_to square is identical to the ring square
        # we are still able to move the entire piece
        if ring_center_index[0] == self.get_location(from_pos):
            return True

        else:
            from_pos_index_list = self.footprint(from_pos)
            white_ring_index_list = self.footprint(ring_center)

            for i in from_pos_index_list:
                for j in white_ring_index_list:
                    if i == j:
                        return False
            return True

    def check_move_to_ring_black(self, from_pos, to_pos, current_player):
        """
        Returns True if player's to_pos is valid. It wont break it's own ring
        False if play's next move will break it's own ring (last ring).
        """

        black_ring_count, ring_center_index = self.black_last_ring_pos()

        if black_ring_count != 1:
            return True

        if current_player != 'black':
            return True

        # check if white player's next move will break it's own last ring
        # black cant break it's only ring
        ring_center = self.get_position_str(ring_center_index[0])

        if ring_center_index[0] == self.get_location(from_pos):
            return True

        else:
            to_pos_index_list = self.footprint(to_pos)
            black_ring_index_list = self.footprint(ring_center)

            for i in to_pos_index_list:
                for j in black_ring_index_list:
                    if i == j:
                        return False
        return True

    def check_move_to_ring_white(self, from_pos, to_pos, current_player):
        """
        Returns True if player's to_pos is valid. It wont break it's own ring
        False if play's next move will break it's own ring ( last ring).
        """

        white_ring_count, ring_center_index = self.white_last_ring_pos()

        if white_ring_count != 1:
            return True

        if current_player != 'white':
            return True

        # check if white player's next move will break it's own last ring
        # white cant break it's only ring
        ring_center = self.get_position_str(ring_center_index[0])

        if ring_center_index[0] == self.get_location(from_pos):
            return True

        else:
            to_pos_index_list = self.footprint(to_pos)
            white_ring_index_list = self.footprint(ring_center)

            for i in to_pos_index_list:
                for j in white_ring_index_list:
                    if i == j:
                        return False
        return True

    def black_last_ring_pos(self):
        """
        Returns a list of black ring positions """

        black_ring_count = 0
        black_ring_list = []
        # A ring is a ring of eight stones around an empty center
        for i in range(self._length_row):
            for j in range(1, self._length_col):
                # check to see if i is empty
                # if it's empty, check the 8 stones around center. If there are 8 stones surrounding it, there is a ring
                if self._board[i][j] == ' ':
                    if self._board[i - 1][j - 1] == 'b' and self._board[i + 1][j - 1] == 'b' and self._board[i - 1][
                        j] == 'b' and self._board[i + 1][j] == 'b' and self._board[i - 1][j + 1] == 'b' \
                            and self._board[i + 1][j + 1] == 'b' and self._board[i][j - 1] == 'b' \
                            and self._board[i][j + 1] == 'b':
                        black_ring_list.append([i, j])
                        black_ring_count += 1
        return black_ring_count, black_ring_list

    def white_last_ring_pos(self):
        """
        Returns a list of black ring positions """

        white_ring_count = 0
        white_ring_list = []
        # A ring is a ring of eight stones around an empty center
        for i in range(self._length_row):
            for j in range(1, self._length_col):
                # check to see if i is empty
                # if it's empty, check the 8 stones around center. If there are 8 stones surrounding it, there is a ring
                if self._board[i][j] == ' ':
                    if self._board[i - 1][j - 1] == 'w' and self._board[i + 1][j - 1] == 'w' and self._board[i - 1][
                        j] == 'w' and self._board[i + 1][j] == 'w' and self._board[i - 1][j + 1] == 'w' \
                            and self._board[i + 1][j + 1] == 'w' and self._board[i][j - 1] == 'w' \
                            and self._board[i][j + 1] == 'w':
                        white_ring_list.append([i, j])
                        white_ring_count += 1

        return white_ring_count, white_ring_list
