from agents.agent import Agent

import time

"""
Idea to implement :
    - Forward pruning : prune branches that are unlikely to be good or decrease the depth of the search for these branches
            => Maybe use ProbCut algorithm (probabilistic cut algorithm)
    - Move ordering : rearrange nodes before exploration in minimax (best apparent move first)
    - Iterative deepening to deal with timing (with transposition table, store best move from previous iteration to improve move ordering)
            => With fixed time limit, last iteration must usually be aborted
            => Always store the best move from the previous iteration in the transposition table
            => Try to predict if another iteration can be completed before the time runs out
            => Can use incomplete last iteration if at least one move searched
    - Transposition table with symmetries => replace existing results with new ones if TT is filled up
    - Quiescent search : search promising moves deeper, unpromising ones less deep (avoid “horizon effect”)
    - Parameter tuning for evaluation function – by machine learning
    - Killer move heuristic : store moves that cause beta cutoffs and try them first in the next iteration
    - Define a lookup table for the 5 / 10 first moves of the game (opening book)
"""

## Variables use for the symmetries of the game board ##

SAME_BOARD = 0

VERTICAL_ALL          = 1
DIAGONAL_ALL          = 2
DIAGONAL_INVERSE__ALL = 3

VERTICAL_SWITCH_HOME     = 4
VERTICAL_SWITCH_OPPONENT = 5
VERTICAL_SWITCH_ALL      = 6

ROTATION_90_Left_ALL  = 7
ROTATION_180_Left_ALL = 8  # = HORIZONTAL_ALL
ROTATION_270_Left_ALL = 9


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
        start_idx, idx = 12, 12
        newBoard = ""
        while count < 16:
            newBoard += board[idx]
            idx -= 4
            if idx < 0:
                start_idx += 1
                idx = start_idx
            count += 1
        return newBoard
    
    """
    Performs a right rotation of the game board.
    """
    def rotateRightBoard(self, board):
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
    Obtains the symmetries of the game board.
    The symmetries are obtained by applying the specific symmetry function given in parameter to the game board.
    """
    def get_AllSymmetry(self, board, transpositionTable):
        
        # !! Moyen de faire de la symétrie avec HOME board + OPPONENT board !! #
        # !! Mais pas avec deux HOME board ou deux OPPONENT board !! #

        list_result = []

        first_board  = board[:16]
        second_board = board[16:32]
        third_board  = board[32:48]
        fourth_board = board[48:]

        # SAME_BOARD
        self.addEntryIfStoredTT(transpositionTable, board, list_result, SAME_BOARD)

        # VERTICAL_ALL
        newBoard = self.get_vertSymmetricBoard(first_board) + self.get_vertSymmetricBoard(second_board) + self.get_vertSymmetricBoard(third_board) + self.get_vertSymmetricBoard(fourth_board)
        self.addEntryIfStoredTT(transpositionTable, newBoard, list_result, VERTICAL_ALL)

        # DIAGONAL_ALL
        newBoard = self.get_diagSymmetricBoard(first_board) + self.get_diagSymmetricBoard(second_board) + self.get_diagSymmetricBoard(third_board) + self.get_diagSymmetricBoard(fourth_board)
        self.addEntryIfStoredTT(transpositionTable, newBoard, list_result, DIAGONAL_ALL)

        # DIAGONAL_INVERSE__ALL
        newBoard = self.get_diagInverseSymmetricBoard(first_board) + self.get_diagInverseSymmetricBoard(second_board) + self.get_diagInverseSymmetricBoard(third_board) + self.get_diagInverseSymmetricBoard(fourth_board)
        self.addEntryIfStoredTT(transpositionTable, newBoard, list_result, DIAGONAL_INVERSE__ALL)

        # VERTICAL_SWITCH_HOME  
        newBoard = second_board + first_board + third_board + fourth_board
        self.addEntryIfStoredTT(transpositionTable, newBoard, list_result, VERTICAL_SWITCH_HOME)

        # VERTICAL_SWITCH_OPPONENT
        newBoard = first_board + second_board + fourth_board + third_board
        self.addEntryIfStoredTT(transpositionTable, newBoard, list_result, VERTICAL_SWITCH_OPPONENT)
        
        # VERTICAL_SWITCH_ALL
        newBoard = second_board + first_board + fourth_board + third_board
        self.addEntryIfStoredTT(transpositionTable, newBoard, list_result, VERTICAL_SWITCH_ALL)
        
        # ROTATION_90_Left_ALL
        newBoard = self.rotateLeftBoard(first_board) + self.rotateLeftBoard(second_board) + self.rotateLeftBoard(third_board) + self.rotateLeftBoard(fourth_board)
        self.addEntryIfStoredTT(transpositionTable, newBoard, list_result, ROTATION_90_Left_ALL)
        
        # ROTATION_180_Left_ALL
        newBoard = self.get_horizSymmetricBoard(first_board) + self.get_horizSymmetricBoard(second_board) + self.get_horizSymmetricBoard(third_board) + self.get_horizSymmetricBoard(fourth_board)
        self.addEntryIfStoredTT(transpositionTable, newBoard, list_result, ROTATION_180_Left_ALL)
        
        # ROTATION_270_Left_ALL
        newBoard = self.rotateRightBoard(first_board) + self.rotateRightBoard(second_board) + self.rotateRightBoard(third_board) + self.rotateRightBoard(fourth_board)
        self.addEntryIfStoredTT(transpositionTable, newBoard, list_result, ROTATION_270_Left_ALL)
        
        return list_result
    

    """
    Add the symmetric state to the list_result if the state is stored in the transposition table.
    """
    def addEntryIfStoredTT(self, transpositionTable, newBoard, list_result, symmetry):
        entry = transpositionTable.get(newBoard)
        if entry is not None:
            list_result.append((symmetry, entry))
    
    """
    Obtains the symmetric move from the move given in parameter.
    The symmetry is the one given in parameter.
    """
    def get_symmetricMove(self, move, symmetry):

        change_direction_vert         = {-3: -5, 5: 3, 3: 5, -5: -3, 4: 4, -4: 4, 1: -1, -1: 1}
        change_direction_horiz        = {1: 1, -1: -1, 4: -4, -4: 4, 5: -3, -3: 5, 3: -5, -5: 3}
        change_direction_diag         = {1: -1, -1: 1, 4: 4, -4: -4, 5: -5, -5: 5, 3: -3, -3: 3}
        change_direction_diag_inverse = {-3: -3, 3: 3, 5: -5, -5: 5, 1: -4, -4: 1, -1: 4, 4: -1}
        change_direction_rotatioLeft  = {4: -1, -4: 1, 1: 4, -1: -4, 5: 3, -3: 5, 3: -5, -5: -3}
        change_direction_rotatioRight = {4: 1, -4: -1, 1: -4, -1: 4, 5: -3, -3: -5, 3: 5, -5: 3}

        change_stone_id_vert          = {0: 3, 4: 7, 8: 11, 12: 15, 1: 2, 5: 6, 9: 10, 13: 14, 2: 1, 6: 5, 10: 9, 14: 13, 3: 0, 7: 4, 11: 8, 15: 12}
        change_stone_id_horiz         = {0: 12, 1: 13, 2: 14, 3: 15, 4: 8, 5: 9, 6: 10, 7: 11, 8: 4, 9: 5, 10: 6, 11: 7, 12: 0, 13: 1, 14: 2, 15: 3}
        change_stone_id_diag          = {0: 15, 1: 11, 2: 7, 3: 3, 4: 14, 5: 10, 6: 6, 7: 2, 8: 13, 9: 9, 10: 5, 11: 1, 12: 12, 13: 8, 14: 4, 15: 0}
        change_stone_id_diag_inverse  = {0: 15, 1: 11, 2: 7, 3: 3, 4: 14, 5: 10, 6: 6, 7: 2, 8: 13, 9: 9, 10: 5, 11: 1, 12: 12, 13: 8, 14: 4, 15: 0}
        change_stone_id_rotationLeft  = {0: 12, 1: 8, 2: 4, 3: 6, 4: 13, 5: 9, 6: 5, 7: 1, 8: 14, 9: 10, 10: 6, 11: 2, 12: 15, 13: 11, 14: 7, 15: 3}
        change_stone_id_rotationRight = {0: 3, 1: 7, 2: 11, 3: 13, 4: 2, 5: 6, 6: 10, 7: 14, 8: 1, 9: 5, 10: 9, 11: 13, 12: 0, 13: 4, 14: 8, 15: 12}
        

        if symmetry == SAME_BOARD:
            return move
        
        elif symmetry == VERTICAL_ALL:
            return move._replace(active_stone_id=change_stone_id_vert[move.active_stone_id],
                                 passive_stone_id=change_stone_id_vert[move.passive_stone_id],
                                 direction=change_direction_vert[move.direction])
        
        elif symmetry == DIAGONAL_ALL:
            return move._replace(active_stone_id=change_stone_id_diag[move.active_stone_id],
                                 passive_stone_id=change_stone_id_diag[move.passive_stone_id],
                                 direction=change_direction_diag[move.direction])
        
        elif symmetry == DIAGONAL_INVERSE__ALL:
            return move._replace(active_stone_id=change_stone_id_diag_inverse[move.active_stone_id],
                                 passive_stone_id=change_stone_id_diag_inverse[move.passive_stone_id],
                                 direction=change_direction_diag_inverse[move.direction])

        elif symmetry == VERTICAL_SWITCH_HOME:
            if move.passive_board_id == 0:
                move = move._replace(passive_board_id=1)
            elif move.passive_board_id == 1:
                move = move._replace(passive_board_id=0)
            
            if move.active_board_id == 0:
                move = move._replace(active_board_id=1)
            elif move.active_board_id == 1:
                move = move._replace(active_board_id=0)
            
            return move

        elif symmetry == VERTICAL_SWITCH_OPPONENT:
            if move.passive_board_id == 2:
                move = move._replace(passive_board_id=3)
            elif move.passive_board_id == 3:
                move = move._replace(passive_board_id=2)
            
            if move.active_board_id == 2:
                move = move._replace(active_board_id=3)
            elif move.active_board_id == 3:
                move = move._replace(active_board_id=2)
            
            return move
        
        elif symmetry == VERTICAL_SWITCH_ALL:
            if move.passive_board_id == 0:
                move = move._replace(passive_board_id=1)
            elif move.passive_board_id == 1:
                move = move._replace(passive_board_id=0)
            elif move.passive_board_id == 2:
                move = move._replace(passive_board_id=3)
            elif move.passive_board_id == 3:
                move = move._replace(passive_board_id=2)
            
            if move.active_board_id == 0:
                move = move._replace(active_board_id=1)
            elif move.active_board_id == 1:
                move = move._replace(active_board_id=0)
            elif move.active_board_id == 2:
                move = move._replace(active_board_id=3)
            elif move.active_board_id == 3:
                move = move._replace(active_board_id=2)
            
            return move
    
        elif symmetry == ROTATION_90_Left_ALL:
            return move._replace(active_stone_id=change_stone_id_rotationLeft[move.active_stone_id],
                                 passive_stone_id=change_stone_id_rotationLeft[move.passive_stone_id],
                                 direction=change_direction_rotatioLeft[move.direction])

        elif symmetry == ROTATION_180_Left_ALL:
            return move._replace(active_stone_id=change_stone_id_horiz[move.active_stone_id],
                                 passive_stone_id=change_stone_id_horiz[move.passive_stone_id],
                                 direction=change_direction_horiz[move.direction])
        
        elif symmetry == ROTATION_270_Left_ALL:
            return move._replace(active_stone_id=change_stone_id_rotationRight[move.active_stone_id],
                                 passive_stone_id=change_stone_id_rotationRight[move.passive_stone_id],
                                 direction=change_direction_rotatioRight[move.direction])

        else:
            print("Error: Symmetry not found")
            exit(1)
        
            
    """
    Obtains the best move from the transposition table that are symmetric to the board given in parameter.
    The best move is the one with the highest value if maximizingPlayer is True, else it is the one with the lowest value among all the symmetric state stored in the TT.
    """
    def getBestMove_StoredTT(self, board, transpositionTable, maximizingPlayer):
        
        bestResult   = - float("inf") if maximizingPlayer else float("inf")
        bestEntry    = None
        bestSymmetry = None

        for result in self.get_AllSymmetry(board, transpositionTable):
            
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
        
        return bestEntry, self.get_symmetricMove(bestEntry["move"], bestSymmetry)


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

        self.total_time = 0.0
        self.nb_play = 0

    """
    Clear the old states of the game that are not needed anymore.
    The old states are the states with a number of pieces greater than the number of pieces of the current game.
    """
    def clear_oldStates(self, nb_pieces):
        keys = list(self.explored.keys())
        for key in keys:
            if key[0] > nb_pieces[0] or key[1] > nb_pieces[1]:
                self.explored.pop(key, None)

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
        self.nb_play += 1
        self.clear_oldStates(self.getPieces(state.board))
        return self.search_alphaBeta(state)
    
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

        INF = 999999999
        if nbPieces_min[player] == 0:
            return - INF
        elif nbPieces_min[opponent] == 0:
            return INF

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

            for positions, sign in [(positions_player, 1), (positions_opponent, -1)]:
                for position in positions:
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
                        if position + offset in positions:
                            score_protection += sign

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
  

    # """
    # Iteratively deepening alpha-beta search algorithm.
    # """
    # def iterativeDeepeningAlphaBeta(self, state):
    #     bestEval, bestMove = - float("inf"), None
    #     for depth in range(1, self.max_depth + 1):
    #         currentEval, currentMove = self.choose_move(state, depth)
    #         if bestEval < currentEval:
    #             bestEval, bestMove = currentEval, currentMove
    #     return bestMove
    

    """
    Compute the best move using the alpha-beta search algorithm with transposition table.
    """
    def search_alphaBeta(self, state):

        def max_value(state, alpha, beta, depth):
            if self.is_cutoff(state, depth):
                return self.eval(state), None

            max_eval = - float("inf")
            best_action = None
            for action in self.game.actions(state):
                child_state = self.game.result(state, action)
                eval_child, _ = min_value(child_state, alpha, beta, depth - 1)
                if eval_child > max_eval:
                    max_eval = eval_child
                    best_action = action
                    if max_eval >= beta:
                        return max_eval, best_action
                    alpha = max(alpha, max_eval)
            return max_eval, best_action
    
        def min_value(state, alpha, beta, depth):
            if self.is_cutoff(state, depth):
                return self.eval(state), None
            
            min_eval = float("inf")
            best_action = None
            for action in self.game.actions(state):
                child_state = self.game.result(state, action)
                eval_child, _ = max_value(child_state, alpha, beta, depth - 1)
                if eval_child < min_eval:
                    min_eval = eval_child
                    best_action = action
                    if alpha >= min_eval:
                        return min_eval, best_action
                    beta = min(beta, min_eval)
            return min_eval, best_action

        start = time.time()
        _, action = max_value(state, - float("inf"), float("inf"), self.max_depth)
        end = time.time()
        self.total_time += end - start
        return action