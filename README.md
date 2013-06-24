This is a self learning Tic Tac Toe game. 
The program uses TD learning (TD(0)). i.e depending on the current state it predicts the next best state.
For exploration vs exploitation the choice of action used is epsilon greedy. where epsilon chosen is 0.9.

The program needs to play 5000 games to completely understand the game. 
The basic idea used in the program is the minimax algorithm.
Lets consider 'X' as the maximizer and 'O' as the minimizer. 
When 'X' makes its move 'O' calculates the best action of the next state which minimizes the reward.
When 'O' makes its move 'X' calculates the best action of the next state which maximises the reward.
