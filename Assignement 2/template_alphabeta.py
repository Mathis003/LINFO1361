from agent import Agent

"""
An agent that uses the alpha-beta pruning algorithm to determine the best move.

This agent extends the base Agent class, providing an implementation of the play
method that utilizes the alpha-beta pruning technique to make decisions more efficiently.

Attributes:
    max_depth (int): The maximum depth the search algorithm will explore.
"""
class AlphaBetaAgent(Agent):

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
        return self.alpha_beta_search(state)
    

    """
    Determines if the search should be cut off at the current depth.

    Args:
        - state (ShobuState): The current state of the game.
        - depth (int): The current depth in the search tree.

    Returns:
        bool: True if the search should be cut off, False otherwise.
    """
    def is_cutoff(self, state, depth):
        # TODO
        return depth == 0 or state.is_terminal()
    

    """
    Evaluates the given state and returns a score from the perspective of the agent's player.

    Args:
        state (ShobuState): The game state to evaluate.

    Returns:
        float: The evaluated score of the state.
    """
    def eval(self, state):
        # TODO
        return state.utility(self.player)


    """
    Implements the alpha-beta pruning algorithm to find the best action.

    Args:
        state (ShobuState): The current game state.

    Returns:
        ShobuAction: The best action as determined by the alpha-beta algorithm.
    """
    def alpha_beta_search(self, state):

        # Launch the alpha-beta search from the state
        maxValue, action = self.max_value(state, - float("inf"), float("inf"), self.max_depth)

        # For debugging purposes
        print(f"Max value: {maxValue}")
        print(f"Action: {action}")

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
        # TODO
        pass


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
        # TODO
        pass