from agents.agent import Agent
import time

"""
An agent that uses the alpha-beta pruning algorithm to determine the best move.

This agent extends the base Agent class, providing an implementation of the play
method that utilizes the alpha-beta pruning technique to make decisions more efficiently.

Attributes:
    max_depth (int): The maximum depth the search algorithm will explore.
"""
class AlphaBetaAgent(Agent):

    def __str__(self):
        return "AlphaBetaAgent"

    """
    Initializes an AlphaBetaAgent instance with a specified player, game, and maximum search depth.

    Args:
        - player (int): The player ID this agent represents (0 or 1).
        - game (ShobuGame): The Shobu game instance the agent will play on.
        - max_depth (int): The maximum depth of the search tree.
    """
    def __init__(self, player, game, max_depth):
        super().__init__(player, game)
        self.max_depth = max_depth

        self.time = [0] * 10000
        self.coup_i = 0

        self.nodeExplored = 0


    """
    Determines the best action by applying the alpha-beta pruning algorithm.

    Overrides the play method in the base class.

    Args:
        - state (ShobuState): The current state of the game.
        - remaining_time (float): The remaining time in seconds that the agent has to make a decision.

    Returns:
        ShobuAction: The action determined to be the best by the alpha-beta algorithm.
    """
    def play(self, state, remaining_time):
        start = time.time()
        action = self.alpha_beta_search(state)
        self.time[self.coup_i] = time.time() - start
        self.coup_i += 1
        return action
    

    """
    Determines if the search should be cut off at the current depth.

    Args:
        - state (ShobuState): The current state of the game.
        - depth (int): The current depth in the search tree.

    Returns:
        bool: True if the search should be cut off, False otherwise.
    """
    def is_cutoff(self, state, depth):
        return depth == self.max_depth or self.game.is_terminal(state)
    

    """
    Evaluates the given state and returns a score from the perspective of the agent's player.

    Args:
        state (ShobuState): The game state to evaluate.

    Returns:
        float: The evaluated score of the state.
    """
    def eval(self, state):
        min_pieces = [4, 4]
        for board in state.board:
            for i in range(2):
                min_pieces[i] = min(min_pieces[i], len(board[i]))
        
        return min_pieces[self.player] - min_pieces[1 - self.player]

    """
    Implements the alpha-beta pruning algorithm to find the best action.

    Args:
        state (ShobuState): The current game state.

    Returns:
        ShobuAction: The best action as determined by the alpha-beta algorithm.
    """
    def alpha_beta_search(self, state):
        _, action = self.max_value(state, - float("inf"), float("inf"), 0)
        return action

    """
    Computes the maximum achievable value for the current player at a given state using the alpha-beta pruning.

    This method recursively explores all possible actions from the current state to find the one that maximizes
    the player's score, pruning branches that cannot possibly affect the final decision.

    Args:
        - state (ShobuState): The current state of the game.
        - alpha (float): The current alpha value, representing the minimum score that the maximizing player is assured of.
        - beta (float): The current beta value, representing the maximum score that the minimizing player is assured of.
        - depth (int): The current depth in the search tree.

    Returns:
        tuple: A tuple containing the best value achievable from this state and the action that leads to this value.
            If the state is a terminal state or the depth limit is reached, the action will be None.
    """
    def max_value(self, state, alpha, beta, depth):

        if self.is_cutoff(state, depth):
            self.nodeExplored += 1
            return self.eval(state), None

        maxValue, bestMove = -float("inf"), None
        
        for action in self.game.actions(state):
            
            result_state = self.game.result(state, action)
            currValue, _ = self.min_value(result_state, alpha, beta, depth + 1)

            if maxValue < currValue:
                maxValue, bestMove = currValue, action
                alpha = max(alpha, maxValue)

            if beta <= alpha:
                break

        return maxValue, bestMove


    """
    Computes the minimum achievable value for the opposing player at a given state using the alpha-beta pruning.

    Similar to max_value, this method recursively explores all possible actions from the current state to find
    the one that minimizes the opponent's score, again using alpha-beta pruning to cut off branches that won't
    affect the outcome.

    Args:
        - state (ShobuState): The current state of the game.
        - alpha (float): The current alpha value, representing the minimum score that the maximizing player is assured of.
        - beta (float): The current beta value, representing the maximum score that the minimizing player is assured of.
        - depth (int): The current depth in the search tree.

    Returns:
        tuple: A tuple containing the best value achievable from this state for the opponent and the action that leads to this value.
            If the state is a terminal state or the depth limit is reached, the action will be None.
    """
    def min_value(self, state, alpha, beta, depth):

        if self.is_cutoff(state, depth):
            self.nodeExplored += 1
            return self.eval(state), None

        minValue, bestMove = float("inf"), None
        
        for action in self.game.actions(state):
            
            result_state = self.game.result(state, action)
            currValue, _ = self.max_value(result_state, alpha, beta, depth + 1)
            
            if currValue < minValue:
                minValue, bestMove = currValue, action
                beta = min(beta, minValue)

            if beta <= alpha:
                break
        
        return minValue, bestMove