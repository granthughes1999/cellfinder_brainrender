from general_Imports import *



def run_brainrender(cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um,estim_shank_radius_um,estim_tip_radius_um,estim_propigation_radius_um,extra_brain_region_acryonm,show_lables,estim_tip_coordinates,save_render,show_gfp_tdTomato_overlapping,show_gfp_only,show_tdTomato_only,overlapping_cells_only,brain_region_estim
):
    cellfinder_output_path = cellfinder_output_path
    mouseid = mouse_id

    data = {'mouse_id': str(mouse_id),
            'cellfinder_output_path': str(cellfinder_output_path),
            'estim_tip_coordinates': str(estim_tip_coordinates),
            'opticalfiber_tip_coordinates' : str(opticalfiber_tip_coordinates),
            'opticalfiber_propigation_radius_um' : str(opticalfiber_propigation_radius_um),
            'estim_shank_radius_um' : str(estim_shank_radius_um) ,
            'estim_tip_radius_um' : str(estim_tip_radius_um),
            'estim_propigation_radius_um' : str(estim_propigation_radius_um),
            'opticalfiper_radius_um' : str(opticalfiper_radius_um),
            'brain_regions_to_evalutate' : str(brain_regions_to_evalutate),
            'extra_brain_region_acryonm' : str(extra_brain_region_acryonm),
            'allen_mouse_10um' : str(allen_mouse_10um) }
    upddateME_df = pd.DataFrame(data,index=[0])
    upddateME_df = upddateME_df.melt()
    

    # df = df.melt(id_vars=["name"], var_name="variable", value_name="value")
    # Run the function from cellfinder_backend.py
    analyze_data_cellfinder(cellfinder_output_path, mouse_id) # ADD BACK HERE cellfinder_output_path, mouse_id
    print(' ')
    print("Running brainrender_backend.py")
    print('Creating 3D-render and calculating distances for each cell relative to your estim_tip_coordinates')
    print("mouse_id: " + str(mouse_id))
    print("estim_tip_coordinates :" +str(estim_tip_coordinates))
    print(' ')
    
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
    
    # run distance_calculations_histograms() from distance_calculation_and_histograms.py
    # calculates 3d-space distances, saves out each cells distance in arrays, and creates histograms of those distances relative to the estim_tip coordinates
    distance_calculations_histograms(brainrender_folder_path,mouse_id,estim_tip_coordinates)

    #Save out the updateME datafram
    updateME_save_path = cellfinder_output_path + str(mouse_id) + "_Completed_Analysis/UpdateME.csv" 
    upddateME_df.to_csv(updateME_save_path, index=False)
    

    ## Sart of brainrender anylysis 
    scene_export_path = brainrender_folder_path + '/' + str(mouse_id) + '_' + str(estim_tip_coordinates) +  '/scence_' + str(mouse_id) + '_' + str(estim_tip_coordinates) + '.html'









    # ------------------------------------------  NEEDS EDITIED FOR REAL DATA -----------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------

    # should be gfp and tdTomato channels

    # Path to cellfinder_output points.npy file
    tdTomato_cells_path = cellfinder_output_path + 'points/points.npy' # --> Update path to how cellfinder outputs different channel data 

    # Load in all registered cell coordinates, and Define the reference point as one of those coordinates
    cells = np.load(tdTomato_cells_path)

    # Create Overlapping cells for testing changing the color of the overlapping cells
    gfp_cells = cells[49000: 55000] # --> Change to path to gfp points.npy file from cellfinder output

    # malke random gfp cells to plot. this should be removed
    modified_gfp_cells = np.add(gfp_cells, 250)
 
    # Create an array that contains the shared voxel coordinates between the gfp and tdTomato channels
    shared_cells = [i for i in gfp_cells if i in cells]
    shared_cells = np.array(shared_cells)
    shared_cells_save_path = brainrender_folder_path + '/' + str(mouse_id) + '_' + str(estim_tip_coordinates) + '/shared_cells_' + mouse_id + '_' +str(estim_tip_coordinates) +  ".npy" 
    np.save(shared_cells_save_path , shared_cells)
    shared_cell_distance_calculations_histograms(brainrender_folder_path,mouse_id,estim_tip_coordinates)


    # create points actors for brainrender to plot in the 3D render
    cells_actor = Points(cells)
    overlapping_cells_actor = Points(shared_cells,colors="blackboard",radius=22)
    modified_gfp_cells_actor = Points(modified_gfp_cells, colors = 'green')


    # ------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------------------



    estim_tip_sphere_actor = Sphere(estim_tip_coordinates,estim_tip_radius_um,"green",)
    estim_propigation_sphere_actor = Sphere(estim_tip_coordinates,estim_propigation_radius_um,"black",0.25)
    opticalfiber_propigation_sphere_actor = Sphere(opticalfiber_tip_coordinates,opticalfiber_propigation_radius_um,"blue",0.25)
    estim_tip_coordinates_array = np.array([estim_tip_coordinates])
    # cell_volume_in_propigation_sphere_actor = PointsDensity(data=estim_tip_coordinates_array,name='Electical Propigation Sphere',dims=(100, 100, 100),radius=1000,)


    # read in braingloab regions df, make lists of names and acryonms
    atlas = BrainGlobeAtlas("allen_mouse_50um")
    brain_regions_df = atlas.lookup_df.head(1000)

    brain_regions_acronym = brain_regions_df['acronym'].to_list()
    brain_regions_name = brain_regions_df['name'].to_list()

    BrainGlobeAtlas_dictionary = dict(
        zip(brain_regions_acronym, brain_regions_name))


    # File path to the saved json file
    file_path = cellfinder_output_path + mouseid + \
        "_Completed_Analysis/" + 'cellfinder_summary/'+ "gfp_brainregions_list.json"
    with open(file_path, 'r') as f:
        file_content = f.read()
        brain_regions_list = json.loads(file_content)

    count_file_path = cellfinder_output_path + mouseid + \
        "_Completed_Analysis/"+ 'cellfinder_summary/'+ "gfp_brainregions_count.json"
    with open(count_file_path, 'r') as f:
        file_content = f.read()
        brain_regions_count_list = json.loads(file_content)

    # create a dictonary and df of brainregion acryonm and name, from the BrainGlobeAtlas. Because this is what brain render uses 
    brain_regions_dictionary = dict(
        zip(brain_regions_list, brain_regions_count_list))
    brain_regions_df = pd.DataFrame.from_dict(
        brain_regions_dictionary, orient='index')
  
    evaluate = list(brain_regions_dictionary.items())[
        :brain_regions_to_evalutate]



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
    # if len(extra_brain_region_acryonm) >= 1:
    index = []
    for i in extra_brain_region_acryonm:
            index.append(brain_regions_acronym.index(i))
    
    extra_brain_region_names = []
    for i in index:
        extra_brain_region_names.append(brain_regions_name[i])
        
    else:
        print('No extra brain regions added')

    extra_brain_regions_dictionary = dict(
    zip(extra_brain_region_names, extra_brain_region_acryonm))
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
    if show_gfp_only == True:
        scene = Scene(atlas_name='allen_mouse_50um', title=mouseid + ' GFP cells only')
        print(scene.atlas.space)

    if show_tdTomato_only == True:
        scene = Scene(atlas_name='allen_mouse_50um', title=mouseid + ' tdTomato cells only')
        print(scene.atlas.space)

    if show_gfp_tdTomato_overlapping  == True:
        scene = Scene(atlas_name='allen_mouse_50um', title=mouseid + ' GFP, tdTomato, and Overlapping cells')
        print(scene.atlas.space)

    if overlapping_cells_only == True:
        scene = Scene(atlas_name='allen_mouse_50um', title=mouseid + ' Overlapping gfp/tdTomato cells')
        print(scene.atlas.space)


     # Iterate over elements in list1
    for element in evaluate_brain_regions:
        # Check if element exists in list2
        if element in extra_brain_region_names:
            # Remove element from list2
            extra_brain_region_names.remove(element)

     # Iterate over elements in list1
    for element in evaluate_brain_region_acronyms:
        # Check if element exists in list2
        if element in extra_brain_region_acryonm:
            # Remove element from list2
            extra_brain_region_acryonm.remove(element)
            print(str(element) + ' is already in the top ' + str(brain_regions_to_evalutate) + ' brain regions. Removing from extra brain regions')
 

    # add top brain regions and labels
    # colors = ["red", 'orange', "yellow", "green", "blue", "red", 'orange',
    #           "yellow", "green", "blue", "red", 'orange', "yellow", "green", "blue","red", 'orange', "yellow", "green", "blue", "red", 'orange',
    #           "yellow", "green", "blue", "red", 'orange', "yellow", "green", "blue"]
    for i in range(brain_regions_to_evalutate):
        evaluate_brain_region_acronyms[i] = scene.add_brain_region(
            str(evaluate_brain_region_acronyms[i]), alpha=0.2, color='blue')
    if show_lables == True:
        for i in range(brain_regions_to_evalutate):
            # print(evaluate_brain_region_acronyms[i])
            scene.add_label(evaluate_brain_region_acronyms[i], str(
                evaluate_brain_regions[i])+' '+ str(brain_regions_count_list[i]))
    
    # scene.add_label(cell_volume_in_propigation_sphere_actor, "Count Volume")

    # load in the dictonary that has all the brain regions and their call counts for this mouse
    all_brain_region_cell_count_path = cellfinder_output_path + \
        str(mouse_id) + "_Completed_Analysis/" + 'cellfinder_summary/'+ 'all_brainregion_cell_count_list.pkl'
    with open(all_brain_region_cell_count_path, 'rb') as f:
        loaded_cell_count_dict = pickle.load(f)



     # # Add extra brain regions. specified in the extra_brain_region_acryonm list found in UpdateME.py
    list_len = len(extra_brain_region_acryonm)
    extra_cell_count_list = []
    if len(extra_brain_region_acryonm) == 0:
        print("adding no extra brain region to this render. to see addition brain regions, add their acryonms to the extra_brain_regions array in UpdateME.py. A full list of brain regions and their associated acryonms is saved in this repository as acronym_brainregions.csv'")
    else:
        for i in range(list_len):
            extra_brain_region_acryonm[i] = scene.add_brain_region(
            str(extra_brain_region_acryonm[i]), alpha=0.2, color='yellow')
        if show_lables == True:
            for i in range(list_len):
                for key in loaded_cell_count_dict.keys():
                    value = loaded_cell_count_dict.get(str(extra_brain_region_names[i]))
                    if value is None:
                        extra_cell_count_list.append('n/a')
                        scene.add_label(extra_brain_region_acryonm[i], str(extra_brain_region_names[i])+ ' ' + '(Manually Added)')
                        continue
                    cell_count = loaded_cell_count_dict[str(extra_brain_region_names[i])]
                    extra_cell_count_list.append(cell_count)
                    scene.add_label(extra_brain_region_acryonm[i], str(extra_brain_region_names[i])+ ' ' + str(cell_count) +' '+ '(Manually Added)')
     


    extra_brain_regions_dictionary_with_cellcount = dict(
        zip(extra_brain_region_names, extra_cell_count_list))

    # create and add a cylinder actor to brain region with the most labled cells
    VISl5 = scene.add_brain_region(
    "VISl5",
    alpha=0.4,
    )


    visual_cylinder_actor = Cylinder(
        # have cylinder run from the referece point to the brains surface 
        VISl5,
        scene.root,  # the cylinder actor needs information about the root mesh
        "black",
        1,
        estim_shank_radius_um,
     )

    estim_cylinder_actor = Cylinder(
        # have cylinder run from the referece point to the brains surface 
        estim_tip_coordinates,
        scene.root,  # the cylinder actor needs information about the root mesh
        "black",
        1,
        estim_shank_radius_um,
     )

    # pos =  [opticalfiber_surface_coordinates,opticalfiber_tip_coordinates]
    # print(pos)
    opticalfiper_cylinder_actor = Cylinder(
        # have cylinder run from the referece point to the brains surface 
        opticalfiber_tip_coordinates,
        scene.root,  # the cylinder actor needs information about the root mesh
        'blue',
        1,
        opticalfiper_radius_um,
     )

    # Testing 
    # estim_cell_coordinates_array = np.array([estim_cell_coordinates])
    # cell_volume_in_propigation_sphere_actor = PointsDensity(data=estim_cell_coordinates_array,name='Electical Propigation Sphere',dims=(100, 100, 100),radius=1000,)


    # Add a sphere in the reference point location
    # scene.add_sphere(center = reference_point, radius = 25, color = 'red')

    # check if 3D render has been saved out
    # if not export the 3D render, which can be opened in a web viewer
    if save_render == True:
        if not os.path.exists(scene_export_path):
            print('Saving out brainrender scence, this may take a few minutes...')
            scene.export(scene_export_path)
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

    # # locally Render the 3D brain Scence
    # rendered_brainregions_dict = {**evaluate, **extra_brain_regions_dictionary_with_cellcount}
    # print(rendered_brainregions_dict)

    # updateME_save_path = cellfinder_output_path + str(mouse_id) + "_Completed_Analysis/brainrender_outputs" 
    # upddateME_df.to_csv(updateME_save_path, index=False)

    # print("The "+str(brain_regions_to_evalutate) +
    #       " brain regions your loading with labled cells count")
    # print(evaluate)
    # print(' ')
    # print("The "+str(len(extra_brain_region_acryonm)) +
    #       " extra brain regions your loading with their cell count")
    # print(extra_brain_regions_dictionary_with_cellcount)
    # scene.render()
    # print the content of the scence
    scene.content

    if brain_region_estim == False:
        # Add cells Actor to Scence
        if show_gfp_tdTomato_overlapping == True:
            scene.add(modified_gfp_cells_actor,overlapping_cells_actor,cells_actor, estim_tip_sphere_actor, estim_cylinder_actor,estim_propigation_sphere_actor,opticalfiper_cylinder_actor ,opticalfiber_propigation_sphere_actor)
            scene.render()

        if show_gfp_only == True:
            scene.add(modified_gfp_cells_actor, estim_tip_sphere_actor, estim_cylinder_actor,estim_propigation_sphere_actor,opticalfiper_cylinder_actor ,opticalfiber_propigation_sphere_actor)
            scene.render()

        if show_tdTomato_only == True:
            scene.add(cells_actor,estim_tip_sphere_actor, estim_cylinder_actor,estim_propigation_sphere_actor,opticalfiper_cylinder_actor ,opticalfiber_propigation_sphere_actor)
            scene.render()

        if overlapping_cells_only == True:
            scene.add(overlapping_cells_actor,estim_tip_sphere_actor, estim_cylinder_actor,estim_propigation_sphere_actor,opticalfiper_cylinder_actor ,opticalfiber_propigation_sphere_actor)
            scene.render()
       
    if brain_region_estim == True:
            # Add cells Actor to Scence
        if show_gfp_tdTomato_overlapping == True:
            scene.add(visual_cylinder_actor,modified_gfp_cells_actor,overlapping_cells_actor,cells_actor, estim_tip_sphere_actor,estim_propigation_sphere_actor,opticalfiper_cylinder_actor ,opticalfiber_propigation_sphere_actor)
            scene.render()

        if show_gfp_only == True:
            scene.add(visual_cylinder_actor,modified_gfp_cells_actor, estim_tip_sphere_actor,estim_propigation_sphere_actor,opticalfiper_cylinder_actor ,opticalfiber_propigation_sphere_actor)
            scene.render()

        if show_tdTomato_only == True:
            scene.add(visual_cylinder_actor,cells_actor,estim_tip_sphere_actor,estim_propigation_sphere_actor,opticalfiper_cylinder_actor ,opticalfiber_propigation_sphere_actor)
            scene.render()

        if overlapping_cells_only == True:
            scene.add(visual_cylinder_actor,overlapping_cells_actor,estim_tip_sphere_actor,estim_propigation_sphere_actor,opticalfiper_cylinder_actor ,opticalfiber_propigation_sphere_actor)
            scene.render()
