
# !! IMPORTANT !!
# in analyze_cellfinder_data.py
# on line 36-39
# gfp_summary.csv & tdTomato_summary.csv do not exist as a natural ouput of cellfinder
# the normal output is just summary.csv
# there for these will need to be changed before really running (these were for testing only)
# Update these variables

# 1. ID of mouse (example: G25)
mouse_id = "test_005"

# 2. cellfinder_output_path, path to where you want the cellfinder output data to be saved to
# analysis from these files will be added to this output folder
# in a new folder titled --> str(mouse_id) + "_Completed_Analysis"
# ADD '/' at the end of your output path example: "/Users/grant/Desktop/mock_cellfinder_output/"
cellfinder_output_path = "/Users/grant/Desktop/cellfinder_brainrender_output/cellfinder_output/"

# 3. Electrode tip Voxel coordinates. using Paxinos-Franklin coordinate system where 
# the x-coordinate corresponds to the medial-lateral axis, with positive values towards the right and negative values towards the left. 
# The y-coordinate corresponds to the dorsal-ventral axis, with positive values towards the dorsal side and negative values towards the ventral side. 
# The z-coordinate corresponds to the rostral-caudal axis, with positive values towards the rostral side and negative values towards the caudal side. 
# refrence_point = [8050., -100., 6150.] ----> [x-coordinate, y-coordinate, z-coordinate]
estim_tip_coordinates = [7700.,  100., 6500.]

# 3. How many top brain regions to evaluate. (default is 5)
# This represents how many brain regions brainrender will populate when creating a 3D render.
# it uses the regions with the most labled cells first and works down the list.
brain_regions_to_evalutate = 5

#  OPTIONAL

# 4. path to local location of allen mouse brain atlas
# you will need a local version of an allen brain atlas.
allen_mouse_10um = '/Users/grant/brainglobe/allen_mouse_10um'

# 5. Your brainrender conda env name
brainrender_env_name = 'brainrender'
