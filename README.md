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



### Mathematical Explanation

The algorithm evaluates the game tree by considering all possible moves and their outcomes. The mathematical representation of the Minimax algorithm with Alpha-Beta pruning can be described as follows:

#### Minimax Function

For the maximizing player:

\[ V(s) = \max_{a \in A(s)} \minimax(s') \]

For the minimizing player:

\[ V(s) = \min_{a \in A(s)} \minimax(s') \]

Where:
- \( V(s) \) is the value of the game state \( s \).
- \( A(s) \) is the set of possible actions in state \( s \).
- \( s' \) is the resulting state from action \( a \).

#### Alpha-Beta Pruning

During the evaluation, the algorithm maintains two values, alpha and beta:

- **Alpha (α):** The best value that the maximizing player can guarantee at that level or above.
- **Beta (β):** The best value that the minimizing player can guarantee at that level or above.

The pruning occurs when:

\[ \beta \leq \alpha \]

This indicates that further exploration of the current node is unnecessary because it cannot affect the final decision.

## Example Usage

The algorithm is used to determine the best move for the AI in the `get_best_move` function:


```python
def get_best_move(game, difficulty):
    if random.random() > difficulty:
        return random.choice(game.available_moves())
    
    best_score = float('-inf')
    best_move = None
    for move in game.available_moves():
        game.make_move(move, 'O')
        score = minimax(game, 0, float('-inf'), float('inf'), False)
        game.board[move] = ' '
        game.current_winner = None
        if score > best_score:
            best_score = score
            best_move = move
    return best_move
```


## Conclusion

The Alpha-Beta Pruning Minimax algorithm allows the AI to play optimally by evaluating the game tree efficiently. This implementation ensures that the AI makes the best possible move, providing a challenging opponent for the player.

This README provides an overview of the algorithm and its implementation in the Tic-Tac-Toe game. For further details, refer to the source code and comments within the code.
