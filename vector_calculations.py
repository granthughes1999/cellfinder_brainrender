# import pandas as pd
# import numpy as np
# import UpdateME 
# from UpdateME import cellfinder_output_path, estim_tip_coordinates
# import matplotlib.pyplot as plt
# from scipy.spatial import distance
# import seaborn as sns
# from bg_atlasapi.bg_atlas import BrainGlobeAtlas


# # Path to cellfinder_output points.npy file
# cells_path = cellfinder_output_path + 'points/points.npy'
# cells_path
# points = np.load(cells_path)

# # Define the reference point 
# estim_cell_coordinates = points[50000:50100]
# estim_tip_for_testing = points[50050]
# # np.save('/Users/grant/Desktop/mock_estim_cell_coords/100_cells.npy',estim_cell_coordinates)


# # Subtract the reference point from each cell coordinate
# displacement = points - estim_tip_coordinates
# # Euclidean Distance: Calculate the magnitude of the displacement vectors
# distances = np.linalg.norm(displacement, axis=1)
# # create a histogram for Euclidean Distance
# plt.hist(distances, bins=500)
# # Add labels and a title
# plt.xlabel('Euclidean Distance (um)')
# plt.ylabel('number of cells')
# plt.title('Histogram of cell Euclidean distances from a Estim tip')
# # Display the histogram
# plt.show()

# # manhattan distances calculations: sum of the absolute differences of their coordinates
# manhattan_distances = np.sum(np.abs(points - estim_tip_coordinates), axis=1)
# manhattan_distances = distance.cdist(points, [estim_tip_coordinates], metric='cityblock')
# # Plot manhattan distances histogram
# plt.hist(manhattan_distances, bins = 100)
# # Add labels
# plt.title('Histogram of cell Manhattan distances from Estim tip')
# plt.xlabel('Manhattan distance (um)')
# plt.ylabel('number of cells')
# # Display the histogram
# plt.show()
# # create subplot with smooth line overlay
# sns.histplot(manhattan_distances, kde = True)
