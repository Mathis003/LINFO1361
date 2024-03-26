from agent import Agent

SAME = 0

class TranpositionTable:

    def __init__(self):
        self.table = {}

    def get(self, key, default_key=None):
        return self.table.get(key, default_key)

    def set(self, key, value):
        self.table[key] = value
    
    def contain(self, key):
        return key in self.table
    
    def remove(self, key):
        del self.table[key]

    def clear(self):
        self.table.clear()
    
    def keys(self):
        return self.table.keys()

    def values(self):
        return self.table.values()

    def items(self):
        return self.table.items()

    def __str__(self):
        pass




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
        self.explored = {}
        self.max_depth = 3


    def clear_oldStates(self, nb_pieces):
        keys = list(self.explored.keys())
        for key in keys:
            if key[0] > nb_pieces[0] or key[1] > nb_pieces[1]:
                del self.explored[key]

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

        self.clear_oldStates(self.getPieces(state.board))
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

        # Avantages de mobilité (Trop long à calculer !)
        # max_score_mobility = 130  # A determiner
        # min_score_mobility = -130 # A determiner
        # player_moves   = self.game.compute_actions(board, player)
        # opponent_moves = self.game.compute_actions(board, opponent)
        # score_mobility = len(player_moves) - len(opponent_moves)

        # Pas vérifier car trop chiant à faire
        # if debug:
            # print("score_mobility : ", score_mobility)
            # print("=======================================\n")

        # score_mobility = (score_mobility - min_score_mobility) / (max_score_mobility - min_score_mobility)

        # Avantage de menace de poussée
        # score_push = 0 
        # Trop compliqué à calculer pour l'instant sans utiliser self.game.result() pour simuler les coups (trop lent)
  
        # Coefficients de pondération
        coeff_material     = 0.55  # A determiner
        coeff_position     = 0.3   # A determiner
        coeff_protection   = 0.15   # A determiner

        # coeff_mobility     = 0.05  # A determiner
        # coeff_push         = 0.0   # A determiner

        total_score = coeff_material * score_material + coeff_position * score_position + coeff_protection * score_protection
        return total_score

    """
    Implements the alpha-beta pruning algorithm to find the best action.

    Args:
        state (ShobuState): The current game state.

    Returns:
        ShobuAction: The best action as determined by the alpha-beta algorithm.
    """
    def alpha_beta_search(self, state):
        # _, action = self.minimaxAlphaBeta(state, - float("inf"), float("inf"), self.max_depth, True)
        _, action = self.minimaxAlphaBetaWithTT(state, - float("inf"), float("inf"), self.max_depth, True)
        return action
    
    
    def getPieces(self, board):
        nb_white_pieces, nb_black_pieces = 0, 0
        for currBoard in board:
            nb_white_pieces += len(currBoard[0])
            nb_black_pieces += len(currBoard[1])
        return (nb_white_pieces, nb_black_pieces)
    

    def hashBoard(self, board):
        board_str = ""
        for i in range(4):
            positions_white = list(board[i][0])
            positions_black = list(board[i][1])
            for pos_idx in range(16):
                    if pos_idx in positions_white:
                        board_str += "o"
                    elif pos_idx in positions_black:
                        board_str += "x"
                    else:
                        board_str += "."
        return board_str


    def minimaxAlphaBeta(self, state, alpha, beta, depth, maximizingPlayer):
        
        if self.is_cutoff(state, depth):
            return self.eval(state), None

        bestMove = None

        if maximizingPlayer:
            value = -float("inf")
            a = alpha
            
            for action in self.game.actions(state):
                
                result_state = self.game.result(state, action)
                currValue, _ = self.minimaxAlphaBeta(result_state, a, beta, depth - 1, False)

                if value < currValue:
                    value, bestMove = currValue, action
                    a = max(a, value)

                if beta <= a:
                    break
        else:
            value = float("inf")
            b = beta
            
            for action in self.game.actions(state):
                
                result_state = self.game.result(state, action)
                currValue, _ = self.minimaxAlphaBeta(result_state, alpha, b, depth - 1, True)
                
                if currValue < value:
                    value, bestMove = currValue, action
                    b = min(b, value)

                if b <= alpha:
                    break
        
        return value, bestMove
    


    def minimaxAlphaBetaWithTT(self, state, alpha, beta, depth, maximizingPlayer):

        boardHashed = self.hashBoard(state.board)
        nbPieces = (boardHashed.count('o'), boardHashed.count('x'))
        TT = self.explored.get(nbPieces)

        tt_entry = None
        if TT is None:
            TT = TranpositionTable()
            self.explored[nbPieces] = TT
        else:
            tt_entry = TT.get(boardHashed)
            if tt_entry is not None and tt_entry["depth"] >= depth:

                if tt_entry["symetrie"] == SAME:

                    if tt_entry["lowerbound"] >= beta:
                        return tt_entry["lowerbound"], tt_entry["move"]
                    
                    if tt_entry["upperbound"] <= alpha:
                        return tt_entry["upperbound"], tt_entry["move"]
                    
                    alpha = max(alpha, tt_entry["lowerbound"])
                    beta  = min(beta, tt_entry["upperbound"])


        if self.is_cutoff(state, depth):
            return self.eval(state), None

        bestMove = None

        if maximizingPlayer:
            value = -float("inf")
            a = alpha
            
            for action in self.game.actions(state):
                
                result_state = self.game.result(state, action)
                currValue, _ = self.minimaxAlphaBetaWithTT(result_state, a, beta, depth - 1, False)

                if value < currValue:
                    value, bestMove = currValue, action
                    a = max(a, value)

                if beta <= a:
                    break
        else:
            value = float("inf")
            b = beta
            
            for action in self.game.actions(state):
                
                result_state = self.game.result(state, action)
                currValue, _ = self.minimaxAlphaBetaWithTT(result_state, alpha, b, depth - 1, True)
                
                if currValue < value:
                    value, bestMove = currValue, action
                    b = min(b, value)

                if b <= alpha:
                    break
        
        lowerbound = -float("inf")
        upperbound = float("inf")
        if value <= alpha:
            upperbound = value
        if value > alpha and value < beta:
            upperbound = value
            lowerbound = value
        if value >= beta:
            lowerbound = value
        
        TT.set(boardHashed, {"exact": value, "lowerbound": lowerbound, "upperbound": upperbound, "move": bestMove, "symetrie": SAME, "depth": depth})
        
        return value, bestMove