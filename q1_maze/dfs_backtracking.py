
# Author: Surinder Matharu
# Date Last Modified: 30-Oct-2026
# Purpose: This python file demonstrates a recursive backtracking DFS to find the best route through a downsampled 21x21 maze.

from grid import (maze_binary, entrance_position, exit_position)

# Maze grid is recurisively explored using DFS. 

def dfs_backtrack_algorithm (current_position, final_position, maze, path):

    if current_position == final_position:
        return True, path

    # Setting orthogonal movements (Left, Right, Up, Down)
    row, col = current_position 
    ortho_dir = [(0,-1), (0,1), (-1,0), (1,0)]

    # Trigger For loop to test different directions
    for drow, dcol in ortho_dir:
        updated_row = row + drow
        updated_col = col + dcol
        next_step = (updated_row, updated_col)

        # Keep new path coordinates in 21x21 boundary, recursion and backtrack
        if not (0 <= updated_row < maze.shape[0] and 0 <= updated_col < maze.shape[1]):
            continue
        if maze[updated_row, updated_col] == 0 and next_step not in path:
            path.append((next_step))
            found_path, route = dfs_backtrack_algorithm (
                (next_step), final_position, maze, path + [next_step]
            )
            if found_path: 
                return True, route
            path.pop()
    return False, path 

# print("Result:", dfs_result)