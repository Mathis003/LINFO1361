"""
Name of the author(s):
- Charles Lohest <charles.lohest@uclouvain.be>
"""
import time
import sys

from search import *

#################
# Problem class #
#################
dico = {}
class Pacman(Problem):

    def getPos_Pacman(self, grid, nbRows, nbCols):
        for i in range(nbRows):
            for j in range(nbCols):
                if grid[i][j] == "P":
                    return (i, j)
        return None


    # Define the possible actions for a given state
    def actions(self, state):

        nbRows = state.shape[0]
        nbCols = state.shape[1]

        result = []

        (row_pac, col_pac) = self.getPos_Pacman(state.grid, nbRows, nbCols)

        for k in range(1, nbCols - col_pac):
            if (state.grid[row_pac][col_pac + k] == "#"):
                break
            else:
                result.append((row_pac, col_pac + k))

        for k in range(1, col_pac + 1):
            if (state.grid[row_pac][col_pac - k] == "#"):
                break
            else:
                result.append((row_pac, col_pac - k))
        
        for k in range(1, nbRows - row_pac):
            if (state.grid[row_pac + k][col_pac] == "#"):
                break
            else:
                result.append((row_pac + k, col_pac))
        
        for k in range(1, row_pac + 1):
            if (state.grid[row_pac - k][col_pac] == "#"):
                break
            else:
                result.append((row_pac - k, col_pac))
            
        return result
                        
    # Apply the action to the state and return the new state
    def result(self, state, action):

        nbRows = state.shape[0]
        nbCols = state.shape[1]

        (row_pac, col_pac) = self.getPos_Pacman(state.grid, nbRows, nbCols)

        new_answer = state.answer

        if state.grid[action[0]][action[1]] == "F":
            new_answer -= 1

        new_grid = []
        for i in range(nbRows):
            row = list(state.grid[i])
            if i == action[0]:
                row[action[1]] = "P"
            if i == row_pac:
                row[col_pac] = "."
            new_grid.append(tuple(row))

        move = "Move to ({}, {})".format(action[0], action[1])
        if new_answer == 0:
            move += " Goal State"

        return State(state.shape, tuple(new_grid), new_answer, move)

    
    # Check for goal state
    def goal_test(self, state):
        
        if state.answer == 0:
            return True
        return False 


###############
# State class #
###############
class State:

    def __init__(self, shape, grid, answer=None, move="Init State"):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s


def read_instance_file(filepath):
    with open(filepath) as fd:
        lines = fd.read().splitlines()
    shape_x, shape_y = tuple(map(int, lines[0].split()))
    initial_grid = [tuple(row) for row in lines[1:1 + shape_x]]
    initial_fruit_count = sum(row.count('F') for row in initial_grid)

    return (shape_x, shape_y), initial_grid, initial_fruit_count


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print(f"Usage: ./Pacman.py <path_to_instance_file>")
        exit(1)

    filepath = sys.argv[1]

    shape, initial_grid, initial_fruit_count = read_instance_file(filepath)
    init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init State")

    problem = Pacman(init_state)

    # Example of search
    start_timer = time.perf_counter()
    node, nb_explored, remaining_nodes = breadth_first_tree_search(problem)
    end_timer = time.perf_counter()

    # Example of print
    path = node.path()

    for n in path:
        # assuming that the __str__ function of state outputs the correct format
        print(n.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* #Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)
