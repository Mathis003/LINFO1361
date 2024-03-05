from agent import Agent
import random
import math


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
An agent that uses the UCT algorithm to determine the best move.

This agent extends the base Agent class, providing an implementation of the play
method that utilizes UCT version of the MCTS algorithm.

Attributes:
    - player (int): The player id this agent represents.
    - game (ShobuGame): The game the agent is playing.
    - iteration (int): The number of simulations to perform in the UCT algorithm.
"""
class UCTAgent(Agent):

    """
    Initializes a UCTAgent with a specified player, game, and number of iterations.

    Args:
        - player (int): The player id this agent represents.
        - game (ShobuGame): The game the agent is playing.
        - iteration (int): The number of simulations to perform in the UCT algorithm.
    """
    def __init__(self, player, game, iteration):
        super().__init__(player, game)
        self.iteration = iteration


    """
    Determines the next action to take in the given state.

    Args:
        - state (ShobuState): The current state of the game.
        - remaining_time (float): The remaining time in seconds that the agent has to make a decision.

    Returns:
        ShobuAction: The chosen action.
    """
    def play(self, state, remaining_time):
        return self.uct(state)


    """
    Executes the UCT algorithm to find the best action from the current state.

    Args:
        state (ShobuState): The current state of the game.

    Returns:
        ShobuAction: The action leading to the best-perceived outcome based on UCT algorithm.
    """
    def uct(self, state):

        root = Node(None, state)

        # Perform the UCT algorithm for a set number of iterations
        for _ in range(self.iteration):
            leaf = self.select(root)
            child = self.expand(leaf)
            result = self.simulate(child.state)
            self.back_propagate(result, child)

        # Choose the action with the highest number of visits
        max_state = max(root.children, key=lambda n: n.N)
        return root.children.get(max_state)


    """
    Selects a leaf node using the UCB1 formula to maximize exploration and exploitation.

    A node is considered a leaf if it has a potential child from which no simulation has yet been initiated or when the game is finished.

    Args:
        node (Node): The node to select from.

    Returns:
        Node: The selected leaf node.
    """
    def select(self, node):
        
        # or any(child.N == 0 for child in node.children.keys())
        if not node.children or self.game.is_terminal(node.state):
            return node
        
        return max(node.children, key=lambda x: self.UCB1(x))

    
    """
    Expands a node by adding a child node to the tree for an unexplored action.

    This function generates all possible actions from the current state represented by the node if they haven't been explored yet. 
    For each unexplored action, a new child node is created, representing the state resulting from that action. The function then 
    selects one of these new child nodes and returns it. If the node represents a terminal state it effectively returns the node itself, 
    indicating that the node cannot be expanded further.

    Args:
        node (Node): The node to expand. This node represents the current state from which we want to explore possible actions.

    Returns:
        Node: The newly created child node representing the state after an unexplored action. If the node is at a terminal state, the node itself is returned.
    """
    def expand(self, node):

        if self.game.is_terminal(node.state):
            return node
        
        unexplored_actions = [action for action in self.game.actions(node.state) if action not in node.children.values()]

        if not unexplored_actions:
            return node
        
        action = random.choice(unexplored_actions)
        next_state = self.game.result(node.state, action)
        child_node = Node(node, next_state)
        node.children[child_node] = action

        return child_node
    

    """
    Simulates a random play-through from the given state to a terminal state.

    Args:
        state (ShobuState): The state to simulate from.

    Returns:
        float: The utility value of the terminal state for the player to move.
    """
    def simulate(self, state):
        
        MAX_ITERATION = 500
        iteration = 0
        currentState = state

        while not self.game.is_terminal(currentState) and iteration < MAX_ITERATION:
            available_actions = self.game.actions(currentState)
            randomAction = random.choice(available_actions)
            currentState = self.game.result(currentState, randomAction)
            iteration += 1

        return self.game.utility(currentState, state.to_move)
    

    """
    Propagates the result of a simulation back up the tree, updating node statistics.

    Args:
        result (float): The result of the simulation.
        node (Node): The node to start backpropagation from.
    """
    def back_propagate(self, result, node):

        if node is None:
            return
        
        node.N += 1
        node.U += result
        self.back_propagate(1 - result, node.parent)


    """
    Calculates the UCB1 value for a given node.

    Args:
        node (Node): The node to calculate the UCB1 value for.

    Returns:
        float: The UCB1 value.
    """
    def UCB1(self, node):

        if node.N == 0:
            return float('inf')
        
        exploitation = node.U / node.N
        exploration = math.sqrt(math.log(node.parent.N) / node.N)
        C = math.sqrt(2)

        return exploitation + C * exploration