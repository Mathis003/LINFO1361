from agents.agent import Agent


"""
An agent that uses ...

This agent extends the base Agent class, providing an implementation of the play
method that utilizes the alpha-beta pruning technique to make decisions more efficiently.

Attributes:
    max_depth (int): The maximum depth the search algorithm will explore.
"""
class AI(Agent):

    """
    Initializes an AlphaBetaAgent instance with a specified player, game, and maximum search depth.

    Args:
        - player (int): The player ID this agent represents (0 or 1).
        - game (ShobuGame): The Shobu game instance the agent will play on.
        - max_depth (int): The maximum depth of the search tree.
    """
    def __init__(self, player, game):
        super().__init__(player, game)
        self.max_depth = 3

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
        self.eval(state, True)
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
        return depth == 0 or self.game.is_terminal(state)
    

    """
    Position Indexing on each board:
        12 | 13 | 14 | 15
        ------------------
        8 |  9 | 10 | 11
        ------------------
        4 |  5 |  6 |  7
        ------------------
        0 |  1 |  2 |  3
    """
    

    """
    Evaluates the given state and returns a score from the perspective of the agent's player.

    Args:
        state (ShobuState): The game state to evaluate.

    Returns:
        float: The evaluated score of the state.
    """
    def eval(self, state, debug=False):
        
        # TODO : Bien distinguer les board d'attaque et de défense !

        board    = state.board
        player   = self.player
        opponent = 1 - player

        # Avantages matériels
        min_score_material_all = -12
        max_score_material_all = 12
        score_material_all = 0

        min_score_material_min = -4
        max_score_material_min = 4
        nbPieces_min = [4, 4]

        for i in range(4):
            score_material_all += len(board[i][player]) - len(board[i][opponent])

            nbPieces_min[player]   = min(len(board[i][player]), nbPieces_min[player])
            nbPieces_min[opponent] = min(len(board[i][opponent]), nbPieces_min[opponent])

        score_material_min = nbPieces_min[player] - nbPieces_min[opponent]

        # Normalement, le code est bon pour ça
        # if debug:
            # print("score_material_all : ", score_material_all)
            # print("score_material_min : ", score_material_min)
            # print("=======================================\n")

        score_material_all = (score_material_all - min_score_material_all) / (max_score_material_all - min_score_material_all)
        score_material_min = (score_material_min - min_score_material_min) / (max_score_material_min - min_score_material_min)

        score_material = 0.3 * score_material_all + 0.7 * score_material_min

        # Avantages positionnels
        score_position = 0
        max_score_position = 16
        min_score_position = -16
        good_positions = [5, 6, 9, 10]
        for i in range(4):
            positions_player   = list(board[i][player])
            positions_opponent = list(board[i][opponent])
            for position in positions_player:
                if position in good_positions:
                    score_position += 1
            for position in positions_opponent:
                if position in good_positions:
                    score_position -= 1

        # Normalement, le code est bon pour ça
        # if debug:
            # print("score_position : ", score_position)
            # print("=======================================\n")
        
        score_position = (score_position - min_score_position) / (max_score_position - min_score_position)
                    
        # Avantage de protection
        max_score_protection = 32
        min_score_protection = -32
        score_protection = 0

        if player == 0:
            range_value = [0, 1]
            other_range_value = [2, 3]
        else:
            range_value = [2, 3]
            other_range_value = [0, 1]

        for i in range_value:
            positions_player = list(board[i][player])
            
            for position in positions_player:

                offsets = [-1, 1, -4, 4, -5, 5, -3, 3]

                if position % 4 == 0:
                    offsets.remove(-1)
                    offsets.remove(-5)
                    offsets.remove(3)

                if (position + 1) % 4 == 0:
                    offsets.remove(1)
                    offsets.remove(-3)
                    offsets.remove(5)
                
                if position < 4:
                    offsets.remove(-4)
                    if -5 in offsets:
                        offsets.remove(-5)
                    if -3 in offsets:
                        offsets.remove(-3)

                if position > 11:
                    offsets.remove(4)
                    if 5 in offsets:
                        offsets.remove(5)
                    if 3 in offsets:
                        offsets.remove(3)

                for offset in offsets:
                    if position + offset in positions_player:
                        score_protection += 1

        for i in other_range_value:
            positions_opponent = list(board[i][opponent])
            for position in positions_opponent:

                offsets = [-1, 1, -4, 4, -5, 5, -3, 3]

                if position % 4 == 0:
                    offsets.remove(-1)
                    offsets.remove(-5)
                    offsets.remove(3)

                if (position + 1) % 4 == 0:
                    offsets.remove(1)
                    offsets.remove(-3)
                    offsets.remove(5)
                
                if position < 4:
                    offsets.remove(-4)
                    if -5 in offsets:
                        offsets.remove(-5)
                    if -3 in offsets:
                        offsets.remove(-3)

                if position > 11:
                    offsets.remove(4)
                    if 5 in offsets:
                        offsets.remove(5)
                    if 3 in offsets:
                        offsets.remove(3)
                
                for offset in offsets:
                    if position + offset in positions_opponent:
                        score_protection -= 1

        # Normalement, le code est bon pour ça
        # if debug:
            # print("score_protection : ", score_protection)
            # print("=======================================\n")
        
        score_protection = (score_protection - min_score_protection) / (max_score_protection - min_score_protection)

        # Avantages de mobilité
        max_score_mobility = 130  # A determiner
        min_score_mobility = -130 # A determiner
        player_moves   = self.game.compute_actions(board, player)
        opponent_moves = self.game.compute_actions(board, opponent)
        score_mobility = len(player_moves) - len(opponent_moves)

        # Pas vérifier car trop chiant à faire
        # if debug:
            # print("score_mobility : ", score_mobility)
            # print("=======================================\n")

        score_mobility = (score_mobility - min_score_mobility) / (max_score_mobility - min_score_mobility)

        # Avantage de menace de poussée
        score_push = 0 
        # Trop compliqué à calculer pour l'instant sans utiliser self.game.result() pour simuler les coups (trop lent)
  
        # Coefficients de pondération
        coeff_material     = 0.55  # A determiner
        coeff_position     = 0.25  # A determiner
        coeff_mobility     = 0.05  # A determiner
        coeff_protection   = 0.15   # A determiner

        coeff_push         = 0.0   # A determiner

        total_score = coeff_material * score_material + coeff_position * score_position + coeff_mobility * score_mobility + coeff_protection * score_protection + coeff_push * score_push
        return total_score

    """
    Implements the alpha-beta pruning algorithm to find the best action.

    Args:
        state (ShobuState): The current game state.

    Returns:
        ShobuAction: The best action as determined by the alpha-beta algorithm.
    """
    def alpha_beta_search(self, state):
        _, action = self.max_value(state, - float("inf"), float("inf"), self.max_depth)
        return action
    
    # def hashBoard(self, board):
    #     board_str = ""
    #     for i in range(4):
    #         currBoard = list(board[i])
    #         for j in range(16):
    #                 if j in currBoard[0]:
    #                     board_str += "o"
    #                 elif j in currBoard[1]:
    #                     board_str += "x"
    #                 else:
    #                     board_str += "."
    #     return board_str


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
        
        # boardHashed = self.hashBoard(state.board)

        if self.is_cutoff(state, depth):
            return self.eval(state), None

        maxValue, bestMove = -float("inf"), None
        
        for action in self.game.actions(state):
            
            result_state = self.game.result(state, action)
            currValue, _ = self.min_value(result_state, alpha, beta, depth - 1)

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

        # boardHashed = self.hashBoard(state.board)

        if self.is_cutoff(state, depth):
            return self.eval(state), None

        minValue, bestMove = float("inf"), None
        
        for action in self.game.actions(state):
            
            result_state = self.game.result(state, action)
            currValue, _ = self.max_value(result_state, alpha, beta, depth - 1)
            
            if currValue < minValue:
                minValue, bestMove = currValue, action
                beta = min(beta, minValue)

            if beta <= alpha:
                break
        
        return minValue, bestMove