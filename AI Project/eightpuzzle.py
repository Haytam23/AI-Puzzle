# eightpuzzle.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import util
import search
import random
from search import h1_misplaced_tiles,h2_manhattan_distance,h3_euclidean_distance,h4_out_of_row_and_column,aStarSearch,solveAndDisplay

# Module Classes

'''=====Start Change Task 1====='''

class FifteenPuzzleState:
    def __init__(self, numbers):
        if len(numbers) != 16:
            raise ValueError(f"Expected 16 elements for a 4x4 puzzle, got {len(numbers)} elements.")

        self.cells = []
        numbers = numbers[:]  # Make a copy to avoid side-effects.
        numbers.reverse()
        for row in range(4):  # 4 rows for the 15-puzzle.
            self.cells.append([])
            for col in range(4):  # 4 columns for the 15-puzzle.
                self.cells[row].append(numbers.pop())
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col


    def isGoal(self):
        """
        Checks to see if the puzzle is in its goal state with the blank in the bottom-right corner.

        The goal state for the 15-puzzle:
        -------------
        |  1 |  2 |  3 |  4 |
        -------------
        |  5 |  6 |  7 |  8 |
        -------------
        |  9 | 10 | 11 | 12 |
        -------------
        | 13 | 14 | 15 |    |
        -------------
        """
        current = 1
        for row in range(4):
            for col in range(4):
                if row == 3 and col == 3:
                    return self.cells[row][col] == 0  # Blank should be in the bottom-right corner.
                if self.cells[row][col] != current:
                    return False
                current += 1
        return True

    '''=====End Change Task 1====='''

    '''=====Start Change Task 1====='''

    def legalMoves(self):
        """
        Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left, or right.
        """
        moves = []
        row, col = self.blankLocation
        if row != 0:  # Can move up
            moves.append('up')
        if row != 3:  # Can move down
            moves.append('down')
        if col != 0:  # Can move left
            moves.append('left')
        if col != 3:  # Can move right
            moves.append('right')
        return moves

    '''=====End Change Task 1====='''


    def result(self, move):
        """
        Returns a new FifteenPuzzleState with the current state and blankLocation
        updated based on the provided move.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise Exception("Illegal Move")

        # Create a copy of the current puzzle with 16 elements for the 15-puzzle
        newPuzzle = FifteenPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        # Update the new puzzle to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle


    # Utilities for comparison and display
    
    def __eq__(self, other):
        return self.cells == other.cells

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
        Returns a display string for the puzzle.
        """
        lines = []
        horizontalLine = ('-' * (20))  # Adjusted width for 4x4 puzzle.
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

# TODO: Implement The methods in this class

class FifteenPuzzleSearchProblem(search.SearchProblem):
    """
    Implementation of a SearchProblem for the Fifteen Puzzle domain.

    Each state is represented by an instance of a FifteenPuzzle.
    """
    def __init__(self, puzzle):
        "Creates a new FifteenPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        """
        Returns list of (successor, action, stepCost) pairs where
        each successor is either left, right, up, or down from the original state
        and the cost is 1.0 for each.
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
        Returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        return len(actions)

'''=====Start Change Task 1====='''

FIFTEEN_PUZZLE_DATA = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0],  # Solved puzzle
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 14, 15, 13],  # Requires more moves
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 14, 13, 0],  # Complex puzzle
]

def loadFifteenPuzzle(puzzleNumber):
    """
    Load one of the predefined 15-puzzle configurations.
    """
    return FifteenPuzzleState(FIFTEEN_PUZZLE_DATA[puzzleNumber])

def createRandomFifteenPuzzle(moves=100):
    """
    Creates a random 15-puzzle by applying a series of random moves to a solved puzzle.
    """
    puzzle = FifteenPuzzleState([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0])
    for i in range(moves):
        puzzle = puzzle.result(random.choice(puzzle.legalMoves()))
    return puzzle

'''=====End Change Task 1====='''







# Debugging Step: Display heuristic values for key nodes in A*
def debug_heuristics(problem, heuristic_func):
    """Print the heuristic values at key points in the A* search."""
    frontier = util.PriorityQueue()
    exploredNodes = set()

    startState = problem.getStartState()
    startNode = (startState, [], 0)

    frontier.push(startNode, 0)
    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()

        # Print the heuristic value for the current state
        print(f"Heuristic for state:\n{currentState}")
        print(f"Heuristic value: {heuristic_func(currentState)}")

        if currentState not in exploredNodes:
            exploredNodes.add(currentState)

            if problem.isGoalState(currentState):
                print("Goal state reached.")
                return actions

            for succState, succAction, succCost in problem.getSuccessors(currentState):
                newAction = actions + [succAction]
                newCost = currentCost + succCost
                frontier.push((succState, newAction, newCost), newCost + heuristic_func(succState))

    return actions

if __name__ == '__main__':
    puzzle = createRandomFifteenPuzzle(25)
    print('A random puzzle:')
    print(puzzle)

    problem = FifteenPuzzleSearchProblem(puzzle)

    # Display heuristic values for the puzzle
    print(f"h1 (Misplaced Tiles): {h1_misplaced_tiles(puzzle)}")
    print(f"h2 (Manhattan Distance): {h2_manhattan_distance(puzzle)}")
    print(f"h3 (Euclidean Distance): {h3_euclidean_distance(puzzle)}")
    print(f"h4 (Out of Row and Column): {h4_out_of_row_and_column(puzzle)}")

    # Prompt user to choose a heuristic
    print("\nChoose which heuristic to use for solving the puzzle:")
    print("1. Misplaced Tiles (h1)")
    print("2. Manhattan Distance (h2)")
    print("3. Euclidean Distance (h3)")
    print("4. Out of Row and Column (h4)")
    choice = input("Enter your choice (1-4): ")

    # Solve the puzzle using the chosen heuristic
    if choice == "1":
        path = solveAndDisplay(problem, h1_misplaced_tiles, "Misplaced Tiles (h1)")
    elif choice == "2":
        path = solveAndDisplay(problem, h2_manhattan_distance, "Manhattan Distance (h2)")
    elif choice == "3":
        path = solveAndDisplay(problem, h3_euclidean_distance, "Euclidean Distance (h3)")
    elif choice == "4":
        path = solveAndDisplay(problem, h4_out_of_row_and_column, "Out of Row and Column (h4)")
    else:
        print("Invalid choice!")
        exit()

   