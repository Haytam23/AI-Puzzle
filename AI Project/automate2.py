'''=====Start Change Task 4====='''

import csv
import time
from search import aStarSearch, h1_misplaced_tiles, h2_manhattan_distance, h3_euclidean_distance, h4_out_of_row_and_column
from eightpuzzle import FifteenPuzzleSearchProblem, FifteenPuzzleState

# Function to check if the puzzle is solvable
def is_solvable(puzzle):
    """Determine if a given 15-puzzle is solvable."""
    flattened_puzzle = [tile for tile in puzzle if tile != 0]  # Remove the blank (0)
    inversions = 0
    for i in range(len(flattened_puzzle)):
        for j in range(i + 1, len(flattened_puzzle)):
            if flattened_puzzle[i] > flattened_puzzle[j]:
                inversions += 1
    # The puzzle is solvable if the number of inversions is even
    return inversions % 2 == 0

def load_scenarios(file_path):
    """Load puzzle scenarios from a CSV file."""
    scenarios = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            if len(row) < 17:
                continue
            puzzle_id = int(row[0])
            initial_state = list(map(int, row[1:17]))  # Ensure exactly 16 elements are read
            scenarios.append((puzzle_id, initial_state))
    return scenarios

def run_heuristic(heuristic_func, problem):
    """Run A* search with a heuristic and collect statistics."""
    start_time = time.time()
    try:
        path, expanded_nodes, max_fringe_size, depth = aStarSearch(problem, heuristic=heuristic_func)
        solved = True if path else False
        exec_time = time.time() - start_time
        return {
            'solved': solved,
            'depth': depth,
            'expanded_nodes': expanded_nodes,
            'max_fringe_size': max_fringe_size,
            'execution_time': exec_time
        }
    except Exception as e:
        print(f"Error with heuristic: {e}")
        return {
            'solved': False,
            'depth': 'N/A',
            'expanded_nodes': 'N/A',
            'max_fringe_size': 'N/A',
            'execution_time': 'N/A'
        }

def write_results(output_file, puzzle_id, initial_state, heuristic_results):
    """Write the results for each heuristic to the output CSV file."""
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        for heuristic_name, result in heuristic_results.items():
            writer.writerow([puzzle_id, initial_state, heuristic_name] + list(result.values()))

if __name__ == '__main__':
    # Load scenarios from CSV
    scenarios = load_scenarios('scenarios.csv')

    # Define heuristics to compare
    heuristics = {
        'Misplaced Tiles (h1)': h1_misplaced_tiles,
        'Manhattan Distance (h2)': h2_manhattan_distance,
        'Euclidean Distance (h3)': h3_euclidean_distance,
        'Out of Row and Column (h4)': h4_out_of_row_and_column
    }

    # Prepare output CSV file
    output_file = 'heuristic_comparison_results.csv'
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Puzzle ID', 'Initial State', 'Heuristic', 'Solved', 'Depth', 'Expanded Nodes', 'Max Fringe Size', 'Execution Time'])

    # Process each puzzle scenario
    for puzzle_id, initial_state in scenarios:
        print(f"Processing Puzzle {puzzle_id}, Initial State: {initial_state}")

        # Check if the puzzle is solvable
        if not is_solvable(initial_state):
            print(f"Puzzle {puzzle_id} is unsolvable. Skipping.")
            for heuristic_name in heuristics.keys():
                write_results(output_file, puzzle_id, initial_state, {
                    heuristic_name: {
                        'solved': False,
                        'depth': 'Unsolvable',
                        'expanded_nodes': 'N/A',
                        'max_fringe_size': 'N/A',
                        'execution_time': 'N/A'
                    }
                })
            continue

        # Create puzzle problem instance
        puzzle = FifteenPuzzleState(initial_state)
        problem = FifteenPuzzleSearchProblem(puzzle)

        # Run all heuristics
        heuristic_results = {}
        for heuristic_name, heuristic_func in heuristics.items():
            print(f"Running {heuristic_name} for Puzzle {puzzle_id}")
            result = run_heuristic(heuristic_func, problem)
            heuristic_results[heuristic_name] = result

        # Write results to CSV
        write_results(output_file, puzzle_id, initial_state, heuristic_results)

        print(f"Completed puzzle {puzzle_id}")

'''=====Start Change Task 4====='''
