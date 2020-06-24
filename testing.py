# class GameEngine:
#     """Represents game engine for Gess"""
#     def __init__(self):
#         self.game = GessGame()
#
#     def engine(self):
#         """Game engine for Gess"""
#         while self.game.get_game_state() == "UNFINISHED":
#             self.game._board.board_display()
#             print("Black goes first.")
#             turn_player = self.game.get_player()
#             print(turn_player, "'s turn")
#             from_pos = input("Enter a location to move from: ").strip()
#             to_pos = input("Enter a location to move to: ").strip()
#             try_move = self.game.make_move(from_pos, to_pos)
#             while not try_move:
#                 print("Move not valid. Try again.")
#                 from_pos = input("Enter a location to move from: ").strip()
#                 to_pos = input("Enter a location to move to: ").strip()
#                 try_move = self.game.make_move(from_pos, to_pos)
#         print(self.game.get_game_state())
#
#
#
# ### Instantiation game for testing ###
# def main():
#     game = GameEngine()
#     game.engine()
#
# if __name__ == '__main__':
#     main()

# game = GessGame()
# print(game._board.board_display())
# print(game.make_move('c3', 'c5'))
# print(game.make_move('p18', 'p16'))
# print(game.make_move('c6', 'c13'))
# print(game.make_move('p15', 'i8'))
# print(game.make_move('c13', 'g9'))
# print(game.make_move('i8', 'j9'))#not valid
# print(game.make_move('j9', 'i8'))
# print(game.make_move('g9', 'g13'))
# print(game.make_move('c18', 'c5'))
# print(game.make_move('g13', 'g16'))
# print(game.make_move('c5', 'c6'))
# print(game.make_move('g16', 'b11'))
# print(game.make_move('c6', 'e6'))
# print(game.make_move('i3', 'i6'))
# print(game.make_move('e6', 'g6'))
# print(game.make_move('l3', 'i3'))
# print(game.make_move('g6', 'g5'))
# print(game.make_move('g6', 'g5'))

###############
# game = GessGame()
# print(game.make_move('i3', 'i6'))

# print(game.make_move('i3', 'i6'))
# print(game.make_move('i6', 'j5'))
# print(game.make_move('k3', 'k4'))
# print(game.make_move('l18', 'l17'))
# print(game.make_move('l18', 'k18'))
# print(game.make_move('l15', 'm14'))
# print(game.make_move('l15', 'l10'))
# print(game.make_move('L18', 'l15'))
# print(game.make_move('i6', 'g8'))
# print(game.make_move('i15', 'i12'))
# print(game.make_move('r3', 'r6'))
# print(game.make_move('l15', 'n15'))
# print(game.make_move('g8', 'b13'))
# print(game.make_move('i18', 'k16'))
# print(game.make_move('l3', 'i3'))
# print(game.make_move('n15', 'q15'))
# print(game.make_move('c13', 'c16'))
# print(game.make_move('o18', 'n17'))
# print(game.make_move('c16', 'c17'))
# print(game.make_move('f18', 'h16'))
# print(game.make_move('i3', 'l3'))
# print(game.make_move('h16', 'e19'))
# print(game.make_move('l3', 'l6'))
# print(game.make_move('q15', 'n12'))
# print(game.make_move('l6', 'l9'))
# print(game.make_move('n12', 'n11'))
# print(game.make_move('l15', 'n15'))
# print(game.make_move('f3', 'g4'))


