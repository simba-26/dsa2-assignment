
# Author: Surinder Matharu
# Date Last Modified: 31-Oct-2026
# Purpose: This python file demonstrates a recursive backtracking DFS to find the best route through a downsampled 21x21 maze.

import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
from grid import (maze_binary, entrance_position, exit_position)

# Maze grid is recursively explored using DFS.
def dfs_backtrack_algorithm(current_position, final_position, maze, path, visited_history=None):
    if visited_history is None:
        visited_history = []
    visited_history.append(path.copy())

    if current_position == final_position:
        return True, path

    # Setting orthogonal movements (Left, Right, Up, Down)
    row, col = current_position
    ortho_dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]


    # Trigger For loop to test different directions
    for drow, dcol in ortho_dir:
        updated_row = row + drow
        updated_col = col + dcol
        next_step = (updated_row, updated_col)

        # Keep new path coordinates in 21x21 boundary, recursion and backtrack
        if not (0 <= updated_row < maze.shape[0] and 0 <= updated_col < maze.shape[1]):
            continue
        if maze[updated_row, updated_col] == 0 and next_step not in path:
            path.append(next_step)
            found_path, route = dfs_backtrack_algorithm(
                next_step, final_position, maze, path, visited_history
            )
            if found_path:
                return True, route
            path.pop()
    return False, path

# Maze bacground display with visited line plot
def visited_path_plot(visited_history):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(maze_binary, cmap='gray_r')
    plt.title('Maze')
    plt.plot(9,0, marker= 'o', color ='cornflowerblue')
    plt.plot(11,20, marker= 'o', color ='seagreen')
    line, = ax.plot(
        [], [], marker='o', color='firebrick', linewidth=2.5,linestyle='-.', label='Depth-First Search Path'
    )
    ax.legend()

    def init():
        line.set_data([], [])
        return (line,)
    
    #Seperate the columns and rows
    def update(frame):
        positions = visited_history[frame]
        row_path = [row for row, col in positions]
        col_path = [col for row, col in positions]
        line.set_data(col_path, row_path)
        return (line,)

    animation = FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(visited_history),
        interval=100,
        blit=True,
        repeat=False,
    )

    return animation

if __name__== "__main__":
    visited_history = []
    found_path, route = dfs_backtrack_algorithm(
        entrance_position,
        exit_position,
        maze_binary, 
        [entrance_position], 
        visited_history,
    )

    if not found_path:
        raise ValueError("Entrance to Exit path could not be identified!")
    animation = visited_path_plot(visited_history)

     # Gif animation generation and file path save
    dir_save = os.path.join("dfs-maze-outputs")
    os.makedirs(dir_save, exist_ok=True)

    filename = os.path.join(dir_save, "DFS_Walkthrough.gif")
    print("Please wait while the frames render and the GIF saves..")
    animation.save(filename, writer='pillow', fps=20)
    print(f'Depth-First Search trace with backtrack saved to: {filename}')

    plt.show()