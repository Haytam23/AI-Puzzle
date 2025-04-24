
# AI-Puzzle
In this project, we undertook the challenge of solving the 15-puzzle problem using
heuristic-based search algorithms. Our objective was to implement and evaluate the
performance of four distinct admissible heuristics—h1, h2, h3, and h4—designed to
efficiently guide the search toward an optimal solution, with the blank space correctly
positioned in the bottom-right corner.
The project is structured into four key tasks. Task 1 focused on adapting the existing
codebase to handle the 15-puzzle, ensuring the proper handling of the puzzle configuration
and solvability. In Task 2, we implemented four heuristic functions: the number of misplaced
tiles, the sum of Manhattan distances, the sum of Euclidean distances, and the number of tiles
out of their respective rows and columns. Each heuristic was designed to solve the puzzle
with varying degrees of efficiency, and we rigorously tested them to verify their correctness
and performance.
Task 3 involved a detailed comparison of these heuristics by automatically generating a
variety of initial states for the 15-puzzle. We developed a script that allowed us to solve each
configuration using all four heuristics, capturing important performance metrics such as the
number of expanded nodes, maximum fringe size, and execution time. This comparison
enabled us to identify the most efficient heuristic for solving the puzzle.
In Task 4, we extended our analysis by comparing the best-performing heuristic from Task 3
against traditional uninformed search strategies, including breadth-first search (BFS) and
depth-first search (DFS). This comparison provided a comprehensive evaluation of the
strengths and weaknesses of heuristic-based search in relation to conventional search
techniques.
![image](https://github.com/user-attachments/assets/855e5649-e181-424c-bc9e-c21002be2104)
![image](https://github.com/user-attachments/assets/6672e6f1-2705-47bb-93ec-fc840d2b10c4)

