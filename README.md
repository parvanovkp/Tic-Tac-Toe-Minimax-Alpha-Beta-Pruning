# Tic-Tac-Toe AI with Alpha-Beta Pruning Minimax Algorithm

This project implements a Tic-Tac-Toe game with an AI opponent using the Alpha-Beta Pruning Minimax algorithm. The algorithm allows the AI to make optimal moves efficiently, reducing the number of nodes evaluated in the game tree.

## Minimax Algorithm with Alpha-Beta Pruning

### Introduction

The Minimax algorithm is a recursive method used in decision-making and game theory to determine the optimal move for a player, assuming that the opponent is also playing optimally. The algorithm explores all possible moves, recursively evaluating the game state to minimize the possible loss for a worst-case scenario.

Alpha-Beta pruning is an optimization technique for the Minimax algorithm that reduces the number of nodes evaluated by the algorithm. It does this by eliminating branches in the game tree that do not need to be explored because they cannot influence the final decision.

### Minimax Algorithm

The Minimax algorithm can be described as follows:

1. **Maximizing Player (AI):** Tries to maximize the score.
2. **Minimizing Player (Human):** Tries to minimize the score.

The algorithm recursively explores all possible moves, updating the score at each level based on whether it is the maximizing or minimizing player's turn.

### Alpha-Beta Pruning

Alpha-Beta pruning introduces two additional parameters:

- **Alpha (α):** The best score that the maximizing player can guarantee.
- **Beta (β):** The best score that the minimizing player can guarantee.

The algorithm prunes branches that cannot improve the outcome for the current player.

### Algorithm Explanation

The algorithm is implemented in the `minimax` function:

```python
def minimax(game, depth, alpha, beta, maximizing_player):
    if game.current_winner == 'O':
        return 1
    elif game.current_winner == 'X':
        return -1
    elif game.num_empty_squares() == 0:
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in game.available_moves():
            game.make_move(move, 'O')
            eval = minimax(game, depth + 1, alpha, beta, False)
            game.board[move] = ' '
            game.current_winner = None
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in game.available_moves():
            game.make_move(move, 'X')
            eval = minimax(game, depth + 1, alpha, beta, True)
            game.board[move] = ' '
            game.current_winner = None
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
```
