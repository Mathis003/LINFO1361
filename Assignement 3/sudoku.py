import random
import time
import math
import sys
import collections

"""
Get the objective score of the Sudoku board.

The objective score is the sum of the number of conflicts in each row, column, and subgrid,
plus the number of empty tiles in the board.

A conflict is the number of times a number appears more than once in a row, column, or subgrid.

@param board: The Sudoku board
@return: The objective score of the board
"""
def objective_score(board):

    """Get the number of empty tiles on the board."""
    def getTilesEmpty():
        return sum(row.count(0) for row in board)

    """Get the number of conflicts in a row of the board."""
    def getConflictsRow(row):
        return sum(count - 1 for count in collections.Counter(board[row]).values() if count > 1)

    """Get the number of conflicts in a column of the board."""
    def getConflictsColumn(col):
        return sum(count - 1 for count in collections.Counter([board[i][col] for i in range(9)]).values() if count > 1)

    """Get the number of conflicts in a subgrid of the board."""
    def getConflictsSubgrid(idx):
        subgridElements = [board[3 * (idx // 3) + k][3 * (idx % 3) + l] for k in range(3) for l in range(3)]
        return sum(count - 1 for count in collections.Counter(subgridElements).values() if count > 1)

    empty_tiles = getTilesEmpty()
    conflicts = sum(getConflictsRow(i) + getConflictsColumn(i) + getConflictsSubgrid(i) for i in range(9))
    return conflicts + empty_tiles

"""
Get the available values that can be placed in a tile of the Sudoku board without create conflicts.

@param board: The Sudoku board
@param i: The row index of the tile
@param j: The column index of the tile

@return: The list of available values that can be placed in the tile
"""
def getAvailableValues(board, i, j):
    row = board[i]
    col = [board[k][j] for k in range(9)]
    subgrid = [board[3 * (i // 3) + k][3 * (j // 3) + l] for k in range(3) for l in range(3)]
    # Substract the values already present in the row, column, and subgrid from the set of all possible values
    available_values = set(range(1, 10)) - set(row + col + subgrid)
    return available_values

"""
Generate a neighboring solution by randomly selecting a tile and changing its value.
The new value is chosen randomly from the set of values that can be legally placed in that tile based on Sudoku rules.
If no such value is available within a specified maximum number of iterations (MAX_ITER),
a random value between 1 and 9 is selected, potentially introducing conflicts.

@param current_solution: The current Sudoku board
@param fixed_positions: The set of fixed positions in the board

@return: The neighbor of the current solution
"""
def generate_neighbor(current_solution, fixed_positions, MAX_ITER=5):
    # Randomly select a tile and get the available values that can be placed in that tile
    values = set()
    i, j = random.randint(0, 8), random.randint(0, 8)
    nbIteration = 0
    while len(values) == 0 and nbIteration < MAX_ITER: # Avoid getting an empty list of available values
        nbIteration += 1
        while (i, j) in fixed_positions: # Avoid changing the value of a fixed tile
            i, j = random.randint(0, 8), random.randint(0, 8)
        values = getAvailableValues(current_solution, i, j)
    if nbIteration == MAX_ITER: values = set(range(1, 10)) # If no available values, select a random value (after MAX_ITER iterations)

    neighbor = [row[:] for row in current_solution]
    best_score = objective_score(neighbor)
    best_neightboor = neighbor
    for value in list(values):
        oldValue = neighbor[i][j]
        neighbor[i][j] = value
        score = objective_score(neighbor)
        if score < best_score:
            best_score = score
            best_neightboor = [row[:] for row in neighbor]
        neighbor[i][j] = oldValue
    
    return best_neightboor

    # # Randomly select a new value for the tile from the available values
    # new_value = random.choice(list(values))

    # # Copy the current solution and update the value of the selected tile to create the neighbor
    # neighbor = [row[:] for row in current_solution]
    # neighbor[i][j] = new_value
    # return neighbor


"""
Get the set of fixed positions in the Sudoku board.

@param initial_board: The initial Sudoku board

@return: The set of fixed positions in the board
"""
def get_fixed_positions(initial_board):
    fixed_positions = set()
    for i in range(9):
        for j in range(9):
            if initial_board[i][j] != 0: fixed_positions.add((i, j))
    return fixed_positions


"""
Fill the empty tiles of the Sudoku board with random values.

@param board: The Sudoku board
@param fixed_positions: The set of fixed positions in the board

@return: The Sudoku board with the empty tiles filled with random values
"""
def fill_board(board, fixed_positions):
    for i in range(9):
        for j in range(9):
            if (i, j) not in fixed_positions and board[i][j] == 0:
                board[i][j] = random.randint(1, 9)
    return board

"""
Simulated annealing Sudoku solver.
"""
def simulated_annealing_solver(initial_board):
    fixed_positions = get_fixed_positions(initial_board)
    
    current_solution = fill_board(initial_board, fixed_positions)
    best_solution = current_solution

    current_score = objective_score(current_solution)
    best_score = current_score

    temperature = 1.0
    cooling_rate = 0.99999 # To have a very slow cooling rate (maximum iterations)

    while temperature > 0.0001:
        try:
            # Generate a neighbor solution
            neighbor = generate_neighbor(current_solution, fixed_positions)

            # Evaluate the neighbor
            neighbor_score = objective_score(neighbor)

            # Calculate acceptance probability
            delta = float(current_score - neighbor_score)

            # If the current score is 0, return the current solution and his score
            if current_score == 0: return current_solution, current_score
            
            # Accept the neighbor with a probability based on the acceptance probability
            if neighbor_score < current_score or (neighbor_score > 0 and math.exp(delta / temperature) > random.random()):
                current_solution = neighbor
                current_score    = neighbor_score
                if (current_score < best_score):
                    best_solution = current_solution
                    best_score    = current_score

            # Cool down the temperature
            temperature *= cooling_rate

        except:
            # print("Break asked");
            break
        
    return best_solution, best_score

"""
Print the Sudoku board.

@param board: The Sudoku board
@return: None
"""
def print_board(board):
    for row in board: print("".join(map(str, row)))
 
"""
Read Sudoku puzzle from a text file.

@param file_path: The path to the text file containing the Sudoku puzzle
@return: The Sudoku board
"""
def read_sudoku_from_file(file_path):
    with open(file_path, 'r') as file:
        sudoku = [[int(num) for num in line.strip()] for line in file]
    return sudoku

# Main function
if __name__ == "__main__":

    # Read the Sudoku puzzle from the text file
    initial_board = read_sudoku_from_file(sys.argv[1])

    # Solve the Sudoku puzzle using simulated annealing
    start_timer = time.perf_counter()
    solved_board, current_score = simulated_annealing_solver(initial_board)
    end_timer = time.perf_counter()

    # Print the solved Sudoku board and the objective score
    print_board(solved_board)
    print("\nValue(C):", current_score)

    # Do not display the time taken in the final submission on Inginious
    # print("\nTime taken:", end_timer - start_timer, "seconds")