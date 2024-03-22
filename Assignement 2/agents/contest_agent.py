from agents.agent import Agent

class AI(Agent):
    
    def __init__(self, player, game):
        super().__init__(player, game)
        self.max_depth = 3
        self.explored = {}


    def play(self, state, remaining_time):
        return self.alpha_beta_search(state)
    

    def alpha_beta_search(self, state):
        strBoard = self.getStrRepresentation(state.board)
        nbPieces = (strBoard.count("o"), strBoard.count("x"))
        self.removeUselessExplored(nbPieces)

        # print("Explored: ", self.explored.keys())

        _, action = self.minimax(state, True, -float("inf"), float("inf"), self.max_depth)
        return action
    
    def isSymetric(self, thisBoard, otherBoard):

        # Same board
        if thisBoard == otherBoard:
            return True
        
        homeBoard1 = [thisBoard[:16], thisBoard[16:32]]
        otherBoard1 = [thisBoard[32:48], thisBoard[48:]]

        homeBoard2 = [otherBoard[:16], otherBoard[16:32]]
        otherBoard2 = [otherBoard[32:48], otherBoard[48:]]

        # Symetric board
        for i in range(2):
            if homeBoard1 == homeBoard2 and otherBoard1[0] == otherBoard2[1] and otherBoard1[1] == otherBoard2[0]:
                return True
            if homeBoard1[0] == homeBoard2[1] and homeBoard1[1] == homeBoard2[0] and otherBoard1 == otherBoard2:
                return True
            if homeBoard1[0] == homeBoard2[1] and homeBoard1[1] == homeBoard2[0] and otherBoard1[0] == otherBoard2[1] and otherBoard1[1] == otherBoard2[0]:
                return True
        
        return False


    def alreadyExplored(self, boardStr, nbPieces):
        if nbPieces in self.explored:
            for key, value in self.explored[nbPieces].items():
                if self.isSymetric(key, boardStr):
                    return value
        return None
    

    def removeUselessExplored(self, nbPieces):
        keys_to_remove = []
        for key in self.explored.keys():
            if key[0] > nbPieces[0] or key[1] > nbPieces[1]:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.explored[key]


    def getStrRepresentation(self, board):
        strBoard = ""
        for idxBoard in range(4):
            currBoard = board[idxBoard]
            for nbTile in range(16):
                if (nbTile in currBoard[0]):
                    strBoard += "o"
                elif (nbTile in currBoard[1]):
                    strBoard += "x"
                else:
                    strBoard += "."
        return strBoard


    def eval(self, state):
        min_pieces = [4, 4]
        for board in state.board:
            for i in range(2):
                min_pieces[i] = min(min_pieces[i], len(board[i]))
        
        return min_pieces[self.player] - min_pieces[1 - self.player]
    

    def is_cutoff(self, state, depth):
        return depth == 0 or self.game.is_terminal(state)

    # Score, Action
    def minimax(self, state, maximizing_player, alpha, beta, depth):

        strBoard = self.getStrRepresentation(state.board)
        nbPieces = (strBoard.count('o'), strBoard.count('x'))

        exploredAction = self.alreadyExplored(strBoard, nbPieces)
        if exploredAction is not None:
            return 0, exploredAction

        if self.is_cutoff(state, depth):
            return self.eval(state), None

        if maximizing_player:

            maxValue, bestMove = -float("inf"), None
        
            for action in self.game.actions(state):
                
                result_state = self.game.result(state, action)
                currValue, _ = self.minimax(result_state, False, alpha, beta, depth - 1)

                if maxValue < currValue:
                    maxValue, bestMove = currValue, action
                    alpha = max(alpha, maxValue)

                if beta <= alpha:
                    break

            if (nbPieces in self.explored):
                self.explored[nbPieces][strBoard] = bestMove
            else:
                self.explored[nbPieces] = {strBoard: bestMove}

            return maxValue, bestMove
        
        else:
            minValue, bestMove = float("inf"), None
        
            for action in self.game.actions(state):
                
                result_state = self.game.result(state, action)
                currValue, _ = self.minimax(result_state, True, alpha, beta, depth - 1)
                
                if currValue < minValue:
                    minValue, bestMove = currValue, action
                    beta = min(beta, minValue)

                if beta <= alpha:
                    break
            
            if (nbPieces in self.explored):
                self.explored[nbPieces][strBoard] = bestMove
            else:
                self.explored[nbPieces] = {strBoard: bestMove}

            return minValue, bestMove