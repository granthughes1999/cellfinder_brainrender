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
from UpdateME import cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um, estim_tip_coordinates, extra_brain_region_acryonm
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


def run_brainrender(cellfinder_output_path, mouseid, brain_regions_to_evalutate, allen_mouse_10um):

    analyze_data_cellfinder(cellfinder_output_path, mouse_id)

    print('Creating 3D-render and histograms for')
    print("mouse_id: " + str(mouse_id))
    print("with estim_tip_coordinates :" +str(estim_tip_coordinates))
    
    # Create new brainrender folder in your cellfinder output folder
    brainrender_folder_path = cellfinder_output_path + \
        str(mouse_id) + "_Completed_Analysis/" +'brainrender_outputs' # create the path for the new folder

    if not os.path.exists(brainrender_folder_path):
        os.makedirs(brainrender_folder_path)
        print('brainrender_output folder has been created at')
        print(f'{brainrender_folder_path}')
        print('')
    else: 
        print('brainrender_output folder already exisits for ' + str(mouse_id) +' with estim_tip_coordinates of ' + str(estim_tip_coordinates))
    # Create new folder in your cellfinder output folder
    mouseid_estim_tip_coordinates_folder_path = brainrender_folder_path + '/' + str(mouse_id) + '_' + str(estim_tip_coordinates)   # create the path for the new folder
    histogram_folder_path = mouseid_estim_tip_coordinates_folder_path + '/' + str(mouse_id) + '_' + str(estim_tip_coordinates) + '_histograms'
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
        cells_path = cellfinder_output_path + 'points/points.npy'
        cells_path
        points = np.load(cells_path)
        hist_save_path = histogram_save_path +'/'+ str(mouse_id)+ '_' + str(estim_tip_coordinates) 

        # Subtract the reference point from each cell coordinate
        displacement = points - estim_tip_coordinates
        # Calculate the magnitude of the displacement vectors
        euclidean_distances = np.linalg.norm(displacement, axis=1)
        plt.hist(euclidean_distances, bins=500)
        # Add labels and a title
        plt.xlabel('Euclidean Distance (um)')
        plt.ylabel('number of cells')
        plt.title('Histogram of cell Euclidean distances from Estim tip')
        # Display & save the histogram
        hist_save_path = histogram_save_path +'/'+ str(mouse_id)+ '_' + str(estim_tip_coordinates) 
        plt.savefig(hist_save_path + '_euclidean_distances.png')
        np.save(npy_folder_path +'/'+ 'euclidean_distances.npy', euclidean_distances) 
        plt.close()
        sns.histplot(euclidean_distances, kde = True)
        plt.savefig(hist_save_path + '_sns_euclidean_distances.png')
        plt.close()

     
        # manhattan distances calculations: sum of the absolute differences of their coordinates
        manhattan_distances = np.sum(np.abs(points - estim_tip_coordinates), axis=1)
        manhattan_distances = distance.cdist(points, [estim_tip_coordinates], metric='cityblock')
        # Plot manhattan distances histogram
        plt.hist(manhattan_distances, bins = 100)
        # Add labels
        plt.title('Histogram of cell Manhattan distances from Estim tip')
        plt.xlabel('Manhattan distance (um)')
        plt.ylabel('number of cells')
        # Save the histogram
        plt.savefig(hist_save_path + '_manhattan_distances.png')
        np.save(npy_folder_path+'/' + 'manhattan_distances.npy', manhattan_distances) 
        plt.close()
        # create subplot with smooth line overlay
        sns.histplot(manhattan_distances, kde = True)
        plt.savefig(hist_save_path + '_sns_manhattan_distances.png')
        plt.close()

        p = 3
        minkowski_distances = distance.cdist(points, [estim_tip_coordinates], 'minkowski', p=p)

        plt.hist(minkowski_distances, bins=100)
        plt.xlabel('Minkowski Distance (um) (p={})'.format(p))
        plt.ylabel('Cell Count')
        plt.title('Histogram of Minkowski Distances')
        plt.savefig(hist_save_path + '_minkowski_distances.png')
        np.save(npy_folder_path +'/'+  'minkowski_distances.npy', minkowski_distances) 
        plt.close()
        sns.histplot(minkowski_distances, kde = True)
        plt.savefig(hist_save_path + '_sns_minkowski_distances.png')
        plt.close()


        chebyshev_distances = distance.cdist(points, [estim_tip_coordinates], 'chebyshev')
        plt.hist(chebyshev_distances, bins=100)
        plt.xlabel('Chebyshev Distance (um)')
        plt.ylabel('Cell count')
        plt.title('Histogram of Chebyshev Distances')
        plt.savefig(hist_save_path + '_chebyshev_distances.png')
        np.save(npy_folder_path +'/'+  'chebyshev_distances.npy', chebyshev_distances) 
        plt.close()
        sns.histplot(minkowski_distances, kde = True)
        plt.savefig(hist_save_path + '_sns_chebyshev_distances.png')
        plt.close()
    
    else:
        print('Skipping histogram creation...')
        print('Histograms for ' + str(mouse_id) + " with estim_tip_coordinates " + str(estim_tip_coordinates) + ' have already been created')
        print('')
       
    

    ## Sart of brainrender anylysis 
    scene_export_path = mouseid_estim_tip_coordinates_folder_path + '/' + mouse_id + '_' +str(estim_tip_coordinates)+ '_scence.html'

    # Path to cellfinder_output points.npy file
    cells_path = cellfinder_output_path + 'points/points.npy'
   
     # Load in all registered cell coordinates, and Define the reference point as one of those coordinates
    cells = np.load(cells_path)
    # reference_coord = cells[40000]
   

    # create points actors for brainrender to plot in the 3D render
    cells_actor = Points(cells_path)
    #  mesh = Sphere(pos=pos, r=radius, c=color, alpha=alpha, res=res)
    estim_tip_sphere_actor = Sphere(estim_tip_coordinates,100,"green",)



    # read in braingloab regions df, make lists of names and acryonms
    atlas = BrainGlobeAtlas("allen_mouse_50um")
    brain_regions_df = atlas.lookup_df.head(1000)

    brain_regions_acronym = brain_regions_df['acronym'].to_list()
    brain_regions_name = brain_regions_df['name'].to_list()

    BrainGlobeAtlas_dictionary = dict(
        zip(brain_regions_acronym, brain_regions_name))

    # File path to the saved json file
    file_path = cellfinder_output_path + mouseid + \
        "_Completed_Analysis/" + "gfp_brainregions_list.json"
    with open(file_path, 'r') as f:
        file_content = f.read()
        brain_regions_list = json.loads(file_content)

    count_file_path = cellfinder_output_path + mouseid + \
        "_Completed_Analysis/" + "gfp_brainregions_count.json"
    with open(count_file_path, 'r') as f:
        file_content = f.read()
        brain_regions_count_list = json.loads(file_content)

    # create a dictonary and df of brainregion acryonm and name, from the BrainGlobeAtlas. Because this is what brain render uses 
    brain_regions_dictionary = dict(
        zip(brain_regions_list, brain_regions_count_list))
    brain_regions_df = pd.DataFrame.from_dict(
        brain_regions_dictionary, orient='index')
    print("The "+str(brain_regions_to_evalutate) +
          " brain regions your loading with labled cells count")
    evaluate = list(brain_regions_dictionary.items())[
        :brain_regions_to_evalutate]
    print(evaluate)

    # create lists of just the brain regions you want to evaluate, uses brain_regions_to_evalutate variable value
    evaluate_brain_regions = brain_regions_list[0:brain_regions_to_evalutate]
    index = []
    for i in evaluate_brain_regions:
        index.append(brain_regions_name.index(i))

    evaluate_brain_region_acronyms = []
    for i in index:
        evaluate_brain_region_acronyms.append(brain_regions_acronym[i])

    evaluate_brain_regions_dictionary = dict(
        zip(evaluate_brain_regions, evaluate_brain_region_acronyms))
    evaluate_brain_regions_df = pd.DataFrame.from_dict(
        evaluate_brain_regions_dictionary, orient='index')
    evaluate_brain_regions_df.rename(index={0: 'acronym'}, inplace=True)

    # create lists of  the extra brain regions you want to evaluate, uses brain_regions_to_evalutate variable value
    index = []
    for i in extra_brain_region_acryonm:
        index.append(brain_regions_acronym.index(i))

    extra_brain_region_names = []
    for i in index:
        extra_brain_region_names.append(brain_regions_name[i])

    extra_brain_regions_dictionary = dict(
        zip(evaluate_brain_regions, evaluate_brain_region_acronyms))
    evaluate_brain_regions_df = pd.DataFrame.from_dict(
        evaluate_brain_regions_dictionary, orient='index')
    evaluate_brain_regions_df.rename(index={0: 'acronym'}, inplace=True)

    # unknown from cylinder example file on github
    settings.SHOW_AXES = False
    settings.WHOLE_SCREEN = False

    print(f"[{orange}]Running example: {Path(__file__).name}")

    # atlas version you want to use
    atlas = BrainGlobeAtlas('allen_mouse_50um', check_latest=False)

    # intialise brainrender scene
    scene = Scene(atlas_name='allen_mouse_50um', title=mouseid)
    print(scene.atlas.space)

    # add top brain regions and labels
    colors = ["red", 'orange', "yellow", "green", "blue", "red", 'orange',
              "yellow", "green", "blue", "red", 'orange', "yellow", "green", "blue","red", 'orange', "yellow", "green", "blue", "red", 'orange',
              "yellow", "green", "blue", "red", 'orange', "yellow", "green", "blue"]
    for i in range(brain_regions_to_evalutate):
        evaluate_brain_region_acronyms[i] = scene.add_brain_region(
            str(evaluate_brain_region_acronyms[i]), alpha=0.2, color=colors[i])

    for i in range(brain_regions_to_evalutate):
        print(evaluate_brain_region_acronyms[i])
        scene.add_label(evaluate_brain_region_acronyms[i], str(
            evaluate_brain_regions[i]))
    
 
    # # Add extra brain regions. specified in the extra_brain_region_acryonm list found in UpdateME.py

    list_len = len(extra_brain_region_acryonm)
    if len(extra_brain_region_acryonm) == 0:
        print("adding no extra brain region to this render. to see addition brain regions, add their acryonms to the extra_brain_regions array in UpdateME.py. A full list of brain regions and their associated acryonms is saved in this repository as acronym_brainregions.csv'")
    else:
        for i in range(list_len):
            extra_brain_region_acryonm[i] = scene.add_brain_region(
            str(extra_brain_region_acryonm[i]), alpha=0.2, color='yellow')

        for i in range(list_len):
            print(extra_brain_region_names[i])
            scene.add_label(extra_brain_region_acryonm[i], str(extra_brain_region_names[i]))



    # create and add a cylinder actor to brain region with the most labled cells
    # mesh = shapes.Cylinder(pos=[top, pos], c=color, r=radius, alpha=alpha)
    # densest_cell_brain_region_cylinder_actor = Cylinder(
    #     # center the cylinder at the center of mass of brain region with the most labled gfp cells, by using its varaible name
    #     evaluate_brain_region_acronyms[0],
    #     scene.root,
    #     'powderblue',
    #     1, 
    #     100,
    # )

    # create and add a cylinder actor to brain region with the most labled cells
     # mesh = shapes.Cylinder(pos=[top, pos], c=color, r=radius, alpha=alpha)
     #  :param pos: list, np.array of ap, dv, ml coordinates. If an actor is passed, get's the center of mass instead
    estim_cylinder_actor = Cylinder(
        # have cylinder run from the referece point to the brains surface 
        estim_tip_coordinates,
        scene.root,  # the cylinder actor needs information about the root mesh
        "yellow",
        1,
        100,
     )

    # NOT sure what this does, from brainrender documentation...
    # BGSpace AnatomicalSpace Objects
    # origin: ('Superior', 'Posterior', 'Lateral')
    # sections: ('Frontal plane')
    # shape: (528, 320, 456)


    # Add cells Actor to Scence
    scene.add(cells_actor, estim_tip_sphere_actor, estim_cylinder_actor,)

    # print the content of the scence
    scene.content

    # Add a sphere in the reference point location
    # scene.add_sphere(center = reference_point, radius = 25, color = 'red')

    # check if 3D render has been saved out
    # if not export the 3D render, which can be opened in a web viewer
    if not os.path.exists(scene_export_path):
        print('Saving out brainrender scence, this may take a few minutes...')
        scene.export(scene_export_path)
        # os.makedirs(scene_export_path)
        print('3D render has been created and saved too ')
        print(f'{scene_export_path}')

    else:
        print('A 3D-render of' + str(mouse_id) + ' already exisits...')
        print('To save out a new render')
        print('Delete or remove pervious 3D-render from ' + f'{scene_export_path}' )

    # locally Render the 3D brain Scence
    scene.render()
