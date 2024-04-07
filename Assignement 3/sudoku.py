import random
import time
import math
import sys

def objective_score(board):

    def getTilesEmpty(board):
        empty_tiles = 0
        for row in board: empty_tiles += row.count(0)
        return empty_tiles

    def getConflictsRow(board, row):
        conflicts = 0
        rowElements = board[row]
        for i in range(1, 10):
            nbElement = rowElements.count(i)
            if nbElement > 1: conflicts += nbElement
        return conflicts

    def getConflictsColumn(board, col):
        conflicts = 0
        columnElements = [board[i][col] for i in range(9)]
        for i in range(1, 10):
            nbElement = columnElements.count(i)
            if nbElement > 1: conflicts += nbElement
        return conflicts

    def getConflictsSubgrid(board, idx):
        subgridElements = []
        pos_i, pos_j = 3 * (idx // 3), 3 * (idx % 3)
        for k in range(3):
            for l in range(3):
                subgridElements.append(board[pos_i + k][pos_j + l])
        conflicts = 0
        for i in range(1, 10):
            nbElement = subgridElements.count(i)
            if nbElement > 1: conflicts += nbElement
        return conflicts

    conflicts = 0
    empty_tiles = getTilesEmpty(board)
    for i in range(9):
        conflicts += getConflictsRow(board, i)
        conflicts += getConflictsColumn(board, i)
        conflicts += getConflictsSubgrid(board, i)
    return conflicts + empty_tiles

def getAvailableValues(board, i, j):
    row = board[i]
    col = [board[k][j] for k in range(9)]
    subgrid = []
    pos_i, pos_j = 3 * (i // 3), 3 * (j // 3)
    for k in range(3):
        for l in range(3):
            subgrid.append(board[pos_i + k][pos_j + l])
    available_values = set(range(1, 10)) - set(row + col + subgrid)
    return list(available_values)

def generate_neighbor(current_solution, fixed_positions):
    listValues = []
    i, j = random.randint(0, 8), random.randint(0, 8)
    MAX_ITER = 5
    incr = 0
    while len(listValues) == 0:
        incr += 1
        while (i, j) in fixed_positions:
            i, j = random.randint(0, 8), random.randint(0, 8)
        listValues = getAvailableValues(current_solution, i, j)
        if incr == MAX_ITER: listValues = list(range(1, 10))

    new_value = random.choice(listValues)
    neighbor = [row[:] for row in current_solution]
    neighbor[i][j] = new_value
    return neighbor

def get_fixed_positions(initial_board):
    fixed_positions = set()
    for i in range(9):
        for j in range(9):
            if initial_board[i][j] != 0: fixed_positions.add((i, j))
    return fixed_positions

"""
Simulated annealing Sudoku solver.
"""
def simulated_annealing_solver(initial_board):
    fixed_positions = get_fixed_positions(initial_board)

    current_solution = [row[:] for row in initial_board]
    best_solution = current_solution

    current_score = objective_score(current_solution)
    best_score = current_score

    temperature = 1.0
    threshold_T = 0.0001
    cooling_rate = 0.9999999999 # To be adjusted

    while temperature > threshold_T:
        try:
            neighbor = generate_neighbor(current_solution, fixed_positions)

            # Evaluate the neighbor
            neighbor_score = objective_score(neighbor)

            # Calculate acceptance probability
            delta = float(current_score - neighbor_score)

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
            print("Break asked"); break
        
    return best_solution, best_score

"""
Print the Sudoku board.
"""
def print_board(board):
    for row in board: print("".join(map(str, row)))
 
"""
Read Sudoku puzzle from a text file.
"""
def read_sudoku_from_file(file_path):
    with open(file_path, 'r') as file:
        sudoku = [[int(num) for num in line.strip()] for line in file]
    return sudoku


if __name__ == "__main__":

    initial_board = read_sudoku_from_file(sys.argv[1])
    start_timer = time.perf_counter()
    solved_board, current_score = simulated_annealing_solver(initial_board)
    end_timer = time.perf_counter()
    print_board(solved_board)
    print("\nValue(C):", current_score)

    # Do not display the time taken in the final submission on Inginious
    # print("\nTime taken:", end_timer - start_timer, "seconds")