from agents.agent import Agent

# Same board for all the boards
SAME = 0

VERTICAL_SWITCH_FIRST_SECOND = -1
VERTICAL_SWITCH_THIRD_FOURTH = -2
VERTICAL_SWITCH_FIRST_SECOND_THIRD_FOURTH = -3
DIAGONAL_FIRST_SECOND = -4
DIAGONAL_THIRD_FOURTH = -5
DIAGONAL_INVERSE_FIRST_SECOND = -6
DIAGONAL_INVERSE_THIRD_FOURTH = -7

# Symetries for all the boards
VERTICAL_ALL = 1
HORIZONTAL_ALL = 2
DIAGONAL_ALL = 3
DIAGONAL_INVERSE_ALL = 4

# Symetries for the first board
VERTICAL_FIRST = 5
HORIZONTAL_FIRST = 6
DIAGONAL_FIRST = 7
DIAGONAL_INVERSE_FIRST = 8

# Symetries for the second board
VERTICAL_SECOND = 9
HORIZONTAL_SECOND = 10
DIAGONAL_SECOND = 11
DIAGONAL_INVERSE_SECOND = 12

# Symetries for the third board
VERTICAL_THIRD = 13
HORIZONTAL_THIRD = 14
DIAGONAL_THIRD = 15
DIAGONAL_INVERSE_THIRD = 16

# Symetries for the fourth board
VERTICAL_FOURTH = 17
HORIZONTAL_FOURTH = 18
DIAGONAL_FOURTH = 19
DIAGONAL_INVERSE_FOURTH = 20

# Symetries for the first and second boards
VERTICAL_FIRST_SECOND = 21
HORIZONTAL_FIRST_SECOND = 22

# Symetries for the first and third boards
VERTICAL_FIRST_THIRD = 23
HORIZONTAL_FIRST_THIRD = 24

# Symetries for the second and fourth boards
VERTICAL_SECOND_FOURTH = 25
HORIZONTAL_SECOND_FOURTH = 26

# Symetries for the third and fourth boards
VERTICAL_THIRD_FOURTH = 27
HORIZONTAL_THIRD_FOURTH = 28


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


class SymmetryComparer:

    def __init__(self):
        pass

    def rotateLeftBoard(self, board):
        count = 0
        start_idx, idx = 3, 3
        newBoard = ""
        while count < 16:
            newBoard += board[idx]
            idx += 4
            if idx > 15:
                start_idx -= 1
                idx = start_idx
            count += 1
        return newBoard
    
    def get_diagSymmetricBoard(self, board):
        count = 0
        start_idx, idx = 15, 15
        newBoard = ""
        while count < 16:
            newBoard += board[idx]
            idx -= 4
            if idx < 0:
                start_idx -= 1
                idx = start_idx
            count += 1
        return newBoard
    
    def get_diagInverseSymmetricBoard(self, board):
        count = 0
        start_idx, idx = 0, 0
        newBoard = ""
        while count < 16:
            newBoard += board[idx]
            idx += 4
            if idx > 15:
                start_idx += 1
                idx = start_idx
            count += 1
        return newBoard

    def get_horizSymmetricBoard(self, board):
        return board[12:] + board[8:12] + board[4:8] + board[:4]
    
    def get_vertSymmetricBoard(self, board):
        board = board[::-1]
        return board[12:] + board[8:12] + board[4:8] + board[:4]
    
    def get_sameSymmetry(self, board, transpositionTable):
        tt_entry = transpositionTable.get(board)
        if tt_entry is not None:
            return [(SAME, tt_entry)]
        return []

    def get_verticalSymmetry(self, board, transpositionTable):
        return self.get_symmetry(board, transpositionTable, self.get_vertSymmetricBoard, [VERTICAL_FIRST_SECOND, VERTICAL_THIRD_FOURTH, VERTICAL_FIRST, VERTICAL_SECOND, VERTICAL_THIRD, VERTICAL_FOURTH])

    def get_horizontalSymmetry(self, board, transpositionTable):
        return self.get_symmetry(board, transpositionTable, self.get_horizSymmetricBoard, [HORIZONTAL_FIRST_SECOND, HORIZONTAL_THIRD_FOURTH, HORIZONTAL_FIRST, HORIZONTAL_SECOND, HORIZONTAL_THIRD, HORIZONTAL_FOURTH])
    
    def get_diagonalSymmetry(self, board, transpositionTable):
       return self.get_symmetry(board, transpositionTable, self.get_diagSymmetricBoard, [DIAGONAL_FIRST_SECOND, DIAGONAL_THIRD_FOURTH, DIAGONAL_FIRST, DIAGONAL_SECOND, DIAGONAL_THIRD, DIAGONAL_FOURTH])

    def get_diagonalInverseSymmetry(self, board, transpositionTable):
       return self.get_symmetry(board, transpositionTable, self.get_diagInverseSymmetricBoard, [DIAGONAL_INVERSE_FIRST_SECOND, DIAGONAL_INVERSE_THIRD_FOURTH, DIAGONAL_INVERSE_FIRST, DIAGONAL_INVERSE_SECOND, DIAGONAL_INVERSE_THIRD, DIAGONAL_INVERSE_FOURTH])

    def get_symmetry(self, board, transpositionTable, getSpecificSymmetry, symmetry):

        list_result = []

        first_board  = board[:16]
        second_board = board[16:32]
        third_board  = board[32:48]
        fourth_board = board[48:]

        partsBoard = [first_board, second_board, third_board, fourth_board]

        ### Partie spécifique pour la symétrie verticale ###
        if symmetry[0] == VERTICAL_FIRST_SECOND:

            newBoard = second_board + first_board + fourth_board + third_board
            entry = transpositionTable.get(newBoard)
            if entry is not None:
                list_result.append((VERTICAL_SWITCH_FIRST_SECOND_THIRD_FOURTH, entry))
            
            newBoard = second_board + first_board + third_board + fourth_board
            entry = transpositionTable.get(newBoard)
            if entry is not None:
                list_result.append((VERTICAL_SWITCH_FIRST_SECOND, entry))
            
            newBoard = first_board + second_board + fourth_board + third_board
            entry = transpositionTable.get(newBoard)
            if entry is not None:
                list_result.append((VERTICAL_SWITCH_THIRD_FOURTH, entry))
        

        # Symétrie par deux plateau (home boards / opponent boards)
        offset = 0
        for i in range(2):
            newBoard = ""
            for j in range(len(partsBoard)):
                if j not in [offset, 1 + offset]:
                    newBoard += partsBoard[j]
                else:
                    newBoard += getSpecificSymmetry(partsBoard[j])
            offset = 2
            entry = transpositionTable.get(newBoard)
            if entry is not None:
                list_result.append((symmetry[i], entry))

        # Symétrie pour un plateau individuel
        for i in range(len(partsBoard)):
            newBoard = ""
            for j in range(len(partsBoard)):
                if i != j:
                    newBoard += partsBoard[j]
                else:
                    newBoard += getSpecificSymmetry(partsBoard[j])

            entry = transpositionTable.get(newBoard)
            if entry is not None:
                list_result.append((symmetry[2 + i], entry))
        
        return list_result
    

    def get_symmetricMove(self, symmetry, tt_entry):

        move = tt_entry["move"]

        change_direction_vert  = {-3: -5, 5: 3, 3: 5, -5: -3, 4: 4, -4: 4, 1: -1, -1: 1}
        change_direction_horiz = {1: 1, -1: -1, 4: -4, -4: 4, 5: -3, -3: 5, 3: -5, -5: 3}
        change_direction_diag  = {1: -1, -1: 1, 4: 4, -4: -4, 5: -5, -5: 5, 3: -3, -3: 3}

        change_stone_id_vert = {0: 3, 4: 7, 8: 11, 12: 15, 1: 2, 5: 6, 9: 10, 13: 14, 2: 1, 6: 5, 10: 9, 14: 13, 3: 0, 7: 4, 11: 8, 15: 12}
        change_stone_id_horiz = {0: 12, 1: 13, 2: 14, 3: 15, 4: 8, 5: 9, 6: 10, 7: 11, 8: 4, 9: 5, 10: 6, 11: 7, 12: 0, 13: 1, 14: 2, 15: 3}
        change_stone_id_diag = {0: 15, 1: 11, 2: 7, 3: 3, 4: 14, 5: 10, 6: 6, 7: 2, 8: 13, 9: 9, 10: 5, 11: 1, 12: 12, 13: 8, 14: 4, 15: 0}
        
        if symmetry == SAME:
            return move
        
        symmetrys = [VERTICAL_FIRST, VERTICAL_SECOND, VERTICAL_THIRD, VERTICAL_FOURTH]
        for i in range(4):
            if symmetry == symmetrys[i]:
                if move.passive_board_id == i:
                    return move._replace(direction=change_direction_vert[move.direction], passive_stone_id=change_stone_id_vert[move.passive_stone_id])
                elif move.active_board_id == i:
                    return move._replace(direction=change_direction_vert[move.direction], active_stone_id=change_stone_id_vert[move.active_stone_id])
                return move
        
        symmetrys = [HORIZONTAL_FIRST, HORIZONTAL_SECOND, HORIZONTAL_THIRD, HORIZONTAL_FOURTH]
        for i in range(4):
            if symmetry == symmetrys[i]:
                if move.passive_board_id == i:
                    return move._replace(direction=change_direction_horiz[move.direction], passive_stone_id=change_stone_id_horiz[move.passive_stone_id])
                elif move.active_board_id == i:
                    return move._replace(direction=change_direction_horiz[move.direction], active_stone_id=change_stone_id_horiz[move.active_stone_id])
                return move

        symmetrys = [HORIZONTAL_FIRST_SECOND, HORIZONTAL_THIRD_FOURTH]    
        for i in range(2):
            move = None
            if symmetry == symmetrys[i]:
                if move.passive_board_id == 2 * i or move.passive_board_id == 2 * i + 1:
                    return move._replace(direction=change_direction_horiz[move.direction], passive_stone_id=change_stone_id_horiz[move.passive_stone_id])
                if move.active_board_id == 2 * i or move.passive_board_id == 2 * i + 1:
                    return move._replace(direction=change_direction_horiz[move.direction], active_stone_id=change_stone_id_horiz[move.active_stone_id])
                return move
        
        # symmetrys = [VERTICAL_FIRST_SECOND, VERTICAL_THIRD_FOURTH]    
        # for i in range(2):
        #     if symmetry == symmetrys[i]:
        #         if move.passive_board_id == 2 * i or move.passive_board_id == 2 * i + 1:
        #             return move._replace(direction=change_direction_vert[move.direction], passive_stone_id=change_stone_id_vert[move.passive_stone_id])
        #         elif move.active_board_id == 2 * i or move.passive_board_id == 2 * i + 1:
        #             return move._replace(direction=change_direction_vert[move.direction], active_stone_id=change_stone_id_vert[move.active_stone_id])
        #         return move
        
        # symmetrys = [VERTICAL_SWITCH_FIRST_SECOND, VERTICAL_SWITCH_THIRD_FOURTH]
        # for i in range(2):
        #     if symmetry == symmetrys[i]:
        #         if move.passive_board_id == 2*i:
        #             move = move._replace(passive_board_id=2*i+1)
        #         elif move.passive_board_id == 2*i+1:
        #             move = move._replace(passive_board_id=2*i)
        #         if move.active_board_id == 2*i:
        #             move = move._replace(active_board_id=2*i+1)
        #         elif move.active_board_id == 2*i+1:
        #             move = move._replace(active_board_id=2*i)
        #         return move
  
        # if symmetry == VERTICAL_SWITCH_FIRST_SECOND_THIRD_FOURTH:
        #     if move.passive_board_id == 2:
        #         move = move._replace(passive_board_id=3)
        #     elif move.passive_board_id == 3:
        #         move = move._replace(passive_board_id=2)
        #     elif move.passive_board_id == 1:
        #         move = move._replace(passive_board_id=0)
        #     elif move.passive_board_id == 0:
        #         move = move._replace(passive_board_id=1)
        #     if move.active_board_id == 2:
        #         move = move._replace(active_board_id=3)
        #     elif move.active_board_id == 3:
        #         move = move._replace(active_board_id=2)
        #     elif move.active_board_id == 1:
        #         move = move._replace(active_board_id=0)
        #     elif move.active_board_id == 0:
        #         move = move._replace(active_board_id=1)
        #     return move
        
        # symmetrys = [DIAGONAL_FIRST, DIAGONAL_SECOND, DIAGONAL_THIRD, DIAGONAL_FOURTH]
        # for i in range(4):
        #     if symmetry == symmetrys[i]:
        #         if move.passive_board_id == i:
        #             return move._replace(direction=change_direction_diag[move.direction], passive_stone_id=change_stone_id_diag[move.passive_stone_id])
        #         elif move.active_board_id == i:
        #             return move._replace(direction=change_direction_diag[move.direction], active_stone_id=change_stone_id_diag[move.active_stone_id])
        #         return move
        
        # symmetrys = [DIAGONAL_FIRST_SECOND, DIAGONAL_THIRD_FOURTH]
        # for i in range(2):
        #     if symmetry == symmetrys[i]:
        #         if move.passive_board_id == 2*i or move.passive_board_id == 2*i+1:
        #             return move._replace(direction=change_direction_diag[move.direction], passive_stone_id=change_stone_id_diag[move.passive_stone_id])
        #         if move.active_board_id == 2*i or move.active_board_id == 2*i+1:
        #             return move._replace(direction=change_direction_diag[move.direction], active_stone_id=change_stone_id_diag[move.active_stone_id])
        #         return move
     
        return move # Ne devrait pas arriver
            

    def getMove_StoredTT(self, board, transpositionTable, maximizingPlayer):

        list_result_same        = self.get_sameSymmetry(board, transpositionTable)
        list_result_vert        = self.get_verticalSymmetry(board, transpositionTable)
        list_result_horiz       = self.get_horizontalSymmetry(board, transpositionTable)
        list_result_diag        = self.get_diagonalSymmetry(board, transpositionTable)
        list_result_inverseDiag = self.get_diagonalInverseSymmetry(board, transpositionTable)

        bestResult   = - float("inf") if maximizingPlayer else float("inf")
        bestEntry    = None
        bestSymmetry = None

        for result in list_result_same + list_result_vert + list_result_horiz + list_result_diag + list_result_inverseDiag:
   
            if maximizingPlayer:
                if bestResult < result[1]["value"]:
                    bestSymmetry = result[0]
                    bestEntry    = result[1]
                    bestResult   = bestEntry["value"]
            else:
                if result[1]["value"] < bestResult:
                    bestSymmetry = result[0]
                    bestEntry    = result[1]
                    bestResult   = bestEntry["value"]
        
        if bestEntry is None:
            return None, None
        
        return bestEntry, self.get_symmetricMove(bestSymmetry, bestEntry)







class AI(Agent):

    def __init__(self, player, game):
        super().__init__(player, game)
        self.max_depth = 3
        self.explored = {}
        self.symmetryComparer = SymmetryComparer()


    def clear_oldStates(self, nb_pieces):
        keys = list(self.explored.keys())
        for key in keys:
            if key[0] > nb_pieces[0] or key[1] > nb_pieces[1]:
                del self.explored[key]


    def play(self, state, remaining_time):
        self.clear_oldStates(self.getPieces(state.board))
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
        _, action = self.minimaxAlphaBetaWithTT(state, - float("inf"), float("inf"), self.max_depth, True)
        if action not in self.game.actions(state):
            print("Error: Action not in actions")
            exit(1)
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
    

    def minimaxAlphaBetaWithTT(self, state, alpha, beta, depth, maximizingPlayer):

        boardHashed = self.hashBoard(state.board)
        nbPieces = (boardHashed.count('o'), boardHashed.count('x'))
        TT = self.explored.get(nbPieces)

        tt_entry = None
        if TT is None:
            TT = TranpositionTable()
            self.explored[nbPieces] = TT
        else:
            tt_entry, move = self.symmetryComparer.getMove_StoredTT(boardHashed, TT, maximizingPlayer)

            if tt_entry is not None and move is not None and tt_entry["depth"] >= depth:
                
                value = None
                if tt_entry["lowerbound"] >= beta:
                    value = tt_entry["lowerbound"]

                if tt_entry["upperbound"] <= alpha:
                    value = tt_entry["upperbound"]

                if value is not None:
                    return value, move
                
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
        
        TT.set(boardHashed, {"value": value, "lowerbound": lowerbound, "upperbound": upperbound, "move": bestMove, "symetrie": SAME, "depth": depth})
        
        return value, bestMove