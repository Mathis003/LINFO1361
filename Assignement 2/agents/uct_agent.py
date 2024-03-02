from agents.agent import Agent
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
        
        # If the node is a terminal state or has no children or hasn't be explored yet (N == 0), return the node
        if self.game.is_terminal(node.state) or node.N == 0 or len(node.children) == 0:
            return node
        
        # Select the child node with the highest UCB1 value
        max_ucb = -1
        next_node = None
        for child_node in node.children.keys():
            child_ucb = self.UCB1(child_node)
            if max_ucb < child_ucb:
                max_ucb = child_ucb
                next_node = child_node

        # Recursively select the next node
        return self.select(next_node)
    
    
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

        # If the node is a terminal state, return the node
        if self.game.is_terminal(node.state):
            return node
        
        # Generate all possible actions from the current state
        actions = self.game.actions(node.state)

        unexplored_actions = []
        for action in actions:
            if action not in node.children.values():
                unexplored_actions.append(action)
        
        action_random = random.choice(unexplored_actions)
        new_state = self.game.result(node.state, action_random)
        new_node = Node(node, new_state)
        node.children[new_node] = action_random
        return new_node

        # For each unexplored action, create a new child node
        # for action in actions:
        #     if action not in node.children.values():
        #         new_state = self.game.result(node.state, action)
        #         new_node = Node(node, new_state)
        #         node.children[new_node] = action
        
        # Select one of the new child nodes
        # return random.choice(list(node.children.keys()))


    """
    Simulates a random play-through from the given state to a terminal state.

    Args:
        state (ShobuState): The state to simulate from.

    Returns:
        float: The utility value of the terminal state for the player to move.
    """
    def simulate(self, state):
        
        max_iter = 500
        for _ in range(max_iter):

            if self.game.is_terminal(state):
                return self.game.utility(state, self.player)
            
            action = random.choice(self.game.actions(state))
            state = self.game.result(state, action)
        
        # Return : ???
        return 0
    

    """
    Propagates the result of a simulation back up the tree, updating node statistics.

    Args:
        result (float): The result of the simulation.
        node (Node): The node to start backpropagation from.
    """
    def back_propagate(self, result, node):
        while node.parent is not None:
            node = node.parent
            node.N += 1
            node.U += result


    """
    Calculates the UCB1 value for a given node.

    Args:
        node (Node): The node to calculate the UCB1 value for.

    Returns:
        float: The UCB1 value.
    """
    def UCB1(self, node):
        C = math.sqrt(2)
        return node.U / node.N + C * math.sqrt(math.log(node.parent.N) / node.N) if node.N != 0 else float('inf')