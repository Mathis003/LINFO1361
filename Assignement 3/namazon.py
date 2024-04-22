from search import *
import time

"""
NAmazonsProblem class for the NAmazons problem.

The problem is to place N amazons on an NxN board with none attacking each other.
The board must be filled column by column, from left to right.
The rules are the following:
    - No two amazons can be in the same row
    - No two amazons can be in the same diagonal
    - No two amazons can be in the same 'special knight moves' (2x3/3x2/4x1/1x4)
"""
class NAmazonsProblem(Problem):
    
    """
    Attributes:
        - initial_state: the initial state of the problem
        - goal_state: NOT USED (because the goal to this problem is not a specific state)
        - N: the size of the board
    """
    def __init__(self, N, initial_state):
        Problem.__init__(self, initial_state)
        self.N = N

    """
    Get the possible actions from a state.

    An action is a row index where an empress can be placed in the current column.
    The current column is the first empty column in the state and is specified in its attributes.
    The action must respect the rules of the problem.

    @param state: The current state of the problem.
    @return: The list of possible actions.
    """
    def actions(self, state):
        actions = []
        for action in range(self.N):
            # Check if the action is valid
            valid_action = True
            for col in range(state.colEmpty):
                diff_col = state.colEmpty - col
                diff_row = abs(state.rows[col] - action)
                if diff_row == 0 or diff_row == diff_col: valid_action = False; break # Same row or same diagonal
                if diff_col == 1 and diff_row == 4: valid_action = False; break # Special 'knight moves' 1x4
                if diff_col == 4 and diff_row == 1: valid_action = False; break # Special 'knight moves' 4x1
                if diff_col == 2 and diff_row == 3: valid_action = False; break # Special 'knight moves' 2x3
                if diff_col == 3 and diff_row == 2: valid_action = False; break # Special 'knight moves' 3x2
            
            if valid_action: actions.append(action)
        return actions
    
    """
    Apply an action to a state and return the new state.
    The action to apply is to place an empress in the current column at the specified row.

    @param state: The current state of the problem.
    @param row: The row index where to place the empress.

    @return: The new state after applying the action.
    """
    def result(self, state, row):
        return State(state.rows[:state.colEmpty] + [row] + [-1 for _ in range(state.colEmpty + 1, self.N)], state.colEmpty + 1)

    """
    Check if a state is a goal state.
    A state is a goal state if the last column are filled with an empress (and thus all the columns through the modeling of the problem).

    @param state: The state to check.

    @return: True if the state is a goal state, False otherwise.
    """
    def goal_test(self, state):
        return True if state.colEmpty == self.N else False
    
    """
    Would putting two Amazons in (row1, col1) and (row2, col2) conflict ?
    A conflict is if the two empresses are in the same row, column or diagonal.
    A conflict is also if the two empresses are in the same 'special knight moves' (2x3/3x2/4x1/1x4).

    @param row1: The row index of the first empress.
    @param col1: The column index of the first empress.
    @param row2: The row index of the second empress.
    @param col2: The column index of the second empress.

    @return: True if the two empresses conflict, False otherwise.
    """
    def conflict(self, row1, col1, row2, col2):
        if row1 == row2: return True # same row
        if col1 == col2: return True # same column
        diff_row = abs(row1 - row2)
        diff_col = abs(col1 - col2)
        if diff_row == diff_col: return True # same diagonal
        if diff_row == 1 and diff_col == 4: return True # special 'knight moves' 1x4
        if diff_row == 4 and diff_col == 1: return True # special 'knight moves' 4x1
        if diff_row == 2 and diff_col == 3: return True # special 'knight moves' 2x3
        if diff_row == 3 and diff_col == 2: return True # special 'knight moves' 3x2
        return False

    """
    Heuristic function for the NAmazonsProblem.
    The heuristic is the sum of conflicts between each empresses on the board and each empty tiles.
    More conflicts means that the board is less close to a solution because we won't be able to place a lot of future actions.
    
    @param node: The node to evaluate.
    @return: The heuristic value of the node.
    """
    def h(self, node):
        num_conflicts = 0
        # Count the number of conflicts between the empresses on the board (take into account the empty columns)
        for (row1, col1) in enumerate(node.state.rows):
            # Avoid counting conflicts twice with the "start" argument
            for (row2, col2) in enumerate(node.state.rows, start=node.state.colEmpty):
                num_conflicts += self.conflict(row1, col1, row2, col2)
        return num_conflicts

"""
State representation for the NAmazonsProblem.

The state is represented as an N-element array, where a value of r in the c-th entry means there is an empress at column c, row r,
and a value of -1 means that the c-th column has not been filled in yet. We fill in columns left to right.
"""
class State:

    """
    Attributes:
        - rows: an N-element array
        - N: the size of the board
        - colEmpty: the index of the first empty column
    """
    def __init__(self, rows, colEmpty=0):
        self.rows = rows
        self.colEmpty = colEmpty
    
    """Equality methods for comparison and hashing"""
    def __eq__(self, other):
        return isinstance(other, State) and self.rows == other.rows

    """Less than method for priority queue"""
    def __lt__(self, other):
        return self.colEmpty < other.colEmpty
    
    """Hash method for hashing in the priority queue"""
    def __hash__(self):
        return hash(tuple(self.rows))
    
    """String representation of the state for formatting the output"""
    def __str__(self):
        str_repr = ""
        size = len(self.rows)
        rows_str = ['#' * size] * size
        for i in range(size):
            row = self.rows[i]
            if row == -1: break # Already created the empty columns in the 'rows_str'
            rows_str[row] = '#' * i + 'A' + '#' * (size - i - 1) # Replace the '#' by 'A' in the row
        # Create the complete string representation
        for row in rows_str: str_repr += row + '\n'
        return str_repr[:-1]


"""
Analyse the time and the number of moves to solve the NAmazonsProblem for a value of N with a given search function.
The results are printed in the console.

@param N: The size of the board (must be > 0).
@param search_function: The search function to use to solve the problem. Default is depth_first_graph_search.
"""
def analyseSolver(N, search_function=depth_first_graph_search):
    # Create the NAzamonsProblem
    initial_state = State([-1 for _ in range(N)])
    problem = NAmazonsProblem(N, initial_state)

    # Solve the problem
    start_timer = time.perf_counter()
    ITERATIONS = 10
    for _ in range(ITERATIONS):
        node = search_function(problem)
    end_timer = time.perf_counter()

    # Print the time and the number of moves
    print("N: ", N)
    print("Time: ", (end_timer - start_timer) / ITERATIONS)
    print('Number of moves: ', str(node.depth))

"""
Analyse the time and the number of moves to solve the NAmazonsProblem for different values of N.
This analysis is done for the depth_first_graph_search, astar_search and breadth_first_graph_search functions.

The results are printed in the console.
"""
def perfs_analyser():
    N = [10, 11, 12, 13, 20, 25, 30]
    for n in N: analyseSolver(n, astar_search)
    for n in N: analyseSolver(n, depth_first_graph_search)
    for n in N: analyseSolver(n, breadth_first_graph_search)


# Main function
if __name__ == "__main__":

    # perfs_analyser()

    N = int(sys.argv[1]) # Get the size of the board from the command line

    # Create the NAmazonsProblem
    initial_state = State([-1 for _ in range(N)])
    problem = NAmazonsProblem(N, initial_state)

    # Solve the problem
    start_timer = time.perf_counter()
    node = breadth_first_graph_search(problem)
    end_timer = time.perf_counter()

    # Print the solution
    path = node.path()
    print('Number of moves: ', str(node.depth))
    for n in path:
        print(n.state)
        print()

    print("Time: ", end_timer - start_timer) # To remove for the submission