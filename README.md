# 🎮 Tic-Tac-Toe - Minimax AI Engine

> A Python command-line game where an **unbeatable AI** uses the Minimax algorithm to play perfect Tic-Tac-Toe. Runs thousands of simulated games to prove the AI never loses.

---

## Overview

This project runs games between a computer that picks moves randomly (`X`) and an AI that always picks the best possible move (`O`). After thousands of games, the result is always the same: the AI never loses.

It shows how a relatively small amount of code can produce a perfectly rational agent - not through guessing or luck, but by thinking through every possible outcome before making a decision.

---

## Features

- **`GeniusComputerPlayer`** - AI that always plays the best move using Minimax
- **`RandomComputerPlayer`** - Picks a random valid move; used to test the AI against
- **`HumanPlayer`** - Lets you play through the terminal with input validation
- **Configurable simulations** - Run any number of games silently and get win/loss/tie counts
- **Visual mode** - Watch the board update move by move with a short delay

---

## Project Structure

```
TIC-TAC-TOE/
├── game.py      # Board, winner logic, game loop, and simulation runner
└── player.py    # All player types: Random, Human, and Minimax AI
```

`game.py` handles the board and game flow. `player.py` handles how each player decides where to move. They only talk to each other through one method - `get_move()` - which makes swapping player types a one-line change.

---

## How It Works

### Board Representation

The board is stored as a flat list of 9 squares. Each square has a number:

```
| 0 | 1 | 2 |
| 3 | 4 | 5 |
| 6 | 7 | 8 |
```

This makes the math straightforward:
- Row of square `i`: `i // 3`
- Column of square `i`: `i % 3`
- Diagonals only pass through even-numbered squares (`i % 2 == 0`)

### Winner Check

After each move, the code only checks the row, column, and diagonals that pass through the square that was just played - not the whole board. This means the check always takes the same amount of time no matter how many moves have been made. That's what O(1) means.

### Minimax Algorithm

The AI works by trying every possible move, then every possible response to that move, all the way to the end of the game. It picks the move that leads to the best outcome, assuming the opponent also plays perfectly.

```
minimax(state, player):
    if the game is over:
        return a score

    for each available move:
        play that move
        score = minimax(state, opponent)   # check what happens next
        undo that move
        keep track of the best score

    return the best score and which move caused it
```

**Scoring:**

| Outcome | Score |
|---|---|
| AI wins | `+(empty squares + 1)` |
| AI loses | `-(empty squares + 1)` |
| Tie | `0` |

The `+ 1` added to the score means the AI prefers to win as fast as possible, and if it's going to lose, it delays as long as possible. Without this, the AI can't tell the difference between winning now and winning in 5 moves.

Instead of making a copy of the board at every step, the code places a move, goes deeper into the recursion, then removes the move when it comes back. This avoids creating a new board object on every single recursive call.

### Game Loop

```python
while game.empty_squares():
    square = current_player.get_move(game)
    game.make_move(square, letter)
    if game.current_winner:
        return letter          # someone won, stop early
    letter = "O" if letter == "X" else "X"
return None                    # board is full, it's a tie
```

---

## Getting Started

**Requirements:** Python 3.8+, no external libraries needed.

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/tictactoe-minimax.git
cd tictactoe-minimax

# 2. Run a simulation (default: 1,200 games)
python game.py
```

**Sample output:**
```
After 1200 iterations, we see 0 X wins, 831 O wins, and 369 ties
```

**Watch a live game:** In `game.py`, set `print_game=True` inside the `__main__` block. The board prints after each move with a short delay.

**Play against the AI:** Replace `x_player` with `HumanPlayer("X")` in `game.py`:

```python
from player import HumanPlayer, GeniusComputerPlayer

x_player = HumanPlayer("X")
o_player = GeniusComputerPlayer("O")
play(TicTacToe(), x_player, o_player, print_game=True)
```

**Expected results:**

| X Player | O Player | X Wins | O Wins | Ties |
|---|---|---|---|---|
| Random | Minimax | 0 | ~830 | ~370 |
| Minimax | Minimax | 0 | 0 | 1200 |
| Human | Minimax | 0* | varies | varies |

*The Minimax AI cannot be beaten.

---

## Reflection

### What I Learned

**The AI isn't smart - it's thorough.** The biggest shift in my thinking was realizing the AI doesn't "figure out" good moves. It just checks every possible game that could happen from this point forward and picks the path that ends best. That's it. Writing it myself made that concrete in a way that reading about it never did.

**You don't need to copy the board on every step.** I assumed recursion meant making a copy of the game state at every level. The cleaner approach is to make the move, go deeper, then undo the move when you come back. It requires knowing exactly what needs to be reset - `board[square] = " "` and `current_winner = None` - but avoids unnecessary memory use.

**Scoring needs a tiebreaker.** My first version scored every win as `+1` and every loss as `-1`. The bug this caused: the AI would take a win in 5 moves when a win in 1 move was available, because both scored the same. Multiplying by `(empty_squares + 1)` fixes it - bigger scores go to faster wins. It was a good reminder that the score function shapes the behaviour directly.

**Good structure means you can swap parts without breaking anything.** Because every player type shares the same `get_move()` method, the game loop doesn't care whether it's talking to a human, a random bot, or the Minimax AI. Replacing one with another is one line. That's what clean interface design actually feels like in practice.

---

### What I'd Do Differently

**Use an abstract base class for `Player`.** Right now, `Player.get_move()` does nothing (`pass`). If someone creates a new player type and forgets to implement `get_move()`, the bug only appears when the code actually runs. Using Python's `abc` module makes the error happen the moment the class is created instead:

```python
from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, letter: str):
        self.letter = letter

    @abstractmethod
    def get_move(self, game) -> int:
        pass
```

**Add type hints.** Writing `def make_move(self, square: int, letter: str) -> bool` makes it immediately clear what the function expects and returns. It also lets tools like `mypy` catch type errors before you even run the code.

**Add Alpha-Beta Pruning.** Minimax checks every possible branch even when some branches can't possibly change the result. Alpha-Beta pruning skips those branches, cutting the work from `O(b^d)` down to roughly `O(b^(d/2))`. It doesn't matter on a 3×3 board, but it's the right next step for understanding how real game AI is built.

**Write a proper test suite from the start.** Testing `winner()` edge cases and verifying the AI never loses in a loop would have caught bugs immediately instead of requiring me to run the simulation and look at the output manually.

**Fix the typo.** `GeniousComputerPlayer` → `GeniusComputerPlayer`.

---

### Key Takeaways

**A small amount of code can produce a perfect player.** The entire Minimax implementation is around 30 lines. That it produces an unbeatable agent is one of the more satisfying things I've built - not because it's complex, but because it's exactly right.

**Don't optimize until you need to.** Minimax without pruning works perfectly here. Adding pruning would make the code harder to read with no practical benefit on a 9-square board. Knowing when to stop is part of the skill.

**Interfaces earn their value immediately.** Three completely different player types - AI, random bot, human - all plug into the same game loop without any changes. That's the direct payoff of the `get_move()` design.

**Running simulations is a valid way to build confidence in your code.** 1,200 games with zero X wins isn't a mathematical proof, but it's strong evidence the AI is working correctly. Understanding when that kind of evidence is good enough - and when you need something more rigorous - is a real engineering judgment.

---

## Acknowledgments

Built independently as a Python learning project to understand recursive algorithms, game AI, and object-oriented design.

---

*Built by Shervin Babaei · [GitHub](https://github.com/yourusername) · [LinkedIn](https://linkedin.com/in/yourusername)*
