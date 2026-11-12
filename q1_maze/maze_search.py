# Author: Surinder Matharu
# Date Last Modified: 12-Nov-2026
# Purpose: Script visualises a Depth-First search (with backtracking) and a Las Vegas random search. 
#          It utilises the downsampled version of the maze.img generated in grid.py.
# References: 

import random
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 
from grid import (maze_binary, entrance_position, exit_position)

# Option 1: Depth-First Algorithm (DFS)
#           DFS methodically traverses the maze using a Last-In-First-Out (LIFO) stack with built-in backtracking, making it easy to 'pop' dead ends. It also 
#           follows each path as deep as possible until it reaches a dead end (Standford University, 2026)
def dfs_backtrack_algorithm(current_position, final_position, maze, path, dfs_route_history):
    
    # Assigning path_stack with a copy of path to start with 
    # ortho_dir sets the required orthogonal movements: left, right, up, down

    path_stack = [path.copy()]
    ortho_dir = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # The while loop implements the LIFO method by popping the most recently visited route. 
        # Append dfs_route_history to capture a copy for animation frames. 
    while path_stack:
        current_route = path_stack.pop()
        current_position = current_route[-1]
        dfs_route_history.append(current_route.copy())

        # Base case: Checks whether current_position matches final_position (exit). 
        #            If so, stops the search and returns the route taken.
        if current_position == final_position:
            return True, current_route

        # Investigates adjacent positions (neighbours) to ensure they are within maze wall boundaries.  
        row, col = current_position
        for drow, dcol in ortho_dir:
            updated_row = row + drow
            updated_col = col + dcol
            next_step = (updated_row, updated_col)

            # Prevents the algorithm friom leaving the physical maze grid by checking that the row index is 
            # between 0 and maze.shape[0] (total rows), and the column index is between 0 and maze.shape[1] (total columns). 
            # If a move exceeds these boundaries, the algorithm should ignore it. 
            if not (0 <= updated_row < maze.shape[0] and 0 <= updated_col < maze.shape[1]):
                continue

            # Checks whether the next position is unvisited and open.
            # path_stack-sppend adds the next path onto the stack for exploration. 
            if maze[updated_row, updated_col] == 0 and next_step not in current_route:
                path_stack.append(current_route + [next_step])
    return False, path

# Option 2: Las-Vegas Search Algorithm
#           Las Vegas randomly chooses unvisited nrighbours to try find a route to the exit (final_position).
#           An iteration limit has been set to prevent infinite loops.
def las_vegas_algorithm(maze, start, end, step_limit=200):
    current_vegas = start
    vegas_route = [start]
    steps = 0
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    visited = {start}

    # While condition: Randomised walk continue until it finds the exit, reaches a dead end, or hits the 200-step limit.
    while current_vegas != end and steps < step_limit:
        # Splits the current_vegas position into separate row and column variables.
        row, col = current_vegas

        # Calculates all possible_moves that are orthogonal to current_vegas position
        possible_moves = [
            (row + drow, col + dcol) for drow, dcol in directions
        ]
        # Checks that surrounding positions are within the grid, unblocked, and unvisited to prevent looping.
        valid_positions = [
            move for move in possible_moves
            if 0 <= move[0] < maze.shape[0]
            and 0 <= move[1] < maze.shape[1]
            and maze[move[0], move[1]] == 0
            and move not in visited
        ]

        # This deals with dead end issues and attempts to restart the random las vegas search
        if not valid_positions:
            current_vegas = start
            visited = {start} # Clear visited history to restart search
            vegas_route =[start] 
            continue # Loop restarts

        # Stochastic decision-making used to select a random open, valid position. 
        # The current_vegas postion is added to the visited list to prevent revisiting this position.
        # The path records each step, and the step count increases by 1. This helps keep track of step count to ensure algorithm stays within the 200-step limit.     
        current_vegas = random.choice(valid_positions) # picks random choice from valid unvisited position
        visited.add(current_vegas) # Adds new position to visited set to avoid it being re-visited
        vegas_route.append(current_vegas) # Helps keep record of all steps taken 
        steps += 1

    vegas_route_successful = current_vegas == end
    return vegas_route, steps, vegas_route_successful

# To provide animations for DFS (with backtracking)
def active_search(dfs_route_history):

    # Heavily relies on Matplotlib tools to create an animation that combines live route exploration with a dotted trail of visited location.
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(maze_binary, cmap='gray_r')
    plt.title('Maze Traversal I Backtracking')
    plt.plot(entrance_position[1], entrance_position[0], marker='o', color='cornflowerblue')
    plt.plot(exit_position[1], exit_position[0], marker= 'o', color ='seagreen')
    
    # To track visited trails a scatter collection is used. 
    visited_trail = ax.scatter(
       [],[], color='coral', alpha=0.3, s=20, label='Visited Route Dots')
    # Live route exploration line showing the traversal stack's active position. 
    line, = ax.plot(
        [], [], marker='o', color='firebrick', linewidth=2.5,linestyle='-.', label='live Route Exploration'
    )
    ax.legend(loc='upper right')

   # Sets blank canvas, clears the previous exploration line and visited trail dots when the animation begins.
    def init():
        line.set_data([], [])
        visited_trail.set_offsets([[0,0]])
        return line, visited_trail

    def update(frame):
        # Collects positions visited from entrance to current position.
        total_frame_visits = []
        for snapshot in dfs_route_history[: frame + 1]:
          total_frame_visits.extend(snapshot)

        # Removes duplicate positions whilst preserving initial visit order.
        explored_paths = list(dict.fromkeys(total_frame_visits))
        if explored_paths:
            row_visited, col_visited = zip(*explored_paths)
            # Swap row and column points to match the graph coordinate orientation. (i.e. Matrix (row, col) whereas graph is (col,row))
            visited_trail.set_offsets(list(zip(col_visited, row_visited)))


        positions = dfs_route_history[frame]
        row_path, col_path = zip(*positions)
        line.set_data(col_path, row_path)
        
        return line, visited_trail

    # FuncAnimation generates the Matplotlib anmimation tool. It calls the update function at each search stepis a Matplotlib tool used to generate the animation. It calls
    # the update function at each search step to capture the exploration line and visited dots frame-by-frame for playback as a GIF. 
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

# DFS execution (Option 1): This inclides GIF animation display and save
if approach == '1':
    print('Processing with DFS Backtracking approach!')
    dfs_route_history = []
    found_path, route = dfs_backtrack_algorithm(
    entrance_position,
    exit_position,
    maze_binary,
    [entrance_position],
    dfs_route_history,
    )

    if not found_path:
        raise ValueError("Entrance to Exit path could not be identified!")
    
    fig, animation = active_search(dfs_route_history)

    # Animation frames are saved as a GIF within dfs_maze_traversal folder.
    dir_save = os.path.join("dfs_maze_traversal")
    os.makedirs(dir_save, exist_ok=True)

    filename = os.path.join(dir_save, "DFS_Walkthrough.gif")
    frame_count = len(dfs_route_history)
    print(f"Saving {frame_count} frames as GIF may take a while. Please be patient...")
    animation.save(filename, writer='pillow', fps=20)
    print(f'Depth-First Search trace with backtrack saved to: {filename}')
    plt.show()

# Las Vegas Execution (2): Static visual
elif approach == '2':
    print('Processing with Las Vegas approach!')
    print('\nMaximum steps allowed for this approach is 200')
    vegas_route, steps, vegas_route_successful = las_vegas_algorithm(
        maze_binary,
        entrance_position,
        exit_position,
        step_limit=200,
    )

    print(f'Total number of steps taken:{steps}')
    if vegas_route_successful:
        print('SUCCESSFUL! Reached exit within step limit.')
    elif steps >= 200:
        print('Unsuccessful! Exit was not reached within step limit')
    # else:
    #     print('Unsuccessful! Blocked, hit a dead end.')
    
    fig, ax = plt.subplots(figsize=(8,8))
    ax.imshow(maze_binary, cmap='gray_r')
    plt.plot(entrance_position[1], entrance_position[0], marker='o', color='cornflowerblue')
    plt.plot(exit_position[1], exit_position[0], marker= 'o', color ='seagreen')

    if vegas_route:
        row_points, col_points = zip(*vegas_route)
        ax.plot(col_points, row_points, color='firebrick',linewidth=2, marker='o', markersize=3, label= 'Las-Vegas',)

    ax.legend(loc='upper right')

    dir_save = os.path.join('lasvegas_maze_traversal')
    os.makedirs(dir_save, exist_ok=True)

    filename = os.path.join(dir_save, 'LasVegas.png')
    fig.savefig(filename)
    print(f'Las Vegas route saved to {filename}')
    plt.show()
    plt.close()

else:
    raise ValueError("Invalid input. Please enter '1' for DFS or '2' for Las Vegas approach.")