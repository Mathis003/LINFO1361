import random
import time
import math
import sys

def objective_score(board):
    conflicts = 0
    # Check row and column conflicts
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                continue # Skip empty cells
            for k in range(9):
                # Conflict same row
                if k != j and board[i][k] == board[i][j]:
                    conflicts += 1
                # Conflict same column
                if k != i and board[k][j] == board[i][j]:
                    conflicts += 1

    # Check subgrid conflicts
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid = []
            for k in range(3):
                for l in range(3):
                    subgrid.append(board[i + k][j + l])
            for num in range(1, 10):
                if subgrid.count(num) > 1:
                    conflicts += subgrid.count(num) - 1

    return conflicts

def getNbSubgrid(board, i, j):
    subGridIdx = i // 3
    subGridIdy = j // 3
    subGrid = []
    for k in range(3):
        for l in range(3):
            subGrid.append(board[subGridIdx * 3 + k][subGridIdy * 3 + l])
    return subGrid

def opposite_numbers(number_list):
    full_set = set(range(1, 10))
    number_set = set(number_list)
    opposite_set = full_set - number_set
    return list(opposite_set)

def generate_neighbor(current_solution, fixed_positions):
    i, j = random.randint(0, 8), random.randint(0, 8)
    while (i, j) in fixed_positions:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
    
    listNb = current_solution[i] + current_solution[j] + getNbSubgrid(current_solution, i, j)
    opposite_listNb = opposite_numbers(listNb)
    if opposite_listNb == []: return current_solution
    randomNb = random.choice(opposite_listNb)
    current_solution[i][j] = randomNb
    return current_solution

def get_fixed_positions(initial_board):
    fixed_positions = set()
    for i in range(len(initial_board)):
        for j in range(len(initial_board[i])):
            if initial_board[i][j] != 0: fixed_positions.add((i, j))
    return fixed_positions

def randomly_fill_board(board):
    for i in range(len(initial_board)):
        for j in range(len(initial_board[i])):
            if board[i][j] == 0: board[i][j] = random.randint(1, 9)
    return board

"""
Simulated annealing Sudoku solver.
"""
def simulated_annealing_solver(initial_board):
    fixed_positions = get_fixed_positions(initial_board)
    current_solution = [row[:] for row in initial_board]
    current_solution = randomly_fill_board(current_solution)
    current_score = objective_score(current_solution)

    best_solution, best_score = current_solution, current_score

    temperature = 1.0
    threshold_T = 0.0001
    cooling_rate = 0.99999 # TODO: Adjust this parameter to control the cooling rate

    # while temperature > threshold_T:
    #     try:  
    #         # TODO: Generate a neighbor (Don't forget to skip non-zeros tiles in the initial board ! It will be verified on Inginious.)
    #         neighbor = generate_neighbor(current_solution, fixed_positions)

    #         # Evaluate the neighbor
    #         neighbor_score = objective_score(neighbor)

    #         if current_score == 0: return current_solution, current_score

    #         # Calculate acceptance probability
    #         delta = float(current_score - neighbor_score)
            
    #         # Accept the neighbor with a probability based on the acceptance probability
    #         if neighbor_score < current_score or (neighbor_score > 0 and math.exp(delta / temperature) > random.random()):
    #             current_solution = neighbor
    #             current_score    = neighbor_score
    #             if (current_score < best_score):
    #                 best_solution = current_solution
    #                 best_score    = current_score

    #         # Cool down the temperature
    #         temperature *= cooling_rate

    #     except:
    #         print("Break asked"); break
        
    # return best_solution, best_score

    while temperature > threshold_T:
        # TODO: Generate a neighbor (Don't forget to skip non-zeros tiles in the initial board ! It will be verified on Inginious.)
        neighbor = generate_neighbor(current_solution, fixed_positions)

        # Evaluate the neighbor
        neighbor_score = objective_score(neighbor)

        if current_score == 0: return current_solution, current_score

        # Calculate acceptance probability
        delta = float(current_score - neighbor_score)
        
        # Accept the neighbor with a probability based on the acceptance probability
        if neighbor_score < current_score or (neighbor_score > 0 and math.exp(delta / temperature) > random.random()):
            current_solution = neighbor
            current_score    = neighbor_score
            if (current_score < best_score):
                best_solution = current_solution
                best_score    = current_score

        # Cool down the temperature
        temperature *= cooling_rate

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
    print("\nTime taken:", end_timer - start_timer, "seconds")