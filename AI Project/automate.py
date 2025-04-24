'''=====Start Change Task 3====='''

import csv
import time
from search import breadthFirstSearch, depthFirstSearch, uniformCostSearch, aStarSearch, h2_manhattan_distance
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

def run_strategy(strategy_func, problem):
    """Run a search strategy and collect statistics."""
    start_time = time.time()
    try:
        path, expanded_nodes, max_fringe_size, depth = strategy_func(problem)
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
        print(f"Error with strategy: {e}")
        return {
            'solved': False,
            'depth': 'N/A',
            'expanded_nodes': 'N/A',
            'max_fringe_size': 'N/A',
            'execution_time': 'N/A'
        }

def write_results(output_file, scenario_id, initial_state, strategy_results):
    """Write the results for each strategy to the output CSV file."""
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        for strategy_name, result in strategy_results.items():
            writer.writerow([scenario_id, initial_state, strategy_name] + list(result.values()))

if __name__ == '__main__':
    # Load scenarios from CSV
    scenarios = load_scenarios('scenarios.csv')

    # Define strategies to compare
    strategies = {
        'BFS': breadthFirstSearch,
        'DFS': depthFirstSearch,
        'UCS': uniformCostSearch,
        'A* (Manhattan Distance)': lambda problem: aStarSearch(problem, h2_manhattan_distance)
    }

    # Prepare output CSV file
    output_file = 'strategy_comparison_results.csv'
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Puzzle ID', 'Initial State', 'Strategy', 'Solved', 'Depth', 'Expanded Nodes', 'Max Fringe Size', 'Execution Time'])

    # Process each puzzle scenario
    for scenario_id, initial_state in scenarios:
        print(f"Processing Puzzle {scenario_id}, Initial State: {initial_state}")

        # Check if the puzzle is solvable
        if not is_solvable(initial_state):
            print(f"Puzzle {scenario_id} is unsolvable. Skipping.")
            for strategy_name in strategies.keys():
                write_results(output_file, scenario_id, initial_state, {
                    strategy_name: {
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

        # Run all strategies
        strategy_results = {}
        for strategy_name, strategy_func in strategies.items():
            print(f"Running {strategy_name} for Puzzle {scenario_id}")
            result = run_strategy(strategy_func, problem)
            strategy_results[strategy_name] = result

        # Write results to CSV
        write_results(output_file, scenario_id, initial_state, strategy_results)

        print(f"Completed puzzle {scenario_id}")

'''=====End Change Task 3====='''


