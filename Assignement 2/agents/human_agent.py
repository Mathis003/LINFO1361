from interface import convert_click_to_position, update_ui
from shobu import ShobuAction
from agents.agent import Agent


"""
An agent that plays following your movement.

This agent extends the base Agent class, providing an implementation your agent.

Attributes:
    player (int): The player id this agent represents (0 or 1).
"""
class HumanAgent(Agent):

    """
    Initializes a HumanAgent instance with a specified player.

    Args:
        player (int): The player ID this agent represents (0 or 1).
    """
    def __init__(self, player):
        self.player = player


    def get_human_move(self, state):
        highlight_squares = []

        # get stone for passive move
        passive_stone = None
        passive_board = None
        passive_board_id = None
        passive_stone_id = None
        print("Select passive stone")
        while passive_stone is None and passive_board is None:
            pos = convert_click_to_position()
            if pos is not None:
                board_idx, piece_idx = pos

                board_id = (abs(board_idx[0] - 1)) * 2 + board_idx[1]
                piece_id = (abs(piece_idx[0] - 3)) * 4 + piece_idx[1]

                if (board_id, piece_id) in [(b, p) for b, p, _, _, _, _ in state.actions]:
                    passive_stone = piece_idx
                    passive_board = board_idx
                    passive_board_id = board_id
                    passive_stone_id = piece_id
                    
            run = update_ui(state, text="Select passive stone")
            if run == -1:
                return None
            if run == -2:
                print("move reset")
                return -2
        highlight_squares.append((passive_board, passive_stone))

        # get direction and length for passive move
        direction = None
        length = None
        print("Select target square for passive move")
        while direction is None and length is None:
            pos = convert_click_to_position()
            if pos is not None:
                board_idx, piece_idx = pos

                board_id = (abs(board_idx[0] - 1)) * 2 + board_idx[1]
                piece_id = (abs(piece_idx[0] - 3)) * 4 + piece_idx[1]

                dir = (piece_id - passive_stone_id)
                le = 1
                if abs(dir) in [1, 3, 4, 5]:
                    le = 1
                elif abs(dir) in [2, 6, 8, 10]:
                    dir //= 2
                    le = 2
                else:
                    continue
                if board_id == passive_board_id and (passive_board_id, passive_stone_id, dir, le) in [(b, p, d, l) for b, p, _, _, d, l in state.actions]:
                    direction = dir
                    length = le
            run = update_ui(state, text="Select target passive move", highlight=highlight_squares)
            if run == -1:
                return None
            if run == -2:
                print("move reset")
                return -2
        highlight_squares.append((board_idx, piece_idx))

        # get stone for active move
        active_stone = None 
        active_board = None
        active_board_id = None
        active_stone_id = None
        print("Select active stone")
        while active_stone is None and active_board is None:
            pos = convert_click_to_position()
            if pos is not None:
                board_idx, piece_idx = pos
                
                board_id = (abs(board_idx[0] - 1)) * 2 + board_idx[1]
                piece_id = (abs(piece_idx[0] - 3)) * 4 + piece_idx[1]

                if (passive_board_id, passive_stone_id, board_id, piece_id, direction, length) in state.actions:
                    active_stone = piece_idx
                    active_board = board_idx
                    active_board_id = board_id
                    active_stone_id = piece_id

            run = update_ui(state, text="Select active stone", highlight=highlight_squares)
            if run == -1:
                return None
            if run == -2:
                return -2
        highlight_squares.append((active_board, active_stone))

        return ShobuAction(passive_board_id, passive_stone_id, active_board_id, active_stone_id, direction, length)


    """
    Determines the next action to take in the given state.

    Args:
        - state (ShobuState): The current state of the game.
        - remaining_time (float): The remaining time in seconds that the agent has to make a decision.

    Returns:
        ShobuAction: The chosen action.
    """
    def play(self, state, remaining_time):
        return self.get_human_move(state)