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
                if diff_row == 0 or diff_row == diff_col or diff_row == diff_col: valid_action = False; break # Same row / column or diagonal
                if diff_col == 1 and diff_row == 4: valid_action = False; break # Special 'knight moves' 1x4
                if diff_col == 4 and diff_row == 1: valid_action = False; break # Special 'knight moves' 4x1
                if diff_col == 2 and diff_row == 3: valid_action = False; break # Special 'knight moves' 2x3
                if diff_col == 3 and diff_row == 2: valid_action = False; break # Special 'knight moves' 3x2
            
            # Add the action if it is valid
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
        rows = state.rows.copy()
        rows[state.colEmpty] = row
        state = State(rows)
        return state

    """
    Check if a state is a goal state.
    A state is a goal state if the last column are filled with an empress (and thus all the columns through the modeling of the problem).

    @param state: The state to check.

    @return: True if the state is a goal state, False otherwise.
    """
    def goal_test(self, state):
        return True if state.colEmpty == state.N else False

    """
    Heuristic function for the NAmazonsProblem.
    The heuristic is the number of attacks between the empresses on the board.
    
    @param node: The node to evaluate.
    @return: The heuristic value of the node.
    """
    def h(self, node):
        conflicts = 0
        rows = node.state.rows
        # Iterate over the filled column
        for i in range(node.state.colEmpty):
            # Iterate to the right of the i_th column (stop to the first empty column)
            for j in range(i + 1, node.state.colEmpty):
                diff_col = j - i
                diff_row = abs(rows[i] - rows[j])
                if diff_row == 0:        conflicts += 1 # Same row
                if diff_row == diff_col: conflicts += 1 # Same diagonal
                if diff_col == 1 and diff_row == 4: conflicts += 1 # Special 'knight moves' 1x4
                if diff_col == 4 and diff_row == 1: conflicts += 1 # Special 'knight moves' 4x1
                if diff_col == 3 and diff_row == 2: conflicts += 1 # Special 'knight moves' 3x2
                if diff_col == 2 and diff_row == 3: conflicts += 1 # Special 'knight moves' 2x3
        return conflicts
    

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
    def __init__(self, rows):
        self.rows = rows
        self.N = len(rows)
        self.colEmpty = self.N if (self.rows[self.N - 1] != -1) else self.rows.index(-1)
    
    """Equality methods for comparison and hashing"""
    def __eq__(self, other):
        return isinstance(other, State) and (self.rows == other.rows)

    """Less than method for priority queue"""
    def __lt__(self, other):
        return self.colEmpty < other.colEmpty
    
    """Hash method for hashing in the priority queue"""
    def __hash__(self):
        return hash(tuple(self.rows))
    
    """String representation of the state for formatting the output"""
    def __str__(self):
        str_repr = ""
        rows_str = ['#' * self.N] * self.N
        for i in range(self.N):
            row = self.rows[i]
            if row == -1: break # Already created the empty columns in the 'rows_str'
            rows_str[row] = '#' * i + 'A' + '#' * (self.N - i - 1) # Replace the '#' by 'A' in the row
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
    node = search_function(problem)
    end_timer = time.perf_counter()

    # Print the time and the number of moves
    print("Time: ", end_timer - start_timer)
    print('Number of moves: ', str(node.depth))

    # For debugging purposes
    # path = node.path()
    # for n in path:
    #     print(n.state)
    #     print()

"""
Analyse the time and the number of moves to solve the NAmazonsProblem for different values of N.
This analysis is done for the depth_first_graph_search, astar_search and breadth_first_graph_search functions.

The results are printed in the console.
"""
def perfs_analyser():
    N = [10, 11, 12, 13, 20, 25, 30]
    for n in N: analyseSolver(n, depth_first_graph_search)
    # for n in N: analyseSolver(n, astar_search)
    # for n in N: analyseSolver(n, breadth_first_graph_search)


# Main function
if __name__ == "__main__":

    # perfs_analyser()

    N = int(sys.argv[1]) # Get the size of the board from the command line

    # Create the NAmazonsProblem
    initial_state = State([-1 for _ in range(N)])
    problem = NAmazonsProblem(N, initial_state)

    # Solve the problem
    start_timer = time.perf_counter()
    node = astar_search(problem)
    end_timer = time.perf_counter()

    # Print the solution
    path = node.path()
    print('Number of moves: ', str(node.depth))
    for n in path:
        print(n.state)
        print()

    print("Time: ", end_timer - start_timer) # To remove for the submission