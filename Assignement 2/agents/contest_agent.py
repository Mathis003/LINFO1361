from agents.agent import Agent
import random
import math


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
        return depth == self.max_depth or self.game.is_terminal(state)
    

    """
    Evaluates the given state and returns a score from the perspective of the agent's player.

    Args:
        state (ShobuState): The game state to evaluate.

    Returns:
        float: The evaluated score of the state.
    """
    def eval(self, state):
        min_pieces = [4, 4]
        for board in state.board:
            for i in range(2):
                min_pieces[i] = min(min_pieces[i], len(board[i]))
        
        return min_pieces[self.player] - min_pieces[1 - self.player]


    """
    Implements the alpha-beta pruning algorithm to find the best action.

    Args:
        state (ShobuState): The current game state.

    Returns:
        Utility: The utility of the best terminal state found.
    """
    def alpha_beta_search(self, state):
        utility, _ = self.max_value(state, - float("inf"), float("inf"), 0)
        return utility


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

        if self.is_cutoff(state, depth):
            return self.eval(state), None

        maxValue, bestMove = -float("inf"), None
        
        for action in self.game.actions(state):

            result_state = self.game.result(state, action)
            currValue, _ = self.min_value(result_state, alpha, beta, depth + 1)

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

        if self.is_cutoff(state, depth):
            return self.eval(state), None

        minValue, bestMove = float("inf"), None
        
        for action in self.game.actions(state):
            
            result_state = self.game.result(state, action)
            currValue, _ = self.max_value(result_state, alpha, beta, depth + 1)
            
            if currValue < minValue:
                minValue, bestMove = currValue, action
                beta = min(beta, minValue)

            if beta <= alpha:
                break
        
        return minValue, bestMove

"""
Node Class

A node in the MCTS tree.

Attributes:
    - parent (Node): The parent node of this node.
    - state (ShobuState): The game state represented by this node.
    - U (int): The total reward of the node. 
    - N (int): The number of times the node has been visited.
    - children (dict[Node, ShobuAction]): A dictionary mapping child nodes to their corresponding actions that lead to the state they represent.
"""
class Node:
    
    """
    Initializes a new Node object.

    Args:
        - parent (Node): The parent node of this node.
        - state (ShobuState): The game state represented by this node.
    """
    def __init__(self, parent, state):
        self.parent = parent
        self.state = state
        self.U = 0
        self.N = 0
        self.children = {}


"""
An agent that plays following your algorithm.

This agent extends the base Agent class, providing an implementation your agent.

Attributes:
    - player (int): The player id this agent represents.
    - game (ShobuGame): The game the agent is playing.
"""
class AI(Agent):
    
    """
    Initializes a new AI agent with a specified player and game.

    Args:
        - player (int): The player id this agent represents.
        - game (ShobuGame): The game the agent is playing.
    """
    def __init__(self, player, game):
        super().__init__(player, game)


    """
    Determines the next action to take in the given state.

    Args:
        - state (ShobuState): The current state of the game.
        - remaining_time (float): The remaining time in seconds that the agent has to make a decision.

    Returns:
        ShobuAction: The chosen action.
    """
    def play(self, state, remaining_time):
        self.uct(state)


    """
    Executes the UCT algorithm to find the best action from the current state.

    Args:
        state (ShobuState): The current state of the game.

    Returns:
        ShobuAction: The action leading to the best-perceived outcome based on UCT algorithm.
    """
    def uct(self, state):

        root = Node(None, state)
        root.children = { Node(root, self.game.result(root.state, action)): action for action in self.game.actions(root.state) }

        # Perform the UCT algorithm for a set number of iterations
        for _ in range(1):
            leaf = self.select(root)
            child = self.expand(leaf)
            result = self.simulate(child.state)
            self.back_propagate(result, child)

        # Choose the action with the highest number of visits
        max_state = max(root.children, key=lambda n: n.N)
        return root.children.get(max_state)


    """
    Selects a leaf node using the UCB1 formula to maximize exploration and exploitation.
    The function recursively selects the children of the node that maximise the UCB1 score, exploring the most promising 
    path in the game tree. It stops when a leaf is found and returns it. A leaf is either a node in a terminal state, 
    or a node with a child for which no simulation has yet been performed.

    Args:
        node (Node): The node to select from.

    Returns:
        Node: The selected leaf node.
    """
    def select(self, node):
        
        if self.game.is_terminal(node.state) or [child for child in node.children.keys() if child.N == 0] != []:
            return node

        return self.select(max(node.children, key=self.UCB1))

    
    """
    Expands a node by adding a child node to the tree for an unexplored action.

    The function returns one of the children of the node for which no simulation has yet been performed. 
    In addition, the function must initialize all the children of that child node in the child's "children" dictionary. 
    If the node is in a terminal state, the function returns itself, indicating that the node can no longer be expanded.

    Args:
        node (Node): The node to expand. This node represents the current state from which we want to explore possible actions.

    Returns:
        Node: The child node selected. If the node is at a terminal state, the node itself is returned.
    """
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
        

    """
    Simulates a random play-through from the given state to a terminal state.

    Args:
        state (ShobuState): The state to simulate from.

    Returns:
        The utility value of the resulting terminal state in the point of view of the opponent in the original state.
    """
    def simulate(self, state):

        alphaBetaAgent = AlphaBetaAgent(state.to_move, self.game, 3)
        utility = alphaBetaAgent.play(state, 100)
        return -utility
        
        # MAX_ITERATION = 500
        # currIteration = 0
        # opponent_player = 1 - state.to_move

        # # Simulate a random play-through from the given state to a terminal state
        # while not self.game.is_terminal(state) and currIteration < MAX_ITERATION:
        #     available_actions = self.game.actions(state)
        #     random_action = random.choice(available_actions)
        #     state = self.game.result(state, random_action)
        #     currIteration += 1

        # return self.game.utility(state, opponent_player)
    

    """
    Propagates the result of a simulation back up the tree, updating node statistics.

    This method is responsible for updating the statistics for each node according to the result of the simulation. 
    It recursively updates the U (utility) and N (number of visits) values for each node on the path from the given 
    node to the root. The utility of a node is only updated if it is a node that must contain the win rate of the 
    player who won the simulation, otherwise the utility is not modified.

    Args:
        result (float): The result of the simulation.
        node (Node): The node to start backpropagation from.
    """
    def back_propagate(self, result, node):
        if node:
            node.N += 1
            if result == 1:
                node.U += 1
            self.back_propagate(-result, node.parent)


    """
    Calculates the UCB1 value for a given node.

    Args:
        node (Node): The node to calculate the UCB1 value for.

    Returns:
        float: The UCB1 value of the node. Returns infinity if the node has not been visited yet.
    """
    def UCB1(self, node):
        
        # If the node has not been visited yet
        if node.N == 0:
            return float('inf')
        
        # Calculate the UCB1 value for the node (Tradeoff between exploitation and exploration)
        exploitation = node.U / node.N
        exploration = math.sqrt(math.log(node.parent.N) / node.N)
        C = math.sqrt(2)

        return exploitation + C * exploration