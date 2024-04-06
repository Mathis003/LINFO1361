from agents.agent import Agent
import random
import time

"""
An agent that plays randomly.

This agent extends the base Agent class, providing an implementation a random agent.

Attributes:
    - player (int): The player id this agent represents.
    - game (ShobuGame): The game the agent is playing.
"""
class RandomAgent(Agent):

    def __init__(self, player, game):
        super().__init__(player, game)
        self.coup_i = 0
        self.time = [0] * 10000

        self.nodeExplored = 0

    def __str__(self):
        return "RandomAgent"
    
    """
    Determines randomly the next action to take in the given state.

    Args:
        - state (ShobuState): The current state of the game.
        - remaining_time (float): The remaining time in seconds that the agent has to make a decision.

    Returns:
        ShobuAction: The chosen action.
    """
    def play(self, state, remaining_time):
        start = time.time()
        actions = self.game.actions(state)

        if len(actions) == 0:
            raise Exception("No actions available")
        self.time[self.coup_i] = time.time() - start
        self.coup_i += 1
        return random.choice(actions)
