from itertools import product

def evaluate_expression_1(A, B, C, D):
    return not (A and B) or (not B and C)

def evaluate_expression_2(A, B, C, D):
    return not (not A or B) or C

def evaluate_expression_3(A, B, C, D):
    return (A or not B) and (B or not C) and not (not D or not A)

def count_true_interpretations():
    count = 0
    for values in product([True, False], repeat=4):
        A, B, C, D = values
        if evaluate_expression_2(A, B, C, D):
            print(f"A={A}, B={B}, C={C}, D={D}")
            count += 1
    return count

num_true_interpretations = count_true_interpretations()
print("Nombre d'interprétations vraies :", num_true_interpretations)