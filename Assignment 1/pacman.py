"""
Name of the author(s):
- Charles Lohest <charles.lohest@uclouvain.be>
"""

"""
Student' name : 
- Mathis Delsart
"""

import time
import sys

from search import *
from Extra.interface import show

#################
# Problem class #
#################
"""
This class extends the Problem class from the search.py file.
It defines the problem of the Pacman game and implements the methods
to solve it using the uninformed search algorithms present in the search.py file.

The problem is defined by :
    - the initial state
    - the action(s)
    - the result of an action
    - the goal state(s)

"""
class Pacman(Problem):

    """
    Define the possible actions (= moves) for a given state of the problem.

    @param state: the current state of the problem
    @return: a list of the possible actions for the given state
    """
    def actions(self, state):

        nbRows, nbCols = state.shape

        # Add this attribute to the state class to avoid finding the position of the pacman at each state.
        row_pac, col_pac = state.pos_pacman

        result = []
        
        # Search for the possible moves in the 4 directions (up, down, left, right) and add them to the result list.
        # If a wall is encountered, stop the search in the corresponding direction.

        # Right move
        for k in range(1, nbCols - col_pac):
            if (state.grid[row_pac][col_pac + k] == "#"):
                break
            else:
                result.append((row_pac, col_pac + k))

        # Left move
        for k in range(1, col_pac + 1):
            if (state.grid[row_pac][col_pac - k] == "#"):
                break
            else:
                result.append((row_pac, col_pac - k))
        
        # Down move
        for k in range(1, nbRows - row_pac):
            if (state.grid[row_pac + k][col_pac] == "#"):
                break
            else:
                result.append((row_pac + k, col_pac))
        
        # Up move
        for k in range(1, row_pac + 1):
            if (state.grid[row_pac - k][col_pac] == "#"):
                break
            else:
                result.append((row_pac - k, col_pac))
            
        return result

    """
    Apply the given action to the given state and return the new state.

    @param state: the current state of the problem
    @param action: the action to apply to the state
    @return: the new state after applying the action
    """
    def result(self, state, action):
        
        newX, newY = action
        row_pac, col_pac = state.pos_pacman
        new_answer = state.answer

        # Decrease the number of remaining fruits if a new furit is eaten.
        if state.grid[newX][newY] == "F":
            new_answer -= 1
        
        # Create the new grid by replacing the old position of the pacman by a dot and the new position by the pacman.
        new_grid = []
        for i, row in enumerate(state.grid):
            if i != newX and i != row_pac:
                new_grid.append(row)
            else:
                new_row = list(row)
                if i == newX:
                    new_row[newY] = "P"
                if i == row_pac:
                    new_row[col_pac] = "."
                new_grid.append(tuple(new_row))

        # Create the new move name.
        move = "Move to ({}, {})".format(newX, newY)
        if new_answer == 0:
            move += " Goal State"

        return State(state.shape, tuple(new_grid), new_answer, move, action)

    """
    Check if the given state is a goal state.

    @param state: the current state of the problem.
    @return: True if the state is a goal state, False otherwise.
    """
    def goal_test(self, state):
        # True if the number of remaining fruits is 0 (goal state).
        return state.answer == 0
        

###############
# State class #
###############
"""
This class represents a state of the problem.
"""
class State:

    """
    Create a new state for the problem.
    """
    def __init__(self, shape, grid, answer=None, move="Init", pos_pacman=None):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move
        
        # Strip : Begin
        # Add this attribute to the class to avoid finding the position of the pacman at each state.
        self.pos_pacman = pos_pacman;
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 'P':
                    self.pos_pacman = (i, j)
                    break
            if self.pos_pacman is not None:
                break
        # Strip : End

    """
    Define the string representation of the state.
    """
    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s
    
    # Strip : Begin
    """
    Define the hash and equality functions for the state.
    Used to compare states and avoid duplicates in the search algorithms.
    """
    def __hash__(self):
        return hash(self.grid)

    def __eq__(self, other):
        return (isinstance(other, State) and self.grid == other.grid and self.answer == other.answer)
    # Strip : End

    # Needs for "uniform_cost_search()"
    # def __lt__(self, other):
    #     pass

"""
Read the instance file and return the shape of the grid, the initial grid and the initial number of fruits.
"""
def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()
    shape_x, shape_y = tuple(map(int, lines[0].split()))
    initial_grid = [tuple(row) for row in lines[1:1 + shape_x]]
    initial_fruit_count = sum(row.count('F') for row in initial_grid)

    return (shape_x, shape_y), initial_grid, initial_fruit_count


"""
Launch the search algorithms to solve the Pacman problem.
"""
if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print(f"Usage: ./Pacman.py <path_to_instance_file>")
        exit(1)

    # Get the path to the instance file from the command line arguments.
    filepath = sys.argv[1]

    # Read the instance file and create the initial state of the problem.
    shape, initial_grid, initial_fruit_count = read_instance_file(filepath)
    init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init")

    problem = Pacman(init_state)

    start_timer = time.perf_counter()

    node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)

    # Other search algorithms available in the search.py file.

    # node, nb_explored, remaining_nodes = depth_first_graph_search(problem)
    # node, nb_explored, remaining_nodes = breadth_first_tree_search(problem)
    # node, nb_explored, remaining_nodes = iterative_deepening_search(problem)
    # node, nb_explored, remaining_nodes = depth_first_tree_search(problem)
    # node, nb_explored, remaining_nodes = depth_first_tree_search(problem)

    end_timer = time.perf_counter()

    # Get the path from the initial state to the goal state.
    path = node.path()

    # Print the optimal path found by the search algorithm.
    for node in path:
        print(node.state)
        show(node)

    # Print the statistics of the search algorithm.
        
    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* # Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)