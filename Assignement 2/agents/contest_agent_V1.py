from agents.agent import Agent


class AI_V1(Agent):

    def __init__(self, player, game):
        super().__init__(player, game)
        self.max_depth = 3


    def play(self, state, remaining_time):
        return self.alpha_beta_search(state)
    

    def is_cutoff(self, state, depth):
        return depth == 0 or self.game.is_terminal(state)


    def eval(self, state, debug=False):

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

        # if debug:
            # print("score_position : ", score_position)
            # print("=======================================\n")
        
        score_position = (score_position - min_score_position) / (max_score_position - min_score_position)
                    
        # Avantage de protection
        max_score_protection = 32
        min_score_protection = -32
        score_protection = 0

        for i in range(4):
            positions_player   = list(board[i][player])
            positions_opponent = list(board[i][opponent])

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

        # if debug:
            # print("score_mobility : ", score_mobility)
            # print("=======================================\n")

        # score_mobility = (score_mobility - min_score_mobility) / (max_score_mobility - min_score_mobility)

        # Avantage de menace de poussée
        # score_push = 0 
        # Trop compliqué à calculer pour l'instant sans utiliser self.game.result() pour simuler les coups (trop lent)
  
        # Coefficients de pondération
        coeff_material     = 0.65  # A determiner
        coeff_position     = 0.25  # A determiner
        coeff_protection   = 0.1   # A determiner

        # coeff_mobility     = 0.05  # A determiner
        # coeff_push         = 0.0   # A determiner

        total_score = coeff_material * score_material + coeff_position * score_position + coeff_protection * score_protection
        return total_score


    def alpha_beta_search(self, state):
        _, action = self.minimaxAlphaBeta(state, - float("inf"), float("inf"), self.max_depth, True)
        if action not in self.game.actions(state):
            print("Error: Action not in actions")
            exit(1)
        return action
    

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