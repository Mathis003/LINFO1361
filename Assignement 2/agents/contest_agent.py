from agent import Agent
import time

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
    Performs a switch of the colors of the stones on the game board.
    """
    def switchColorsStones(self, board):
        newBoard = ""
        for tile in board:
            if tile == "o":
                newBoard += "x"
            elif tile == "x":
                newBoard += "o"
            else:
                newBoard += "."
        return newBoard

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
    def get_FirstSymmetry(self, board, transpositionTable):
        first_board  = board[:16]
        second_board = board[16:32]
        third_board  = board[32:48]
        fourth_board = board[48:]

        # SAME_BOARD
        entry = transpositionTable.get(board)
        if entry is not None: return entry

        # VERTICAL_ALL
        newBoard = self.get_vertSymmetricBoard(first_board) + self.get_vertSymmetricBoard(second_board) + self.get_vertSymmetricBoard(third_board) + self.get_vertSymmetricBoard(fourth_board)
        entry = transpositionTable.get(newBoard)
        if entry is not None: return entry

        # DIAGONAL_ALL
        newBoard = self.get_diagSymmetricBoard(first_board) + self.get_diagSymmetricBoard(second_board) + self.get_diagSymmetricBoard(third_board) + self.get_diagSymmetricBoard(fourth_board)
        entry = transpositionTable.get(newBoard)
        if entry is not None: return entry

        # DIAGONAL_INVERSE__ALL
        newBoard = self.get_diagInverseSymmetricBoard(first_board) + self.get_diagInverseSymmetricBoard(second_board) + self.get_diagInverseSymmetricBoard(third_board) + self.get_diagInverseSymmetricBoard(fourth_board)
        entry = transpositionTable.get(newBoard)
        if entry is not None: return entry

        # VERTICAL_SWITCH_HOME  
        newBoard = second_board + first_board + third_board + fourth_board
        entry = transpositionTable.get(newBoard)
        if entry is not None: return entry

        # VERTICAL_SWITCH_OPPONENT
        newBoard = first_board + second_board + fourth_board + third_board
        entry = transpositionTable.get(newBoard)
        if entry is not None: return entry
        
        # VERTICAL_SWITCH_ALL
        newBoard = second_board + first_board + fourth_board + third_board
        entry = transpositionTable.get(newBoard)
        if entry is not None: return entry
        
        # ROTATION_90_Left_ALL
        newBoard = self.rotateLeftBoard(first_board) + self.rotateLeftBoard(second_board) + self.rotateLeftBoard(third_board) + self.rotateLeftBoard(fourth_board)
        entry = transpositionTable.get(newBoard)
        if entry is not None: return entry
        
        # ROTATION_180_Left_ALL
        newBoard = self.get_horizSymmetricBoard(first_board) + self.get_horizSymmetricBoard(second_board) + self.get_horizSymmetricBoard(third_board) + self.get_horizSymmetricBoard(fourth_board)
        entry = transpositionTable.get(newBoard)
        if entry is not None: return entry
        
        # ROTATION_270_Left_ALL
        newBoard = self.rotateRightBoard(first_board) + self.rotateRightBoard(second_board) + self.rotateRightBoard(third_board) + self.rotateRightBoard(fourth_board)
        entry = transpositionTable.get(newBoard)
        if entry is not None: return entry
        
        newBoard = self.switchColorsStones(board)
        entry = transpositionTable.get(newBoard)
        if entry is not None:
            entry["value"] = - entry["value"]
            return entry
        return None
            
    def getEntry_StoredTT(self, board, transpositionTable):        
        return self.get_FirstSymmetry(board, transpositionTable)




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

        self.TT = TranspositionTable()
        self.symmetryComparer = SymmetryComparer()
        self.max_depth = 15

        self.total_time = 0.0
        self.nb_play    = 0

        self.MaxTimeALlowedPerMove = 15.0
        self.timeReached = False

        self.best_move = None

        self.best_iter_eval = - float("inf")
        self.best_iter_move = None

        self.first_turn_iter = True

        self.currDepth = 0

    # """
    # Get the number of pieces for each player in the game.
    # """
    # def getPieces(self, boards):
    #     nb_white_pieces, nb_black_pieces = 0, 0
    #     for board in boards:
    #         nb_white_pieces += len(board[0])
    #         nb_black_pieces += len(board[1])
    #     return (nb_white_pieces, nb_black_pieces)

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
        if self.nb_play == 1 and self.player == 0:
            return state.actions[0]._replace(active_board_id=3, passive_board_id=0, active_stone_id=0, passive_stone_id=0, direction=5, length=1)
        return self.iterativeDeepeningAlphaBeta(state)
    
    """
    Check if the state is a cutoff state.
    """
    def is_cutoff(self, state, depth):
        return depth == 0 or self.game.is_terminal(state)
    
    """
    Evaluate the state using the evaluation function.
    The evaluation function is a weighted sum of the material advantage, the positional advantage and the protection advantage.
    """
    def eval(self, state):
        board    = state.board
        player   = self.player
        opponent = 1 - player

        if self.game.is_terminal(state):
            return 999999999 * self.game.utility(state, self.player)
        
        positions = {player: [list(board[i][player]) for i in range(4)], opponent: [list(board[i][opponent]) for i in range(4)]}
        
        def materialScore():
            score_material_all = 0
            min_score_material_all, max_score_material_all = -12, 12
            nbPieces_min = [4, 4]
            min_score_material_min, max_score_material_min = -3, 3
            for i in range(4):
                score_material_all += len(positions[player][i]) - len(positions[opponent][i])
                nbPieces_min[player]   = min(len(positions[player][i]), nbPieces_min[player])
                nbPieces_min[opponent] = min(len(positions[opponent][i]), nbPieces_min[opponent])
            score_material_min = nbPieces_min[player] - nbPieces_min[opponent]

            score_material_all = (score_material_all - min_score_material_all) / (max_score_material_all - min_score_material_all)
            score_material_min = (score_material_min - min_score_material_min) / (max_score_material_min - min_score_material_min)
            score_material = 0.3 * score_material_all + 0.7 * score_material_min 
            return score_material
        
        def centeringPositionScore():
            score_position = 0
            min_score_position, max_score_position = -24, 24
            centering_positions = [5, 6, 9, 10]
            best_centering_positions = {0: [9, 10], 1: [5, 6]}
            best_board = {0: [2, 3], 1: [0, 1]}
            for i in range(4):
                for position in positions[player][i]:
                    if position in centering_positions:
                        score_position += 1
                        if (i in best_board[player]): score_position += 1
                        if (position in best_centering_positions[player]): score_position += 2
                for position in positions[opponent][i]:
                    if position in centering_positions:
                        score_position -= 1
                        if (i in best_board[opponent]): score_position -= 1
                        if (position in best_centering_positions[opponent]): score_position -= 2

            score_position = (score_position - min_score_position) / (max_score_position - min_score_position)
            return score_position

        def extraPositionScore():
            score_extra_position = 0
            min_score_extra_position, max_score_extra_position = -80, 80
            best_position = {0: [13, 14], 1: [1, 2]}
            for i in range(4):
                for position in positions[player][i]:
                    passedHere = False
                    if position == best_position[player][0]:
                        if best_position[player][0] - 1 in positions[opponent][i]:
                            passedHere = True
                            score_extra_position += 5
                        if best_position[player][0] + 1 in positions[opponent][i]:
                            score_extra_position += 5
                        if passedHere: score_extra_position += 10
                    elif position == best_position[player][1]:
                        if best_position[player][1] - 1 in positions[opponent][i]:
                            passedHere = True
                            score_extra_position += 5
                        if best_position[player][1] + 1 in positions[opponent][i]:
                            score_extra_position += 5
                        if passedHere: score_extra_position += 10
                for position in positions[opponent][i]:
                    passedHere = False
                    if position == best_position[opponent][0]:
                        if best_position[opponent][0] - 1 in positions[player][i]:
                            passedHere = True
                            score_extra_position -= 5
                        if best_position[opponent][0] + 1 in positions[player][i]:
                            score_extra_position -= 5
                        if passedHere: score_extra_position -= 10
                    if position == best_position[opponent][1]:
                        if best_position[opponent][1] - 1 in positions[player][i]:
                            passedHere = True
                            score_extra_position -= 5
                        if best_position[opponent][1] + 1 in positions[player][i]:
                            score_extra_position -= 5
                        if passedHere: score_extra_position -= 10

            score_extra_position = (score_extra_position - min_score_extra_position) / (max_score_extra_position - min_score_extra_position)
            return score_extra_position

        def interposedPositionScore():
            score_interpose_position = 0
            min_score_interpose_position, max_score_interpose_position = -16, 16
            rangePositions = [i for i in range(16)]
            offsets = [[-1, 1], [-3, 3],[-5, 5], [-4, 4]]
            for i in range(4):
                for position in positions[player][i]:
                    for offsetDir in offsets:
                        pos1 = position + offsetDir[0]
                        pos2 = position + offsetDir[1]
                        if (pos1 in rangePositions and pos2 in rangePositions and pos1 in positions[opponent][i] and pos2 in positions[opponent][i]): score_interpose_position += 1
                for position in positions[opponent][i]:
                    for offsetDir in offsets:
                        pos1 = position + offsetDir[0]
                        pos2 = position + offsetDir[1]
                        if (pos1 in rangePositions and pos2 in rangePositions and pos1 in positions[player][i] and pos2 in positions[player][i]): score_interpose_position -= 1
            
            score_interpose_position = (score_interpose_position - min_score_interpose_position) / (max_score_interpose_position - min_score_interpose_position)
            return score_interpose_position
        
        def mobilityScore():
            min_score_mobility, max_score_mobility = -100, 100
            score_mobility = len(state.actions) - len(self.game.compute_actions(state.board, 1 - state.to_move))
            score_mobility = (score_mobility - min_score_mobility) / (max_score_mobility - min_score_mobility)
            return score_mobility if self.player == state.to_move else -score_mobility
        
        def attackPositionScore():
            score_attack_position = 0
            min_score_attack_position, max_score_attack_position = -16, 16
            best_tile =  {0: [8, 9, 10, 11, 12, 13, 14, 15], 1: {0, 1, 2, 3, 4, 5, 6, 7}}
            for i in range(4):
                for position in positions[player][i]:
                    if position in best_tile[player]: score_attack_position += 1
                for position in positions[opponent][i]:
                    if position in best_tile[opponent]: score_attack_position -= 1
            score_attack_position = (score_attack_position - min_score_attack_position) / (max_score_attack_position - min_score_attack_position)
            return score_attack_position
        
        score_material            = materialScore()
        score_centering           = centeringPositionScore()
        score_extra_position      = extraPositionScore()
        score_interposed_position = interposedPositionScore()
        score_mobility            = mobilityScore()
        score_attack_position     = attackPositionScore()

        coeff_material            = 0.6
        coeff_centering           = 0.1
        coeff_extra_position      = 0.1
        coeff_interposed_position = 0.1
        coeff_mobility            = 0.05
        coeff_attack_position     = 0.05

        total_score = coeff_material * score_material + coeff_centering * score_centering + coeff_extra_position * score_extra_position + coeff_interposed_position * score_interposed_position + coeff_mobility * score_mobility + coeff_attack_position * score_attack_position
        return total_score
  
    def moveReordering(self, state, actions):

        def capture_stone(state, action):
            player   = state.to_move
            opponent = 1 - player
            new_active_stone_id = action.active_stone_id + action.length * action.direction
            board_active = state.board[action.active_board_id]

            if new_active_stone_id not in board_active[opponent]: return False

            if action.length == 1:
                if (new_active_stone_id in [0, 3, 12, 15] or
                    (new_active_stone_id in [1, 2] and action.active_stone_id in [4, 5, 6, 7]) or
                    (new_active_stone_id in [13, 14] and action.active_stone_id in [8, 9, 10, 11]) or
                    (new_active_stone_id in [4, 8] and action.active_stone_id in [1, 5, 9, 13]) or
                    (new_active_stone_id in [7, 11] and action.active_stone_id in [2, 6, 10, 14])):
                    return True
            else:
                if action.active_stone_id in [0, 3, 12, 15]: return False
                if ((action.direction == 1 and action.active_stone_id in [1, 5, 9, 13]) or
                    (action.direction == -1 and action.active_stone_id in [2, 6, 10, 14]) or
                    (action.direction == 4 and action.active_stone_id in [4, 5, 6, 7]) or
                    (action.direction == -4 and action.active_stone_id in [8, 9, 10, 11]) or
                    (action.direction == 5 and action.active_stone_id in [4, 5, 1]) or
                    (action.direction == -5 and action.active_stone_id in [14, 10, 11]) or
                    (action.direction == 3 and action.active_stone_id in [7, 6, 2]) or
                    (action.direction == -3 and action.active_stone_id in [12, 9, 8])):
                    return True
            return False

        capturing_actions     = []
        non_capturing_actions = []
        for action in actions:
            capturing_actions.append(action) if capture_stone(state, action) else non_capturing_actions.append(action)
        actionsReordered = capturing_actions + non_capturing_actions
        if self.first_turn_iter and self.best_move is not None:
            actionsReordered.remove(self.best_move)
            actionsReordered.insert(0, self.best_move)
            self.first_turn_iter = False
        return actionsReordered


    def iterativeDeepeningAlphaBeta(self, state):
        startTimer = time.time()

        def alphaBetaSearch(state, alpha, beta, depth):

            def max_value(state, alpha, beta, depth):
                max_eval = - float("inf")
                actions = self.moveReordering(state, self.game.actions(state))
                for action in actions:
                    child_state = self.game.result(state, action)
                    currEval = alphaBetaSearch(child_state, alpha, beta, depth - 1)
                    if currEval > max_eval:
                        max_eval = currEval
                        if depth == self.currDepth: self.best_iter_move = action
                    if max_eval >= beta: return max_eval 
                    alpha = max(alpha, max_eval)
                return max_eval
        
            def min_value(state, alpha, beta, depth):    
                min_eval = float("inf")
                actions = self.moveReordering(state, self.game.actions(state))
                for action in actions:
                    child_state = self.game.result(state, action)
                    min_eval = min(min_eval, alphaBetaSearch(child_state, alpha, beta, depth - 1))
                    if min_eval <= alpha: return min_eval
                    beta = min(beta, min_eval)
                return min_eval
            
            hashBoard = self.hashBoard(state.board)
            tt_entry = self.symmetryComparer.get_FirstSymmetry(hashBoard, self.TT)
            if tt_entry is not None and tt_entry['depth'] >= depth:
                if tt_entry['flag'] == 'exact':
                    return tt_entry['value']
                elif tt_entry['flag'] == 'lowerbound':
                    alpha = max(alpha, tt_entry['value'])
                elif tt_entry['flag'] == 'upperbound':
                    beta = min(beta, tt_entry['value'])
                if alpha >= beta:
                    return tt_entry['value']
                
            if time.time() - startTimer >= self.MaxTimeALlowedPerMove or self.is_cutoff(state, depth):
                evalState = self.eval(state)
                tt_entry = {"depth": depth, "value": evalState}
                if (evalState <= alpha):
                    tt_entry["flag"] = 'lowerbound'
                elif (evalState >= beta):
                    tt_entry["flag"] = 'upperbound'
                else:
                    tt_entry["flag"] = 'exact'
                self.TT.set(hashBoard, tt_entry)
                return evalState
                
            return max_value(state, alpha, beta, depth) if state.to_move == self.player else min_value(state, alpha, beta, depth)

        self.best_move = None
        self.best_iter_move = None
        self.timeReached = False
        best_eval_state = - float("inf")
        for depth in range(1, self.max_depth + 1):
            self.currDepth = depth
            self.first_turn_iter = True
            eval_state = alphaBetaSearch(state, - float("inf"), float("inf"), depth)
            if eval_state > best_eval_state:
                best_eval_state = eval_state
                self.best_move = self.best_iter_move
                self.best_iter_move = None
            if self.timeReached:
                break
        self.total_time += time.time() - startTimer
        return self.best_move