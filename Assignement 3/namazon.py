from search import *
import time

#################
# Problem class #
#################

"""
The problem of placing N amazons on an NxN board with none attacking
each other. A state is represented as an N-element array, where
a value of r in the c-th entry means there is an empress at column c,
row r, and a value of -1 means that the c-th column has not been
filled in yet. We fill in columns left to right.
"""
class NAmazonsProblem(Problem):
    
    def __init__(self, N, initial_state):
        Problem.__init__(self, initial_state)
        self.N = N

    def actions(self, state):
        actions = [i for i in range(self.N) if i not in state.rows]
        filtered_actions = []
        for action in actions:
            valid_action = True
            for i in range(state.colEmpty):
                currRow = state.rows[i]
                # Check the same row
                if currRow == action: valid_action = False; break
                diff_col = state.colEmpty - i
                diff_row = abs(currRow - action)
                # Check the same diagonal
                if diff_row == diff_col: valid_action = False; break
                # Check the special 'knight moves'
                if diff_col == 1 and diff_row == 4: valid_action = False; break
                if diff_col == 4 and diff_row == 1: valid_action = False; break
                if diff_col == 2 and diff_row == 3: valid_action = False; break
                if diff_col == 3 and diff_row == 2: valid_action = False; break

            if valid_action:
                filtered_actions.append(action)

        return filtered_actions
    
    def result(self, state, row):
        rows = state.rows.copy()
        rows[state.colEmpty] = row
        state = State(rows)
        return state

    def goal_test(self, state):
        return True if state.colEmpty == state.N else False

    def h(self, node):
        nbAttacks = 0
        rows = node.state.rows
        for i in range(node.state.colEmpty):
            currRow = rows[i]
            for j in range(node.state.colEmpty):
                if i == j: continue # No need to check the same column (by construction of the problem)
                otherRow = rows[j]
                if currRow == otherRow: nbAttacks += 1 # Same row
                if abs(currRow - otherRow) == abs(i - j): nbAttacks += 1 # Same diagonal
                # Special 'knight moves'
                if abs(i - j) == 1 and abs(currRow - otherRow) == 4: nbAttacks += 1
                if abs(i - j) == 4 and abs(currRow - otherRow) == 1: nbAttacks += 1
                if abs(i - j) == 3 and abs(currRow - otherRow) == 2: nbAttacks += 1
                if abs(i - j) == 2 and abs(currRow - otherRow) == 3: nbAttacks += 1
        return nbAttacks
    
###############
# State class #
###############

class State:

    def __init__(self, rows):
        self.rows = rows
        self.N = len(rows)
        self.colEmpty = self.N if (self.rows[self.N - 1] != -1) else self.rows.index(-1)
    
    def __eq__(self, other):
        return isinstance(other, State) and (self.rows == other.rows)

    def __lt__(self, other):
        return self.colEmpty < other.colEmpty
    
    def __hash__(self):
        return hash(tuple(self.rows))
    
    def __str__(self):
        str_repr = ""
        listRows = ['#' * self.N] * self.N
        for i in range(self.N):
            row = self.rows[i]
            if row == -1:
                break
            listRows[row] = '#' * i + 'A' + '#' * (self.N - i - 1)
        for row in listRows:
            str_repr += row + '\n'
        return str_repr[:-1]
        

#####################
# Launch the search #
#####################

def analyseTime(search_function):
    N = [10, 11, 12, 13, 20, 25, 30]
    for n in N:
        initial_state = State([-1 for _ in range(n)])
        problem = NAmazonsProblem(n, initial_state)
        start_timer = time.perf_counter()
        node = search_function(problem)
        end_timer = time.perf_counter()
        print("Time: ", end_timer - start_timer)
        path = node.path()
        print('Number of moves: ', str(node.depth))
        # for n in path:
        #     print(n.state)
        #     print()

# analyseTime(breadth_first_graph_search)
# analyseTime(depth_first_graph_search)
# analyseTime(astar_search)

N = int(sys.argv[1])
initial_state = State([-1 for _ in range(N)])
problem = NAmazonsProblem(N, initial_state)

start_timer = time.perf_counter()

node = depth_first_graph_search(problem)

end_timer = time.perf_counter()

path = node.path()
# print('Number of moves: ', str(node.depth))
# for n in path:
#     print(n.state) # assuming that the _str_ function of state outputs the correct format
#     print()
print("Time: ", end_timer - start_timer)

# path = node.path()
# print("initial state")
# print(path[0].state)
# print()
# for i in range(1, len(path) - 1):
#     n = path[i]
#     print("state {}".format(i))
#     print(n.state)
#     print()
# n = path[len(path) - 1]
# print("goal state")
# print(n.state)