from game import TicTacToe, play
from player import GeniousComputerPlayer, RandomComputerPlayer


# winner test
def test_winner_row():
    t = TicTacToe()
    t.make_move(0, "X")
    t.make_move(1, "X")
    t.make_move(2, "X")
    assert t.current_winner == "X"


def test_winner_col():
    t = TicTacToe()
    t.make_move(0, "X")
    t.make_move(3, "X")
    t.make_move(6, "X")
    assert t.current_winner == "X"


def test_winner_diagonal():
    t = TicTacToe()
    t.make_move(0, "X")
    t.make_move(4, "X")
    t.make_move(8, "X")
    assert t.current_winner == "X"


def test_no_winner():
    t = TicTacToe()
    t.make_move(0, "X")
    t.make_move(1, "X")
    assert t.current_winner is None


# make_move() test
def test_make_move_valid():
    t = TicTacToe()
    assert t.make_move(0, "X") == True


def test_make_move_invalid():
    t = TicTacToe()
    t.make_move(0, "X")
    assert t.make_move(0, "O") == False  # square already taken


# available_moves() test
def test_available_moves_start():
    t = TicTacToe()
    assert t.available_moves() == list(range(9))


def test_available_moves_after_play():
    t = TicTacToe()
    t.make_move(4, "X")
    assert 4 not in t.available_moves()
    assert len(t.available_moves()) == 8


# Minimax never loses
def test_minimax_never_loses():
    x_player = RandomComputerPlayer("X")
    o_player = GeniousComputerPlayer("O")

    for _ in range(100):
        t = TicTacToe()
        result = play(t, x_player, o_player, print_game=False)
        assert result != "X"
