# search.py
import util
import math

class SearchProblem:
    """
    This class outlines the structure of a search problem but doesn't implement
    any of the methods (an abstract class).
    """

    def getStartState(self):
        util.raiseNotDefined()

    def isGoalState(self, state):
        util.raiseNotDefined()

    def getSuccessors(self, state):
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem, depth_limit=30):
    """Search the deepest nodes in the search tree first."""
    frontier = util.Stack()
    exploredNodes = set()
    frontier.push((problem.getStartState(), [], 0))  # (state, actions, current_depth)

    max_fringe_size = len(frontier.list)

    while not frontier.isEmpty():
        state, actions, current_depth = frontier.pop()

        max_fringe_size = max(max_fringe_size, len(frontier.list))

        if current_depth > depth_limit:
            continue

        if state not in exploredNodes:
            exploredNodes.add(state)

            if problem.isGoalState(state):
                return actions, len(exploredNodes), max_fringe_size, current_depth

            for successor, action, _ in problem.getSuccessors(state):
                new_actions = actions + [action]
                frontier.push((successor, new_actions, current_depth + 1))

    return [], len(exploredNodes), max_fringe_size, 'N/A'


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    frontier = util.Queue()
    exploredNodes = set()
    frontier.push((problem.getStartState(), [], 0))

    max_fringe_size = len(frontier.list)

    while not frontier.isEmpty():
        state, actions, _ = frontier.pop()

        max_fringe_size = max(max_fringe_size, len(frontier.list))

        if state not in exploredNodes:
            exploredNodes.add(state)

            if problem.isGoalState(state):
                return actions, len(exploredNodes), max_fringe_size, len(actions)

            for successor, action, _ in problem.getSuccessors(state):
                new_actions = actions + [action]
                frontier.push((successor, new_actions, 0))

    return [], len(exploredNodes), max_fringe_size, 'N/A'


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    frontier = util.PriorityQueue()
    exploredNodes = {}
    frontier.push((problem.getStartState(), [], 0), 0)

    max_fringe_size = len(frontier.heap)

    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()

        max_fringe_size = max(max_fringe_size, len(frontier.heap))

        if state not in exploredNodes or cost < exploredNodes[state]:
            exploredNodes[state] = cost

            if problem.isGoalState(state):
                return actions, len(exploredNodes), max_fringe_size, len(actions)

            for successor, action, step_cost in problem.getSuccessors(state):
                new_actions = actions + [action]
                new_cost = cost + step_cost
                frontier.update((successor, new_actions, new_cost), new_cost)

    return [], len(exploredNodes), max_fringe_size, 'N/A'


def nullHeuristic(state, problem=None):
    return 0

'''=====Start Change Task 2====='''

def h1_misplaced_tiles(state, problem=None):
    """h1: Misplaced Tiles Heuristic"""
    misplaced_tiles = 0
    goal = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]
    for row in range(4):
        for col in range(4):
            if state.cells[row][col] != 0 and state.cells[row][col] != goal[row * 4 + col]:
                misplaced_tiles += 1
    return misplaced_tiles


def h2_manhattan_distance(state, problem=None):
    """h2: Manhattan Distance Heuristic"""
    manhattan_distance = 0
    for row in range(4):
        for col in range(4):
            tile = state.cells[row][col]
            if tile != 0:
                goal_row = (tile - 1) // 4
                goal_col = (tile - 1) % 4
                manhattan_distance += abs(row - goal_row) + abs(col - goal_col)
    return manhattan_distance


def h3_euclidean_distance(state, problem=None):
    """h3: Euclidean Distance Heuristic"""
    euclidean_distance = 0
    for row in range(4):
        for col in range(4):
            tile = state.cells[row][col]
            if tile != 0:
                goal_row = (tile - 1) // 4
                goal_col = (tile - 1) % 4
                distance = math.sqrt((row - goal_row) ** 2 + (col - goal_col) ** 2)
                euclidean_distance += distance
    return euclidean_distance


def h4_out_of_row_and_column(state, problem=None):
    """h4: Out of Row and Column Heuristic"""
    out_of_row = 0
    out_of_column = 0
    for row in range(4):
        for col in range(4):
            tile = state.cells[row][col]
            if tile != 0:
                goal_row = (tile - 1) // 4
                goal_col = (tile - 1) % 4
                if row != goal_row:
                    out_of_row += 1
                if col != goal_col:
                    out_of_column += 1
    return out_of_row + out_of_column
'''=====End Change Task 2====='''



'''=====Start Change Task 2====='''

# Scaling factor for heuristic influence
HEURISTIC_SCALE = 1.5


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    exploredNodes = set()

    startState = problem.getStartState()
    startNode = (startState, [], 0)

    frontier.push(startNode, 0)

    while not frontier.isEmpty():
        currentState, actions, currentCost = frontier.pop()

        if currentState not in exploredNodes:
            exploredNodes.add(currentState)

            if problem.isGoalState(currentState):
                return actions, len(exploredNodes), len(frontier.heap), len(actions)

            for succState, succAction, succCost in problem.getSuccessors(currentState):
                newActions = actions + [succAction]
                newCost = currentCost + succCost
                heuristic_value = heuristic(succState, problem) * HEURISTIC_SCALE
                frontier.push((succState, newActions, newCost), newCost + heuristic_value)

    return [], len(exploredNodes), len(frontier.heap), 'N/A'


# Solve the problem and display the solution path
def solveAndDisplay(problem, heuristic_func, heuristic_name):
    """Run A* search using the specified heuristic, and print the solution path."""
    print(f"\nSolving with {heuristic_name}:")
    path, expanded_nodes, max_fringe_size, depth = aStarSearch(problem, heuristic=heuristic_func)
    
    print(f"A* with {heuristic_name} found a path of {len(path)} moves.")
    print(f"Nodes expanded: {expanded_nodes}")
    print(f"Maximum fringe size: {max_fringe_size}")
    print(f"Search depth: {depth}")

    current_state = problem.getStartState()
    print("Initial State:")
    print(current_state)

    i = 1
    for move in path:
        current_state = current_state.result(move)
        print(f"\nAfter move {i}: {move}")
        print(current_state)
        i += 1

    return path


# Abbreviations for easier testing
astar_h1 = lambda problem: aStarSearch(problem, heuristic=h1_misplaced_tiles)
astar_h2 = lambda problem: aStarSearch(problem, heuristic=h2_manhattan_distance)
astar_h3 = lambda problem: aStarSearch(problem, heuristic=h3_euclidean_distance)
astar_h4 = lambda problem: aStarSearch(problem, heuristic=h4_out_of_row_and_column)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch

'''=====End Change Task 2====='''
