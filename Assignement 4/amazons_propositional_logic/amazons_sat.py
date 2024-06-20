from clause import *

"""
For the n-amazon problem, the only code you have to do is in this file.

You should code a list of clauses modeling the n-amazons problem for the input file.

You should build clauses using the Clause class defined in clause.py

Here is an example presenting how to create a clause:
Let's assume that the length/width of the chessboard is 4.
To create a clause X_0_1 OR ~X_1_2 OR X_3_3
you can do:

clause = Clause(4)
clause.add_positive(0, 1)
clause.add_negative(1, 2)
clause.add_positive(3, 3)

The clause must be initialized with the length/width of the chessboard.
The reason is that we use a 2D index for our variables but the format
imposed by MiniSAT requires a 1D index.
The Clause class automatically handle this change of index, but needs to know the
number of column and row in the chessboard.

X_0_0 is the literal representing the top left corner of the chessboard
"""

def get_expression(size: int, placed_amazons: list[(int, int)]) -> list[Clause]:
    """
    Defines the clauses for the N-amazons problem
    :param size: length/width of the chessboard
    :param placed_amazons: a list of the already placed amazons
    :return: a list of clauses
    """

    expression = []

    # Constrain 1 : Ensure that the already placed amazons are not on the same square
    for i, j in placed_amazons:
        clause = Clause(size)
        clause.add_positive(i, j)
        expression.append(clause)

    # Constrain 2 : Ensure that there is at most one amazon per row
    for i in range(size):

        # Ensure that there is at least one amazon per row
        clause = Clause(size)
        for j in range(size): clause.add_positive(i, j)
        expression.append(clause)

        # Ensure that there is at most one amazon per row
        for j in range(size):
            for k in range(j + 1, size):
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i, k)
                expression.append(clause)
    
    # Constrain 3 : Ensure that there is at most one amazon per column
    for j in range(size):

        # Ensure that there is at least one amazon per column
        clause = Clause(size)
        for i in range(size):
            clause.add_positive(i, j)
        expression.append(clause)

        # Ensure that there is at most one amazon per column
        for i in range(size):
            for k in range(i + 1, size):
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(k, j)
                expression.append(clause)
    
    # Constrain 4 : Ensure that there is at most one amazon per diagonal (both ways)
    for i in range(size):
        for j in range(size):
            for k in range(1, size):
                if i + k < size and j + k < size:
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(i + k, j + k)
                    expression.append(clause)
                if i + k < size and j - k >= 0:
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(i + k, j - k)
                    expression.append(clause)
                if i - k >= 0 and j + k < size:
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(i - k, j + k)
                    expression.append(clause)
                if i - k >= 0 and j - k >= 0:
                    clause = Clause(size)
                    clause.add_negative(i, j)
                    clause.add_negative(i - k, j - k)
                    expression.append(clause)

    # Constrain 5 : Ensure that there is at most one amazon per 3x2 move
    for i in range(size):
        for j in range(size):
            if i + 3 < size and j + 2 < size:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i + 3, j + 2)
                expression.append(clause)
            if i + 3 < size and j - 2 >= 0:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i + 3, j - 2)
                expression.append(clause)
            if i - 3 >= 0 and j + 2 < size:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i - 3, j + 2)
                expression.append(clause)
            if i - 3 >= 0 and j - 2 >= 0:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i - 3, j - 2)
                expression.append(clause)
            if i + 2 < size and j + 3 < size:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i + 2, j + 3)
                expression.append(clause)
            if i + 2 < size and j - 3 >= 0:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i + 2, j - 3)
                expression.append(clause)
            if i - 2 >= 0 and j + 3 < size:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i - 2, j + 3)
                expression.append(clause)
            if i - 2 >= 0 and j - 3 >= 0:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i - 2, j - 3)
                expression.append(clause)
    
    # Constrain 6 : Ensure that there is at most one amazon per 4x1 move
    for i in range(size):
        for j in range(size):
            if i + 4 < size and j + 1 < size:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i + 4, j + 1)
                expression.append(clause)
            if i + 4 < size and j - 1 >= 0:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i + 4, j - 1)
                expression.append(clause)
            if i - 4 >= 0 and j + 1 < size:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i - 4, j + 1)
                expression.append(clause)
            if i - 4 >= 0 and j - 1 >= 0:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i - 4, j - 1)
                expression.append(clause)
            if i + 1 < size and j + 4 < size:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i + 1, j + 4)
                expression.append(clause)
            if i + 1 < size and j - 4 >= 0:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i + 1, j - 4)
                expression.append(clause)
            if i - 1 >= 0 and j + 4 < size:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i - 1, j + 4)
                expression.append(clause)
            if i - 1 >= 0 and j - 4 >= 0:
                clause = Clause(size)
                clause.add_negative(i, j)
                clause.add_negative(i - 1, j - 4)
                expression.append(clause)
                
    return expression