import matplotlib.pyplot as plt
import numpy as np

maze_img = plt.imread('supportingfiles/maze.png')
# print ("Maze Dimensions:", maze_img.shape)

maze_2d_shape = maze_img[:,:, 0]
# print ("2d Maze:", maze_2d_shape.shape)

maze_21x21 = maze_2d_shape[::10, ::10] ---> what if the image size change (resolution changes)??? Worth considering if there is a different way to do it?

maze_binary = np.where(maze_21x21>0.5, 0, 1)
# print(maze_binary.shape)
# print(maze_binary)

entrance = np.where(maze_binary[0, :] == 0)[0][0]
exit = np.where(maze_binary[-1, :] == 0)[0][0]

entrance_pos = (0, int(entrance))
exit_pos = (20, int(exit))

# print ("start:", entrance_pos)
# print ("end:", exit_pos)

plt.imshow(maze_binary, cmap='gray_r')
plt.plot(9,0, marker= 'o', color ='green')
plt.plot(11,20, marker = 'o', color ='blue')
plt.title('Maze')
plt.show()