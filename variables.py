import analyze_cellfinder_data
from analyze_cellfinder_data import analyze_data_cellfinder

# Update these variables

# 1. ID of mouse (example: G25)
mouse_id = "test_003"

# 2. cellfinder_output_path, path to where you want the cellfinder output data to be saved to
# analysis from these files will be added to this output folder
# in a new folder titled --> str(mouse_id) + "_Completed_Analysis"
cellfinder_output_path = "/Users/grant/Desktop/mock_df/cellfinder_output/"

# 3. How many top brain regions to evaluate. (default is 5)
# This represents how many brain regions brainrender will populate when creating a 3D render.
# it uses the regions with the most labled cells first and works down the list.
brain_regions_to_evalutate = 5

# 4. path to local location of allen mouse brain atlas
# you will need a local version of an allen brain atlas.
allen_mouse_10um = '/Users/grant/brainglobe/allen_mouse_10um'

# 5. Your brainrender conda env name
brainrender_env_name = 'brainrender'


analyze_data_cellfinder(cellfinder_output_path, mouse_id)
