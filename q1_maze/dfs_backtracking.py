
# Author: Surinder Matharu
# Date Last Modified: 07-Nov-2026
# Purpose: This python file demonstrates a recursive backtracking DFS to find the best route through a downsampled 21x21 maze.

import os
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
from grid import (maze_binary, entrance_position, exit_position)

# Option 1: Depth-First Algorithm (Backtrack)
def dfs_backtrack_algorithm(current_position, final_position, maze, path, dfs_route_history):
    path_stack = [path.copy()]
    active_dfs_position = {current_position}
    ortho_dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while path_stack:
        current_route = path_stack.pop()
        current_position = current_route[-1]
        dfs_route_history.append(current_route.copy())

        if current_position == final_position:
            return True, current_route

        row, col = current_position
        for drow, dcol in ortho_dir:
            updated_row = row + drow
            updated_col = col + dcol
            next_step = (updated_row, updated_col)

            if not (0 <= updated_row < maze.shape[0] and 0 <= updated_col < maze.shape[1]):
                continue
            if maze[updated_row, updated_col] == 0 and next_step not in current_route:
                active_dfs_position.add(next_step)
                path_stack.append(current_route + [next_step])
    return False, path

 # Option 2. Las-Vegas Search Algorithm
def las_vegas_algorithm(maze, start, end, step_limit=200):
    current_vegas = start
    vegas_route = [start]
    steps = 0
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    visited = {start}

    while current_vegas != end and steps < step_limit:
        row, col = current_vegas
        possible_moves = [
            (row + drow, col + dcol) for drow, dcol in directions
        ]
        valid_positions = [
            move for move in possible_moves
            if 0 <= move[0] < maze.shape[0]
            and 0 <= move[1] < maze.shape[1]
            and maze[move[0], move[1]] == 0
            and move not in visited
        ]   
        if not valid_positions:
            
            break # Faces dead end
                
        current_vegas = random.choice(valid_positions)
        visited.add(current_vegas)
        vegas_route.append(current_vegas)
        steps += 1

    vegas_route_successful = current_vegas == end
    return vegas_route, steps, vegas_route_successful

def active_search(dfs_route_history):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(maze_binary, cmap='gray_r')
    plt.title('Maze Traversal')
    plt.plot(entrance_position[1], entrance_position[0], marker='o', color='cornflowerblue')
    plt.plot(exit_position[1], exit_position[0], marker= 'o', color ='seagreen')
    line, = ax.plot(
        [], [], marker='o', color='firebrick', linewidth=2.5,linestyle='-.', label='Depth-First Search Path'
    )
    ax.legend(loc='upper right')

    def init():
        line.set_data([], [])
        return (line,)
    
    #Seperate the columns and rows
    def update(frame):
        positions = dfs_route_history[frame]
        row_path, col_path = zip(*positions)
        line.set_data(col_path, row_path)
        return (line,)

    animation = FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(dfs_route_history),
        interval=100,
        blit=True,
        repeat=False,
    )

    return fig, animation

# Header print statments to introduce the two search algorithms 
print('Pick an approach:')
print('1. Depth-First Search (Backtracking)')
print('2. Las Vegas (Random)')

# User prompt to choose desired approach
approach = input('Please enter 1 or 2 to select desired approach: ').strip()

# Option 1: DFS animation display
if approach == '1':
    print('Processing with DFS Backtracking approach!')
    dfs_route_history =[]
    found_path, dfs_route_history = dfs_backtrack_algorithm(
    entrance_position,
    exit_position,
    maze_binary,
    [entrance_position],
    dfs_route_history,
    )

    if not found_path:
        raise ValueError("Entrance to Exit path could not be identified!")
    animation = active_search(dfs_route_history)
    #Gif animation generation and file path save
    dir_save = os.path.join("dfs-maze-outputs")
    os.makedirs(dir_save, exist_ok=True)

    filename = os.path.join(dir_save, "DFS_Walkthrough.gif")
    frame_count = len(dfs_route_history)
    print(f"Saving {frame_count} frames as GIF may take a while. Please be patient...")
    animation.save(filename, writer='pillow', fps=20)
    print(f'Depth-First Search trace with backtrack saved to: {filename}')
    plt.show()

#Option 2: Las Vegas Display

elif approach == '2':
    print('Processing with Las Vegas approach!')
    print('\nMaximum steps allowed for this approach is 200')
    vegas_route, steps, vegas_route_successful = las_vegas_algorithm(
        maze_binary,
        entrance_position,
        exit_position,
        step_limit=200,
    )
    # print(f'Las Vegas route {vegas_route}')
    print(f'Total number of steps taken:{steps}')
    if vegas_route_successful:
        print('SUCCESSFUL! Reached exit within step limit.')
    elif len(vegas_route) >= 200:
        print('UNSUCCESSFUL! Exit was not reached within step limit')
    else:
        print('UNSUCCESSFUL! Dead end!')
    
    fig, ax = plt.subplots(figsize=(8,8))
    ax.imshow(maze_binary, cmap='gray_r')
    plt.plot(entrance_position[1], entrance_position[0], marker='o', color='cornflowerblue')
    plt.plot(exit_position[1], exit_position[0], marker= 'o', color ='seagreen')

    if vegas_route:
        row_points, col_points = zip(*vegas_route)
        ax.plot(
            col_points,
            row_points,
            color='orange',
            linewidth=2, 
            marker='o',
            markersize=3,
            label= 'Las-Vegas',
        )

        ax.legend(loc='upper right')
        plt.show()
else:
    raise ValueError("Please enter 1 or 2 to select a valid approach.")