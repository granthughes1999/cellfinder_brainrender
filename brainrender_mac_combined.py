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
import variables
from variables import cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um 
import os



# From variables.py
# 1. How many top brain regions to evaluate. (default is 5)
brain_regions_to_evalutate = brain_regions_to_evalutate
# 2. path to cellfinder output folder
# cellfinder_output_path = "/Users/grant/Desktop/mock_df/cellfinder_output/"
cellfinder_output_path = cellfinder_output_path
# 3. path to local location of allen mouse brain atlas
allen_mouse_10um = allen_mouse_10um
# 4. mouse id (example: G25)
# mouseid = "test_000"
mouseid = mouse_id

def run_brainrender(cellfinder_output_path,mouseid,brain_regions_to_evalutate,allen_mouse_10um):

    def activate_env(brainrender_env_name):
        os.system("conda activate " + brainrender_env_name)

    activate_env("myenv")

    # Path to cellfinder_output points.npy file
    cells_path = cellfinder_output_path + 'points/points.npy'
    print(cells_path)

    # read in braingloab regions df, make lists of names and acryonms
    atlas = BrainGlobeAtlas("allen_mouse_50um")
    brain_regions_df = atlas.lookup_df.head(1000)

    brain_regions_acronym = brain_regions_df['acronym'].to_list()
    brain_regions_name = brain_regions_df['name'].to_list()

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

    brain_regions_dictionary = dict(
        zip(brain_regions_list, brain_regions_count_list))
    brain_regions_df = pd.DataFrame.from_dict(
        brain_regions_dictionary, orient='index')
    print("The "+str(brain_regions_to_evalutate) +
        " brain regions your loading with labled cells count")
    evaluate = list(brain_regions_dictionary.items())[:brain_regions_to_evalutate]
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

    # unknown from cylinder example file on github
    settings.SHOW_AXES = False
    settings.WHOLE_SCREEN = False

    print(f"[{orange}]Running example: {Path(__file__).name}")

    # atlas version you want to use
    atlas = BrainGlobeAtlas('allen_mouse_50um', check_latest=False)

    # intialise brainrender scene
    scene = Scene(atlas_name='allen_mouse_50um', title=mouseid)
    print(scene.atlas.space)

    # add brain regions and labels
    colors = ["red", 'orange', "yellow", "green", "blue", "red", 'orange',
            "yellow", "green", "blue", "red", 'orange', "yellow", "green", "blue"]
    for i in range(brain_regions_to_evalutate):
        evaluate_brain_region_acronyms[i] = scene.add_brain_region(
            str(evaluate_brain_region_acronyms[i]), alpha=0.2, color=colors[i])

    for i in range(brain_regions_to_evalutate):
        scene.add_label(evaluate_brain_region_acronyms[i], str(
            evaluate_brain_regions[i]))

    # You can specify color, transparency... of brain regions
    # VISp = scene.add_brain_region("VISp", alpha=0.2, color="green")
    # VISl = scene.add_brain_region('VISl',  alpha=0.2, color="red")
    # LGd = scene.add_brain_region('LGd', alpha=0.2, color="blue")
    # LP = scene.add_brain_region('LP', alpha=0.2, color="yellow")

    # # Add lables to brain regions'
    # scene.add_label(VISp, "Primary Visual area")
    # scene.add_label(VISl, "Lateral Visual area")
    # scene.add_label(LGd, "Lateral Geniculate Nucleus of the Thalmus")
    # scene.add_label(LP, "Lateral Posterior Thalmus")

    # create and add a cylinder actor to brain region with the most labled cells
    actor_electrode = Cylinder(
        # center the cylinder at the center of mass of Primary Visual area, by using its varaible name
        evaluate_brain_region_acronyms[0],
        scene.root,  # the cylinder actor needs information about the root mesh
    )

    # NOT sure what this does, from brainrender documentation...
    # BGSpace AnatomicalSpace Objects
    # origin: ('Superior', 'Posterior', 'Lateral')
    # sections: ('Frontal plane')
    # shape: (528, 320, 456)


    # create points actor
    cells = Points(cells_path)

    # Add cells Actor to Scence
    scene.add(cells, actor_electrode)

    # print the content of the scence
    scene.content

    # Render the 3D brain Scence
    scene.render()
