import csv
import random

# Function to check if the puzzle is solvable
def is_solvable(puzzle):
    """Determine if a given 15-puzzle is solvable."""
    flattened_puzzle = [tile for tile in puzzle if tile != 0]
    inversions = 0
    for i in range(len(flattened_puzzle)):
        for j in range(i + 1, len(flattened_puzzle)):
            if flattened_puzzle[i] > flattened_puzzle[j]:
                inversions += 1
    # The puzzle is solvable if the number of inversions is even
    return inversions % 2 == 0

def generate_easy_puzzle(moves=25):
    """Generate a puzzle by applying a number of random moves to the solved state."""
    solved_puzzle = list(range(1, 16)) + [0]  # Solved puzzle configuration
    puzzle = solved_puzzle[:]
    blank_pos = 15  # Blank (0) starts at the bottom-right corner

    # Possible move directions (up, down, left, right) for the blank space
    moves_dict = {
        'up': -4,    # Move blank up
        'down': 4,   # Move blank down
        'left': -1,  # Move blank left
        'right': 1   # Move blank right
    }

    # Ensure the blank does not move out of bounds
    def is_valid_move(blank, move):
        if move == 'up' and blank >= 4:
            return True
        if move == 'down' and blank < 12:
            return True
        if move == 'left' and blank % 4 != 0:
            return True
        if move == 'right' and blank % 4 != 3:
            return True
        return False

    # Apply a number of random valid moves to the solved puzzle
    for _ in range(moves):
        valid_moves = [m for m in moves_dict if is_valid_move(blank_pos, m)]
        move = random.choice(valid_moves)
        new_blank_pos = blank_pos + moves_dict[move]
        puzzle[blank_pos], puzzle[new_blank_pos] = puzzle[new_blank_pos], puzzle[blank_pos]
        blank_pos = new_blank_pos

    return puzzle

def generate_easy_scenarios(num_scenarios, moves=10, output_file='scenarios2.csv'):
    scenarios = []
    for i in range(1, num_scenarios + 1):
        puzzle = generate_easy_puzzle(moves)
        scenarios.append([i] + puzzle)  # Add puzzle ID as the first column
    
    # Save scenarios to CSV with headers
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Puzzle ID'] + [f'Cell {i}' for i in range(16)])  # Write header
        writer.writerows(scenarios)
    
    print(f"{num_scenarios} easy solvable scenarios saved to {output_file}.")

if __name__ == '__main__':
    num_scenarios = 2100
    generate_easy_scenarios(num_scenarios, moves=25)
