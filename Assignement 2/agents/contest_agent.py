from agents.agent import Agent

SAME_BOARD = 0

VERTICAL_FIRST_SECOND, VERTICAL_THIRD_FOURTH = 1, 2
VERTICAL_SWITCH_FIRST_SECOND, VERTICAL_SWITCH_THIRD_FOURTH, VERTICAL_SWITCH_ALL = 3, 4, 5
VERTICAL_FIRST, VERTICAL_SECOND, VERTICAL_THIRD, VERTICAL_FOURTH = 6, 7, 8, 9

HORIZONTAL_FIRST_SECOND, HORIZONTAL_THIRD_FOURTH = 10, 11
HORIZONTAL_FIRST, HORIZONTAL_SECOND, HORIZONTAL_THIRD, HORIZONTAL_FOURTH = 12, 13, 14, 15

DIAGONAL_FIRST_SECOND, DIAGONAL_THIRD_FOURTH = 16, 17
DIAGONAL_FIRST, DIAGONAL_SECOND, DIAGONAL_THIRD, DIAGONAL_FOURTH = 18, 19, 20, 21

DIAGONAL_INVERSE_FIRST_SECOND, DIAGONAL_INVERSE_THIRD_FOURTH = 22, 23
DIAGONAL_INVERSE_FIRST, DIAGONAL_INVERSE_SECOND, DIAGONAL_INVERSE_THIRD, DIAGONAL_INVERSE_FOURTH = 24, 25, 26, 27



#################################################
########### == Transposition Table == ###########
#################################################

"""
This class is used to store state of the game for a fixed number of pieces for each player.
There is methods to access, set, remove, clear, keys, values and items of the table.

The state is stored in a dictionary where the key is the hashed board and the value is a dictionary containing:
    - value       (float)       : The evaluation value of the state.
    - lowerbound  (float)       : The lowerbound of the value.
    - upperbound  (float)       : The upperbound of the value.
    - move        (ShobuAction) : The best move to play from this state.
    - depth       (int)         : The depth of the search when the state was stored.
"""
class TranspositionTable:
    
    """
    Initialize the table as an empty dictionary.
    """
    def __init__(self):
        self.table = {}

    """
    Get the value of the key in the table. 
    If the key is not in the table, return the default value.
    """
    def get(self, key, default_value=None):
        return self.table.get(key, default_value)

    """
    Set the value of the key in the table.
    """
    def set(self, key, value):
        self.table[key] = value
    
    """
    Check if the key is in the table.
    """
    def contain(self, key):
        return key in self.table
    
    """
    Remove the key from the table.
    """
    def remove(self, key):
        self.table.pop(key, None)

    """
    Clear the table.
    """
    def clear(self):
        self.table.clear()
    
    """
    Get the keys of the table.
    """
    def keys(self):
        return self.table.keys()

    """
    Get the values of the table.
    """
    def values(self):
        return self.table.values()

    """
    Get the items (= pair of (key, value)) of the table.
    """
    def items(self):
        return self.table.items()


#################################################
############ == SYMMETRY COMPARER == ############
#################################################
    
"""
This class is used for comparing game state symmetries and obtaining different symmetries of a game board.
"""
class SymmetryComparer:

    """
    Performs a left rotation of the game board.
    """
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
    
    """
    Apply a diagonal symmetry to the board.
    """
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
    
    """
    Obtains the board symmetric about the diagonal.
    """
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

    """
    Compares the symmetries of the game board with those stored in the transposition table.
    """
    def get_horizSymmetricBoard(self, board):
        return board[12:] + board[8:12] + board[4:8] + board[:4]
    
    """
    Obtains the vertical symmetries of the game board.
    """
    def get_vertSymmetricBoard(self, board):
        board = board[::-1]
        return board[12:] + board[8:12] + board[4:8] + board[:4]
    
    """
    Obtains the evaluated move for the game board from the transposition table.
    """
    def get_sameSymmetry(self, board, transpositionTable):
        tt_entry = transpositionTable.get(board)
        return [(SAME_BOARD, tt_entry)] if tt_entry is not None else []

    """
    Obtains the vertical symmetries of the game board.
    """
    def get_verticalSymmetry(self, board, transpositionTable):
        return self.get_symmetry(board, transpositionTable, self.get_vertSymmetricBoard, [VERTICAL_FIRST_SECOND, VERTICAL_THIRD_FOURTH, VERTICAL_FIRST, VERTICAL_SECOND, VERTICAL_THIRD, VERTICAL_FOURTH])

    """
    Obtains the horizontal symmetries of the game board.
    """
    def get_horizontalSymmetry(self, board, transpositionTable):
        return self.get_symmetry(board, transpositionTable, self.get_horizSymmetricBoard, [HORIZONTAL_FIRST_SECOND, HORIZONTAL_THIRD_FOURTH, HORIZONTAL_FIRST, HORIZONTAL_SECOND, HORIZONTAL_THIRD, HORIZONTAL_FOURTH])
    
    """
    Obtains the diagonal symmetries of the game board.
    """
    def get_diagonalSymmetry(self, board, transpositionTable):
       return self.get_symmetry(board, transpositionTable, self.get_diagSymmetricBoard, [DIAGONAL_FIRST_SECOND, DIAGONAL_THIRD_FOURTH, DIAGONAL_FIRST, DIAGONAL_SECOND, DIAGONAL_THIRD, DIAGONAL_FOURTH])

    """
    Obtains the diagonal inverse symmetries of the game board.
    """
    def get_diagonalInverseSymmetry(self, board, transpositionTable):
       return self.get_symmetry(board, transpositionTable, self.get_diagInverseSymmetricBoard, [DIAGONAL_INVERSE_FIRST_SECOND, DIAGONAL_INVERSE_THIRD_FOURTH, DIAGONAL_INVERSE_FIRST, DIAGONAL_INVERSE_SECOND, DIAGONAL_INVERSE_THIRD, DIAGONAL_INVERSE_FOURTH])

    """
    Obtains the symmetries of the game board.
    The symmetries are obtained by applying the specific symmetry function given in parameter to the game board.
    """
    def get_symmetry(self, board, transpositionTable, getSpecificSymmetry, symmetries):

        list_result = []

        first_board  = board[:16]
        second_board = board[16:32]
        third_board  = board[32:48]
        fourth_board = board[48:]

        partsBoard = [first_board, second_board, third_board, fourth_board]

        ### Partie spécifique pour la symétrie verticale ###
        if symmetries[0] == VERTICAL_FIRST_SECOND:

            newBoard = second_board + first_board + fourth_board + third_board
            entry = transpositionTable.get(newBoard)
            if entry is not None:
                list_result.append((VERTICAL_SWITCH_ALL, entry))
            
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
                list_result.append((symmetries[i], entry))

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
                list_result.append((symmetries[2 + i], entry))
        
        return list_result
    
    """
    Obtains the symmetric move from the move given in parameter.
    The symmetry is the one given in parameter.
    """
    def get_symmetricMove(self, symmetry, tt_entry):

        move = tt_entry["move"]

        change_direction_vert  = {-3: -5, 5: 3, 3: 5, -5: -3, 4: 4, -4: 4, 1: -1, -1: 1}
        change_direction_horiz = {1: 1, -1: -1, 4: -4, -4: 4, 5: -3, -3: 5, 3: -5, -5: 3}
        change_direction_diag  = {1: -1, -1: 1, 4: 4, -4: -4, 5: -5, -5: 5, 3: -3, -3: 3}

        change_stone_id_vert  = {0: 3, 4: 7, 8: 11, 12: 15, 1: 2, 5: 6, 9: 10, 13: 14, 2: 1, 6: 5, 10: 9, 14: 13, 3: 0, 7: 4, 11: 8, 15: 12}
        change_stone_id_horiz = {0: 12, 1: 13, 2: 14, 3: 15, 4: 8, 5: 9, 6: 10, 7: 11, 8: 4, 9: 5, 10: 6, 11: 7, 12: 0, 13: 1, 14: 2, 15: 3}
        change_stone_id_diag  = {0: 15, 1: 11, 2: 7, 3: 3, 4: 14, 5: 10, 6: 6, 7: 2, 8: 13, 9: 9, 10: 5, 11: 1, 12: 12, 13: 8, 14: 4, 15: 0}
        
        if symmetry == SAME_BOARD:
            return move
        
        symmetries = [VERTICAL_FIRST, VERTICAL_SECOND, VERTICAL_THIRD, VERTICAL_FOURTH]
        for i in range(4):
            if symmetry == symmetries[i]:
                if move.passive_board_id == i:
                    return move._replace(direction=change_direction_vert[move.direction], passive_stone_id=change_stone_id_vert[move.passive_stone_id])
                elif move.active_board_id == i:
                    return move._replace(direction=change_direction_vert[move.direction], active_stone_id=change_stone_id_vert[move.active_stone_id])
                return move
        
        symmetries = [HORIZONTAL_FIRST, HORIZONTAL_SECOND, HORIZONTAL_THIRD, HORIZONTAL_FOURTH]
        for i in range(4):
            if symmetry == symmetries[i]:
                if move.passive_board_id == i:
                    return move._replace(direction=change_direction_horiz[move.direction], passive_stone_id=change_stone_id_horiz[move.passive_stone_id])
                elif move.active_board_id == i:
                    return move._replace(direction=change_direction_horiz[move.direction], active_stone_id=change_stone_id_horiz[move.active_stone_id])
                return move

        symmetries = [HORIZONTAL_FIRST_SECOND, HORIZONTAL_THIRD_FOURTH]    
        for i in range(2):
            if symmetry == symmetries[i]:
                if move.passive_board_id == 2 * i or move.passive_board_id == 2 * i + 1:
                    return move._replace(direction=change_direction_horiz[move.direction], passive_stone_id=change_stone_id_horiz[move.passive_stone_id])
                if move.active_board_id == 2 * i or move.passive_board_id == 2 * i + 1:
                    return move._replace(direction=change_direction_horiz[move.direction], active_stone_id=change_stone_id_horiz[move.active_stone_id])
                return move
        
        symmetries = [VERTICAL_FIRST_SECOND, VERTICAL_THIRD_FOURTH]    
        for i in range(2):
            if symmetry == symmetries[i]:
                if move.passive_board_id == 2 * i or move.passive_board_id == 2 * i + 1:
                    return move._replace(direction=change_direction_vert[move.direction], passive_stone_id=change_stone_id_vert[move.passive_stone_id])
                elif move.active_board_id == 2 * i or move.passive_board_id == 2 * i + 1:
                    return move._replace(direction=change_direction_vert[move.direction], active_stone_id=change_stone_id_vert[move.active_stone_id])
                return move
        
        symmetries = [VERTICAL_SWITCH_FIRST_SECOND, VERTICAL_SWITCH_THIRD_FOURTH]
        for i in range(2):
            if symmetry == symmetries[i]:
                if move.passive_board_id == 2*i:
                    move = move._replace(passive_board_id=2*i+1)
                elif move.passive_board_id == 2*i+1:
                    move = move._replace(passive_board_id=2*i)
                if move.active_board_id == 2*i:
                    move = move._replace(active_board_id=2*i+1)
                elif move.active_board_id == 2*i+1:
                    move = move._replace(active_board_id=2*i)
                return move
  
        if symmetry == VERTICAL_SWITCH_ALL:
            if move.passive_board_id == 2:
                move = move._replace(passive_board_id=3)
            elif move.passive_board_id == 3:
                move = move._replace(passive_board_id=2)
            elif move.passive_board_id == 1:
                move = move._replace(passive_board_id=0)
            elif move.passive_board_id == 0:
                move = move._replace(passive_board_id=1)
            if move.active_board_id == 2:
                move = move._replace(active_board_id=3)
            elif move.active_board_id == 3:
                move = move._replace(active_board_id=2)
            elif move.active_board_id == 1:
                move = move._replace(active_board_id=0)
            elif move.active_board_id == 0:
                move = move._replace(active_board_id=1)
            return move
        
        symmetries = [DIAGONAL_FIRST, DIAGONAL_SECOND, DIAGONAL_THIRD, DIAGONAL_FOURTH]
        for i in range(4):
            if symmetry == symmetries[i]:
                if move.passive_board_id == i:
                    return move._replace(direction=change_direction_diag[move.direction], passive_stone_id=change_stone_id_diag[move.passive_stone_id])
                elif move.active_board_id == i:
                    return move._replace(direction=change_direction_diag[move.direction], active_stone_id=change_stone_id_diag[move.active_stone_id])
                return move
        
        symmetries = [DIAGONAL_FIRST_SECOND, DIAGONAL_THIRD_FOURTH]
        for i in range(2):
            if symmetry == symmetries[i]:
                if move.passive_board_id == 2*i or move.passive_board_id == 2*i+1:
                    return move._replace(direction=change_direction_diag[move.direction], passive_stone_id=change_stone_id_diag[move.passive_stone_id])
                if move.active_board_id == 2*i or move.active_board_id == 2*i+1:
                    return move._replace(direction=change_direction_diag[move.direction], active_stone_id=change_stone_id_diag[move.active_stone_id])
                return move
     
        return None
            
    """
    Obtains the best move from the transposition table that are symmetric to the board given in parameter.
    The best move is the one with the highest value if maximizingPlayer is True, else it is the one with the lowest value among all the symmetric state stored in the TT.
    """
    def getBestMove_StoredTT(self, board, transpositionTable, maximizingPlayer):
        
        list_result_same        = self.get_sameSymmetry(board, transpositionTable)
        list_result_vert        = self.get_verticalSymmetry(board, transpositionTable)
        list_result_horiz       = self.get_horizontalSymmetry(board, transpositionTable)
        list_result_diag        = self.get_diagonalSymmetry(board, transpositionTable)
        list_result_inverseDiag = self.get_diagonalInverseSymmetry(board, transpositionTable)

        bestResult   = - float("inf") if maximizingPlayer else float("inf")
        bestEntry    = None
        bestSymmetry = None

        for result in list_result_same + list_result_vert + list_result_horiz + list_result_diag + list_result_inverseDiag:
            
            entry = result[1]
            if maximizingPlayer:
                if bestResult < entry["value"]:
                    bestSymmetry = result[0]
                    bestResult   = entry["value"]
                    bestEntry    = entry
            else:
                if entry["value"] < bestResult:
                    bestSymmetry = result[0]
                    bestResult   = entry["value"]
                    bestEntry    = entry
        
        if bestEntry is None:
            return None, None
        
        return bestEntry, self.get_symmetricMove(bestSymmetry, bestEntry)


#################################################
################ == AI Player == ################
#################################################

"""
This class is used to implement the AI player for the Shobu game.
The AI player uses the alpha-beta search algorithm with transposition table to play the game.

The AI player has the following attributes:
    - player            (int)              : The player number of the AI.
    - game              (ShobuGame)        : The game object of the Shobu game.
    - explored          (dict)             : The dictionary containing the explored states of the game.
    - symmetryComparer  (SymmetryComparer) : The symmetry comparer used to compare the symmetries of the game board.
    - max_depth         (int)              : The maximum depth of the search in the alpha-beta algorithm.

The explored dictionary contains the states of the game for a fixed number of pieces for each player.
The key of the dictionary is the number of pieces for each player
and the value is a TranspositionTable object containing the states of the game for this number of pieces.
"""
class AI(Agent):

    def __init__(self, player, game):
        super().__init__(player, game)
        self.explored = {}
        self.symmetryComparer = SymmetryComparer()
        self.max_depth = 3 # To change if needed

    """
    Clear the old states of the game that are not needed anymore.
    The old states are the states with a number of pieces greater than the number of pieces of the current game.
    """
    def clear_oldStates(self, nb_pieces):
        keys = list(self.explored.keys())
        for key in keys:
            if key[0] > nb_pieces[0] or key[1] > nb_pieces[1]:
                del self.explored[key]

    """
    Get the number of pieces for each player in the game.
    """
    def getPieces(self, boards):
        nb_white_pieces, nb_black_pieces = 0, 0
        for board in boards:
            nb_white_pieces += len(board[0])
            nb_black_pieces += len(board[1])
        return (nb_white_pieces, nb_black_pieces)

    """
    Hash the game board to store it in the transposition table.
    """
    def hashBoard(self, boards):
        board_str = ""
        for board in boards:
            positions_white, positions_black = list(board[0]), list(board[1])
            for pos_idx in range(16):
                    if pos_idx in positions_white:
                        board_str += "o"
                    elif pos_idx in positions_black:
                        board_str += "x"
                    else:
                        board_str += "."
        return board_str

    """
    Play the move using the alpha-beta search algorithm.
    The clearing of the old states is done before playing the move.
    """
    def play(self, state, remaining_time):
        self.clear_oldStates(self.getPieces(state.board))
        return self.alpha_beta_search(state)
    
    """
    Compute the best move using the alpha-beta search algorithm with transposition table.
    """
    def alpha_beta_search(self, state):
        _, action = self.minimaxAlphaBetaWithTT(state, - float("inf"), float("inf"), self.max_depth, True)
        # if action not in self.game.actions(state):
        #     print("Error: Action not in actions")
        #     exit(1)
        return action
    
    """
    Check if the state is a cutoff state.
    """
    def is_cutoff(self, state, depth):
        return depth == 0 or self.game.is_terminal(state)

    """
    Evaluate the state using the evaluation function.
    The evaluation function is a weighted sum of the material advantage, the positional advantage and the protection advantage.
    """
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

        if nbPieces_min[player] == 0:
            return - float("inf")
        
        if nbPieces_min[opponent] == 0:
            return float("inf")

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

        max_score_attack = 32
        min_score_attack = -32
        score_attack = 0

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
                    if position + offset in positions_opponent:
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
                    if position + offset in positions_player:
                        score_protection -= 1

        # if debug:
            # print("score_protection : ", score_protection)
            # print("=======================================\n")
        
        score_protection = (score_protection - min_score_protection) / (max_score_protection - min_score_protection)
        score_attack     = (score_attack - min_score_attack) / (max_score_attack - min_score_attack)

        # Coefficients de pondération
        coeff_material     = 0.65  # A determiner
        coeff_position     = 0.25  # A determiner
        coeff_protection   = 0.05  # A determiner
        coeff_attack       = 0.05  # A determiner

        total_score = coeff_material * score_material + coeff_position * score_position + coeff_protection * score_protection + coeff_attack * score_attack
        return total_score
    
    """
    Compute the best move using the alpha-beta search algorithm with transposition table.
    """
    def minimaxAlphaBetaWithTT(self, state, alpha, beta, depth, maximizingPlayer):

        boardHashed = self.hashBoard(state.board)
        nbPieces = (boardHashed.count('o'), boardHashed.count('x'))
        TT = self.explored.get(nbPieces)

        tt_entry = None
        if TT is None:
            TT = TranspositionTable()
            self.explored[nbPieces] = TT
        else:
            tt_entry, move = self.symmetryComparer.getBestMove_StoredTT(boardHashed, TT, maximizingPlayer)
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
            value = - float("inf")
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
        
        lowerbound = - float("inf")
        upperbound = float("inf")

        if value <= alpha:
            upperbound = value
        
        if value >= beta:
            lowerbound = value

        if value > alpha and value < beta:
            upperbound = value
            lowerbound = value
        
        TT.set(boardHashed, {"value": value, "lowerbound": lowerbound, "upperbound": upperbound, "move": bestMove, "depth": depth})
        
        return value, bestMove