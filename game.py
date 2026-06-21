from player import HumanPlayer, RandomComputerPlayer


class TicTacToe:
    def __init__(self):
        self.board = [
            " " for _ in range(9)
        ]  # we will use a single list to represent 3x3
        self.current_winner = None  # keeps track of winner

    def print_board(self):
        # getting rows in 3x3
        for row in [self.board[i * 3 : (i + 1) * 3] for i in range(3)]:
            print("| " + " | ".join(row) + " |")

    @staticmethod
    def print_board_nums():
        # what number corresponds to what box
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print("| " + " | ".join(row) + " |")

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def empty_squares(self):
        return " " in self.board

    def num_empty_squares(self):
        return self.board.count(" ")

    def make_move(self, square, letter):
        if self.board[square] == " ":
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # winner if 3 in row, but we have to check all possiblity's
        row_index = square // 3
        row = self.board[row_index * 3 : (row_index + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        col_index = square % 3
        column = [self.board[col_index + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0, 4, 8]]  # left to right
            if all([spot == letter for spot in diag1]):
                return True

            diag2 = [self.board[i] for i in [2, 4, 6]]  # right to left
            if all([spot == letter for spot in diag2]):
                return True

        return False


def play(game, x_player, o_player, print_game=True):
    # returns winner of the game (letter) or None for tie
    if print_game:
        game.print_board_nums()

    letter = "X"  # starting letter

    # we will iterate while game still has empty squares
    while game.empty_squares():
        # getting the move from the appropriate player
        if letter == "O":
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        # function to make the move
        if game.make_move(square, letter):
            if print_game:
                print(letter + f" makes a move to square {square}")
                game.print_board()
                print("")  # just empty line

            # win check
            if game.current_winner:
                if print_game:
                    print(letter + " wins!")
                return letter

            # switches players
            letter = "O" if letter == "X" else "X"

    # ONLY runs when loop ends (tie)
    if print_game:
        print("It's a tie")

    return None


if __name__ == "__main__":
    x_player = HumanPlayer("X")
    o_player = RandomComputerPlayer("O")
    t = TicTacToe()
    play(t, x_player, o_player, print_game=True)
