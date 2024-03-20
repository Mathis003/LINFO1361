from agents.agent import Agent
import random
import math
from tensorflow.keras.models import load_model
import numpy as np

MODEL_PATH = "shobu_winner_prediction_model.h5"

class Node:
    
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.U = 0
        self.N = 0
        self.children = {}


class AI(Agent):
    
    def __init__(self, player, game):
        super().__init__(player, game)
        self.machine_learning_model = load_model(MODEL_PATH)
        self.turn = 0


    def play(self, state, remaining_time):
        self.turn += 1
        return self.uct(state)
    
    #################################
    #### MONTE-CARLO TREE SEARCH ####
    #################################

    def uct(self, state):

        root = Node(None, state)
        root.children = { Node(root, self.game.result(root.state, action)): action for action in self.game.actions(root.state) }

        # Perform the UCT algorithm for a set number of iterations
        if self.turn < 10:
            NB_ITERATIONS = 100
        else:
            NB_ITERATIONS = 1000

        for _ in range(NB_ITERATIONS):
            leaf = self.select(root)
            child = self.expand(leaf)
            result = self.simulate(child.state)
            self.back_propagate(result, child)

        # Choose the action with the highest number of visits
        max_state = max(root.children, key=lambda n: n.N)
        return root.children.get(max_state)


    def select(self, node):
        
        if self.game.is_terminal(node.state) or [child for child in node.children.keys() if child.N == 0] != []:
            return node

        return self.select(max(node.children, key=self.UCB1))

 
    def expand(self, node):

        if self.game.is_terminal(node.state):
            return node

        # Keep track of the children that have NOT been visited yet
        childrenNotVisited = [child for child in node.children.keys() if child.N == 0]
        if childrenNotVisited == []:
            # Initialize a new child node with a random action
            available_actions = self.game.actions(node.state)
            action = random.choice(available_actions)
            newState = self.game.result(node.state, action)
            childNode = Node(node, newState)
        else:
            # Select a random child node that has not been visited yet
            childNode = random.choice(childrenNotVisited)
            action = node.children[childNode]
        
        # Initialize all the children of the child node
        node.children[childNode] = action
        childNode.children = { Node(childNode, self.game.result(childNode.state, action)): action for action in self.game.actions(childNode.state) }

        return childNode
 

    def simulateRandom(self, state):
                
        MAX_ITERATION = 500
        currIteration = 0
        opponent_player = 1 - state.to_move

        # Simulate a random play-through from the given state to a terminal state
        while not self.game.is_terminal(state) and currIteration < MAX_ITERATION:
            available_actions = self.game.actions(state)
            random_action = random.choice(available_actions)
            state = self.game.result(state, random_action)
            currIteration += 1

        return self.game.utility(state, opponent_player)
    
    """ With Machine Learning Model """
    def simulate(self, state):

        if self.turn < 10:
            return self.simulateRandom(state)

        opponent_player = 1 - state.to_move

        board = np.zeros((8, 8))

        for i in range(2):
            for pos in state.board[0][i]:
                player = 1 if i == 0 else -1
                board[pos // 4][pos % 4] = player

        for i in range(2):
            for pos in state.board[1][i]:
                player = 1 if i == 0 else -1
                board[pos // 4][4 + pos % 4] = player
        
        for i in range(2):
            for pos in state.board[2][i]:
                player = 1 if i == 0 else -1
                board[4 + pos // 4][pos % 4] = player

        for i in range(2):
            for pos in state.board[2][i]:
                player = 1 if i == 0 else -1
                board[4 + pos // 4][4 + pos % 4] = player
        
        board = board.reshape(1, 8, 8, 1)

        predicted_winner = self.machine_learning_model.predict(board)[0][0]

        print(predicted_winner)

        # predicted_winner is the probability for the black player to win
        if opponent_player == 1:
            return predicted_winner
        else:
            return 1 - predicted_winner
    
    def back_propagate(self, result, node):
        if node:
            node.N += 1
            if self.turn < 10:
                if result == 1:
                    node.U += 1
                self.back_propagate(-result, node.parent)
            else:
                node.U += result
                self.back_propagate(1 - result, node.parent)


    def UCB1(self, node):
        
        # If the node has not been visited yet
        if node.N == 0:
            return float('inf')
        
        # Calculate the UCB1 value for the node (Tradeoff between exploitation and exploration)
        exploitation = node.U / node.N
        exploration = math.sqrt(math.log(node.parent.N) / node.N)
        C = math.sqrt(2)

        return exploitation + C * exploration
    
    ######################################
    #### ALPHA-BETA PRUNING ALGORITHM ####
    ######################################

    def alpha_beta_search(self, state):
        MAX_DEPTH = 3
        _, action = self.minimax(state, True, -float("inf"), float("inf"), MAX_DEPTH)
        return action

    def score_pieces(self, state):
        nb_pieces = [0, 0]
        for board in state.board:
            for i in range(2):
                nb_pieces[i] += len(board[i])
        
        return nb_pieces[self.player] - nb_pieces[1 - self.player]
    
    def score_position_pieces(self, state):

        # Si pierres connectées, score += 1
        scores = [0, 0]
        for board in state.board:
            for i in range(2):
                board_list = list(board[i])
                for j in range(len(board_list)):
                    pos_j = board_list[j]
                    for k in range(len(board_list)):
                        pos_k = board_list[k]
                        if pos_j == pos_k + 1 or pos_j == pos_k - 1 or pos_j == pos_k + 4 or pos_j == pos_k - 4:
                            scores[i] += 1

        # Si pierres au centre du plateau, score += 2
        for board in state.board:
            for i in range(2):
                board_list = list(board[i])
                for j in range(len(board_list)):
                    pos_j = board_list[j]
                    if pos_j == 5 or pos_j == 6 or pos_j == 9 or pos_j == 10:
                        scores[i] += 2

        # Si pierres a x possibilité de mouvement, score += factor * x
        factor = 1
        scores[self.player] = factor * len(self.game.compute_actions(state.board, self.player))
        scores[1 - self.player] = factor * len(self.game.compute_actions(state.board, 1 - self.player))

        return scores[self.player] - scores[1 - self.player]
    
    def eval(self, state):

        # Heuristics
        score_nb_pieces = self.score_pieces(state)
        score_position_pieces = self.score_position_pieces(state)

        # Coefficients for the heuristics
        a = 0.2
        b = 0.8

        total_score = a * score_nb_pieces + b * score_position_pieces
        return total_score
    

    def is_cutoff(self, state, depth):
        return depth == 0 or self.game.is_terminal(state)


    def minimax(self, state, MAXIMIZING_PLAYER, alpha, beta, depth):
        bestMove = None

        if self.is_cutoff(state, depth):
            return self.eval(state), bestMove

        if MAXIMIZING_PLAYER:
            maxValue = -float("inf")

            for action in self.game.actions(state):
                
                result_state = self.game.result(state, action)
                currValue, _ = self.minimax(result_state, False, alpha, beta, depth - 1)

                if maxValue < currValue:
                    maxValue, bestMove = currValue, action
                    alpha = max(alpha, maxValue)

                if beta <= alpha:
                    break

            return maxValue, bestMove
        
        else:
            minValue = float("inf")

            for action in self.game.actions(state):
                
                result_state = self.game.result(state, action)
                currValue, _ = self.minimax(result_state, True, alpha, beta, depth - 1)
                
                if currValue < minValue:
                    minValue, bestMove = currValue, action
                    beta = min(beta, minValue)

                if beta <= alpha:
                    break
            
            return minValue, bestMove