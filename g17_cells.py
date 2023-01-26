# Path to cellfinder_output points.npy file
import numpy as np

g17_cells_path = '/Users/grant/Desktop/work/Denman_Lab/Cal_Light/brainrender/cellfinder_brainrender_output/cellfinder_output/points/g17_points.npy'
g17_points = np.load(g17_cells_path)
print('G17 normal')
print(g17_points)
print('')
print('G17 *100')
result = g17_points  * 1000
print(result)


points_path = '/Users/grant/Desktop/work/Denman_Lab/Cal_Light/brainrender/cellfinder_brainrender_output/cellfinder_output/points/points.npy'
points = np.load(points_path)
print('')
print('points Normal')
print(points)
print('')

