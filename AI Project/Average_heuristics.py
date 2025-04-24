'''=====Start Change Task 3====='''

import csv
from collections import defaultdict

# Function to aggregate results and compute averages
def calculate_averages(input_file, output_file):
    results = defaultdict(lambda: {'solved': 0, 'depth': 0, 'expanded_nodes': 0, 
                                   'max_fringe_size': 0, 'execution_time': 0.0, 'count': 0})
    
    with open(input_file, mode='r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            heuristic = row['Heuristic']
            solved = row['Solved']
            if solved == 'True':
                # Increment the counters only if the puzzle was solved
                results[heuristic]['solved'] += 1
                results[heuristic]['depth'] += int(row['Depth'])
                results[heuristic]['expanded_nodes'] += int(row['Expanded Nodes'])
                results[heuristic]['max_fringe_size'] += int(row['Max Fringe Size'])
                results[heuristic]['execution_time'] += float(row['Execution Time'])
                results[heuristic]['count'] += 1
    
    # Write averages to a new CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        writer.writerow(['Heuristic', 'Solved Puzzles', 'Average Depth', 'Average Expanded Nodes', 
                         'Average Max Fringe Size', 'Average Execution Time (seconds)'])
        
        # Write data for each heuristic
        for heuristic, data in results.items():
            if data['count'] > 0:
                avg_depth = data['depth'] / data['count']
                avg_expanded_nodes = data['expanded_nodes'] / data['count']
                avg_fringe_size = data['max_fringe_size'] / data['count']
                avg_exec_time = data['execution_time'] / data['count']
                writer.writerow([heuristic, data['solved'], f"{avg_depth:.2f}", 
                                 f"{avg_expanded_nodes:.2f}", f"{avg_fringe_size:.2f}", 
                                 f"{avg_exec_time:.4f}"])

    print(f"Averages have been written to {output_file}.")

if __name__ == '__main__':
    # Path to the results CSV file generated earlier
    input_file = 'heuristic_comparison_results.csv'
    
    # Path to the output CSV file to write averages
    output_file = 'heuristic_averages.csv'
    
    # Calculate and write averages to the output file
    calculate_averages(input_file, output_file)

'''=====Start Change Task 3====='''
