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
class Pacman(Problem):

    # Define the possible actions for a given state
    def actions(self, state):

        nbRows, nbCols = state.shape
        row_pac, col_pac = state.pos_pacman

        result = []
        
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
        
        newX, newY = action
        row_pac, col_pac = state.pos_pacman
        new_answer = state.answer

        if state.grid[newX][newY] == "F":
            new_answer -= 1
        
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

        move = "Move to ({}, {})".format(newX, newY)
        if new_answer == 0:
            move += " Goal State"

        return State(state.shape, tuple(new_grid), new_answer, move, action)

    # Check for goal state
    def goal_test(self, state):
        return state.answer == 0
        

###############
# State class #
###############
class State:

    def __init__(self, shape, grid, answer=None, move="Init", pos_pacman=None):
        self.shape = shape
        self.answer = answer
        self.grid = grid
        self.move = move
        
        # Strip : Begin
        self.pos_pacman = pos_pacman;
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell == 'P':
                    self.pos_pacman = (i, j)
                    break
            if self.pos_pacman is not None:
                break
        # Strip : End

    def __str__(self):
        s = self.move + "\n"
        for line in self.grid:
            s += "".join(line) + "\n"
        return s
    
    # Strip : Begin
    def __hash__(self):
        return hash(self.grid)

    def __eq__(self, other):
        return (isinstance(other, State) and self.grid == other.grid and self.answer == other.answer)
    # Strip : End

    # Needs for "uniform_cost_search()"
    # def __lt__(self, other):
    #     pass

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
    init_state = State(shape, tuple(initial_grid), initial_fruit_count, "Init")

    problem = Pacman(init_state)

    start_timer = time.perf_counter()

    # node, nb_explored, remaining_nodes = breadth_first_graph_search(problem)
    #node, nb_explored, remaining_nodes = depth_first_graph_search(problem)
    #node, nb_explored, remaining_nodes = breadth_first_tree_search(problem)
    #node, nb_explored, remaining_nodes = iterative_deepening_search(problem)
    #node, nb_explored, remaining_nodes = depth_first_tree_search(problem)
    node, nb_explored, remaining_nodes = depth_first_tree_search(problem)

    end_timer = time.perf_counter()

    # path = node.path()

    # for node in path:
    #     print(node.state)

    print("* Execution time:\t", str(end_timer - start_timer))
    print("* Path cost to goal:\t", node.depth, "moves")
    print("* # Nodes explored:\t", nb_explored)
    print("* Queue size at goal:\t",  remaining_nodes)
