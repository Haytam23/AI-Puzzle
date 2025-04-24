import csv
import math
from collections import defaultdict

# Function to calculate f(b*) for Newton's method
def f(b, N, d):
    return sum([b**i for i in range(d + 1)]) - N

# Function to calculate the derivative of f(b*) with respect to b
def f_prime(b, d):
    return sum([i * b**(i-1) for i in range(1, d + 1)])

# Newton's method to calculate the effective branching factor (b*)
def calculate_b_star(N, d, initial_guess=1.5, tolerance=1e-7, max_iterations=100):
    b = initial_guess
    for _ in range(max_iterations):
        f_b = f(b, N, d)
        f_prime_b = f_prime(b, d)
        if abs(f_b) < tolerance:
            return b  # Convergence reached
        b = b - f_b / f_prime_b
    return None  # Did not converge

# Function to process the results and compute the effective branching factor b*
def calculate_branching_factors(input_file, output_file):
    branching_factors = defaultdict(lambda: {'sum_b_star': 0.0, 'count': 0})

    with open(input_file, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            heuristic = row['Heuristic']
            solved = row['Solved']

            if solved == 'True':
                N = int(row['Expanded Nodes'])
                d = int(row['Depth'])

                if d > 0:  # Only calculate if depth is greater than 0
                    b_star = calculate_b_star(N, d)
                    if b_star is not None:
                        branching_factors[heuristic]['sum_b_star'] += b_star
                        branching_factors[heuristic]['count'] += 1

    # Write average b* values to the output file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Heuristic', 'Average Effective Branching Factor (b*)'])

        for heuristic, data in branching_factors.items():
            if data['count'] > 0:
                average_b_star = data['sum_b_star'] / data['count']
                writer.writerow([heuristic, f"{average_b_star:.4f}"])

    print(f"Average branching factors have been written to {output_file}.")

if __name__ == '__main__':
    input_file = 'heuristic_comparison_results.csv'
    output_file = 'average_branching_factor_results.csv'

    # Calculate branching factors and write the average to the output file
    calculate_branching_factors(input_file, output_file)
