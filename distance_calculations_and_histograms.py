from brainrender.scene import Scene
from brainrender.actors import Points
from bg_atlasapi.bg_atlas import BrainGlobeAtlas
from brainrender import settings
from brainrender.actors import Cylinder
import bg_space as bg
import numpy as np
from rich import print
from myterial import orange
from pathlib import Path
import pandas as pd
import json
from bg_atlasapi import show_atlases
from bg_atlasapi.bg_atlas import BrainGlobeAtlas
import UpdateME
from UpdateME import cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um, estim_tip_coordinates, extra_brain_region_acryonm, estim_shank_radius_um, estim_tip_radius_um, estim_propigation_radius_um
import os
import brainrender
from vedo import Spheres, Sphere
from vedo import Points as vPoints
import matplotlib.pyplot as plt
from scipy.spatial import distance
import seaborn as sns
brainrender.SHADER_STYLE = "cartoon"
import cellfinder_backend
from cellfinder_backend import analyze_data_cellfinder
import pickle 
# from brainrender_backend import brainrender_folder_path 


def distance_calculations_histograms(brainrender_folder_path,mouse_id,estim_tip_coordinates,cellfinder_output_path):
    # Create new folder in your cellfinder output folder
    mouseid_estim_tip_coordinates_folder_path = brainrender_folder_path + '/' + str(mouse_id) + '_' + str(estim_tip_coordinates)   # create the path for the new folder
    histogram_folder_path = mouseid_estim_tip_coordinates_folder_path + '/' + str(mouse_id) + '_' + str(estim_tip_coordinates) + '_histograms/tdTomato_cells'
    npy_folder_path = histogram_folder_path + '/' + "distance_arrays"
    if not os.path.exists(histogram_folder_path):
        os.makedirs(histogram_folder_path)
        os.makedirs(npy_folder_path)
        print('Histogram folder has been created at')
        print(f'{ histogram_folder_path}')
        print('')
        print('Making histograms...')
        print('')

        histogram_save_path = histogram_folder_path 
        # npy_save_path = histogram_save_path + '/' + 'distance_arrays'
        # Calaculate 3d-space distances for cells relative to estim_tip_coordinates. and save out histograms of those distances
        # Path to cellfinder_output points.npy file
        print('cellfinder Output Path:' + str(cellfinder_output_path))
        tdTomato_cells_path = cellfinder_output_path + 'points/tdTomato_points.npy'
        tdTomato_cells_path
        points = np.load(tdTomato_cells_path)
        hist_save_path = histogram_save_path +'/'+ str(mouse_id)+ '_' + str(estim_tip_coordinates) + '/tdTomato_cells'

        # Subtract the reference point from each cell coordinate
        displacement = points - estim_tip_coordinates
        # Calculate the magnitude of the displacement vectors
        euclidean_distances = np.linalg.norm(displacement, axis=1)
        plt.hist(euclidean_distances, bins=25)
        # Add labels and a title
        plt.xlabel('Euclidean Distance (um)')
        plt.ylabel('number of cells')
        plt.title(str(mouse_id) + ' tdTomato, Histogram of cell Euclidean distances from Estim tip')
        # Display & save the histogram
        hist_save_path = histogram_save_path +'/'+ str(mouse_id)+ '_' + str(estim_tip_coordinates) 
        plt.savefig(hist_save_path + '_euclidean_distances.png')
        np.save(npy_folder_path +'/'+ 'euclidean_distances.npy', euclidean_distances) 
        plt.close()
        sns.histplot(euclidean_distances, kde = True)
        plt.xlabel('Euclidean Distance (um)')
        plt.ylabel('number of cells')
        plt.title(str(mouse_id) + ' tdTomato, Histogram of cell Euclidean distances from Estim tip')
        plt.savefig(hist_save_path + '_sns_euclidean_distances.png')
        plt.close()


        # manhattan distances calculations: sum of the absolute differences of their coordinates
        manhattan_distances = np.sum(np.abs(points - estim_tip_coordinates), axis=1)
        manhattan_distances = distance.cdist(points, [estim_tip_coordinates], metric='cityblock')
        # Plot manhattan distances histogram
        plt.hist(manhattan_distances, bins = 25)
        # Add labels
        plt.title(str(mouse_id) + ' tdTomato, Manhattan distances from Estim tip')
        plt.xlabel('Manhattan distance (um)')
        plt.ylabel('number of cells')
        # Save the histogram
        plt.savefig(hist_save_path + '_manhattan_distances.png')
        np.save(npy_folder_path+'/' + 'manhattan_distances.npy', manhattan_distances) 
        plt.close()
        # create subplot with smooth line overlay
        sns.histplot(manhattan_distances, kde = True)
        plt.title(str(mouse_id) + ' tdTomato, Manhattan distances from Estim tip')
        plt.xlabel('Manhattan distance (um)')
        plt.ylabel('number of cells')
        plt.savefig(hist_save_path + '_sns_manhattan_distances.png')
        plt.close()

        p = 3
        minkowski_distances = distance.cdist(points, [estim_tip_coordinates], 'minkowski', p=p)

        plt.hist(minkowski_distances, bins=25)
        plt.xlabel('Minkowski Distance (um) (p={})'.format(p))
        plt.ylabel('Cell Count')
        plt.title(str(mouse_id) + ' tdTomato, Minkowski Distances from estim tip')
        plt.savefig(hist_save_path + '_minkowski_distances.png')
        np.save(npy_folder_path +'/'+  'minkowski_distances.npy', minkowski_distances) 
        plt.close()
        sns.histplot(minkowski_distances, kde = True)
        plt.xlabel('Minkowski Distance (um) (p={})'.format(p))
        plt.ylabel('Cell Count')
        plt.title(str(mouse_id) + ' tdTomato, Minkowski Distances from estim tip')
        plt.savefig(hist_save_path + '_sns_minkowski_distances.png')
        plt.close()


        chebyshev_distances = distance.cdist(points, [estim_tip_coordinates], 'chebyshev')
        plt.hist(chebyshev_distances, bins=25)
        plt.xlabel('tdTomato, Chebyshev Distance (um)')
        plt.ylabel('Cell count')
        plt.title(str(mouse_id) + ' tdTomato Chebyshev Distances from estim tip')
        plt.savefig(hist_save_path + '_chebyshev_distances.png')
        np.save(npy_folder_path +'/'+  'chebyshev_distances.npy', chebyshev_distances) 
        plt.close()
        sns.histplot(minkowski_distances, kde = True)
        plt.xlabel('tdTomato, Chebyshev Distance (um)')
        plt.ylabel('Cell count')
        plt.title(str(mouse_id) + ' tdTomato Chebyshev Distances from estim tip')
        plt.savefig(hist_save_path + '_sns_chebyshev_distances.png')
        plt.close()

    else:
        print('Skipping histogram creation, because ' + 'histograms for ' + str(mouse_id) + " with estim_tip_coordinates " + str(estim_tip_coordinates) + ' have already been created')
        print('')