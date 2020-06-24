from GessGame import GessGame
from GessGame import Board

if __name__ == "__main__":
    game = GessGame()
    board = game._board

    print("Black goes first.")
    play_game = "yes"
    while play_game == "yes":
        while game.get_game_state() == "UNFINISHED":
            try:
                game._board.board_display()
                turn_player = game.get_player()
                print(turn_player, "'s turn")
                from_pos = input("Enter a location to move from: ").strip()
                to_pos = input("Enter a location to move to: ").strip()
                try_move = game.make_move(from_pos, to_pos)
                while not try_move:
                    print("Move not valid. Try again.")
                    from_pos = input("Enter a location to move from: ").strip()
                    to_pos = input("Enter a location to move to: ").strip()
                    try_move = game.make_move(from_pos, to_pos)
            except ValueError:
                print("This is not valid notation. Please try again.")
                continue
        print(game.get_game_state())
    play_again = input("Would you like to play again: ")
    play_game = play_again.lower()

