from general_Imports import *


def tdTomato_scene(brain_regions_to_evalutate,evaluate_brain_region_acronyms,evaluate_brain_regions,brain_regions_count_list,scene_tdTomato,loaded_cell_count_dict,extra_brain_region_names,scene_export_path):
    for i in range(brain_regions_to_evalutate):
        evaluate_brain_region_acronyms[i] = scene_tdTomato.add_brain_region(
            str(evaluate_brain_region_acronyms[i]), alpha=0.2, color='blue')
    if show_lables == True:
        for i in range(brain_regions_to_evalutate):
            # print(evaluate_brain_region_acronyms[i])
            scene_tdTomato.add_label(evaluate_brain_region_acronyms[i], str(
                evaluate_brain_regions[i])+' '+ str(brain_regions_count_list[i]))
  # # Add extra brain regions. specified in the extra_brain_region_acryonm list found in UpdateME.py
    list_len = len(extra_brain_region_acryonm)
    extra_cell_count_list = []
    if len(extra_brain_region_acryonm) == 0:
        print("adding no extra brain region to this render. to see addition brain regions, add their acryonms to the extra_brain_regions array in UpdateME.py. A full list of brain regions and their associated acryonms is saved in this repository as acronym_brainregions.csv'")
    else:
        for i in range(list_len):
            extra_brain_region_acryonm[i] = scene_tdTomato.add_brain_region(
            str(extra_brain_region_acryonm[i]), alpha=0.2, color='yellow')
        if show_lables == True:
            for i in range(list_len):
                for key in loaded_cell_count_dict.keys():
                    value = loaded_cell_count_dict.get(str(extra_brain_region_names[i]))
                    if value is None:
                        extra_cell_count_list.append('n/a')
                        scene_tdTomato.add_label(extra_brain_region_acryonm[i], str(extra_brain_region_names[i])+ ' ' + '(Manually Added)')
                        continue
                    cell_count = loaded_cell_count_dict[str(extra_brain_region_names[i])]
                    extra_cell_count_list.append(cell_count)
                    scene_tdTomato.add_label(extra_brain_region_acryonm[i], str(extra_brain_region_names[i])+ ' ' + str(cell_count) +' '+ '(Manually Added)')

                    extra_brain_regions_dictionary_with_cellcount = dict(
    zip(extra_brain_region_names, extra_cell_count_list))
    # create and add a cylinder actor to brain region with the most labled cells
     # mesh = shapes.Cylinder(pos=[top, pos], c=color, r=radius, alpha=alpha)
     #  :param pos: list, np.array of ap, dv, ml coordinates. If an actor is passed, get's the center of mass instead
    estim_cylinder_actor = Cylinder(
        # have cylinder run from the referece point to the brains surface 
        estim_tip_coordinates,
        scene_tdTomato.root,  # the cylinder actor needs information about the root mesh
        "black",
        1,
        estim_shank_radius_um,
     )

    # pos =  [opticalfiber_surface_coordinates,opticalfiber_tip_coordinates]
    # print(pos)
    opticalfiper_cylinder_actor = Cylinder(
        # have cylinder run from the referece point to the brains surface 
        opticalfiber_tip_coordinates,
        scene_tdTomato.root,  # the cylinder actor needs information about the root mesh
        'blue',
        1,
        opticalfiper_radius_um,
     )

    # check if 3D render has been saved out
    # if not export the 3D render, which can be opened in a web viewer
    if save_render == True:
        if not os.path.exists(scene_export_path):
            print('Saving out brainrender scence, this may take a few minutes...')
            scene_tdTomato.export(scene_export_path)
            # os.makedirs(scene_export_path)
            print('3D render has been created and saved too ')
            print(f'{scene_export_path}')

        else:
            print('A 3D-render of ' + str(mouse_id) + ' already exisits...')
            print('To save out a new render')
            print('Delete or remove pervious 3D-render from ' + f'{scene_export_path}' )
            print(' n')
    else:
        print('Render Not Saved....')