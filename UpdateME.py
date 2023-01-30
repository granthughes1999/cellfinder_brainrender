

# ____________________________________________ IMPORTANT ______________________________________________

# in analyze_cellfinder_data.py, on line 36-39
# gfp_summary.csv & tdTomato_summary.csv do not exist as natural ouputs of cellfinder. The normal output is just summary.csv
# therefore, you will need to take the summary.csv from the gfp and tdTomato channels and rename them gfp_summary.csv and tdTomato_summary.csv
# then place them both into the cellfinder_output/analysis folder created for the gfp channel 


# _____________________________________________ please note ____________________________________________

# 1. if you do not change mouse_id or estim_tip_coordinates 
#    no new data will be created when running create_3d_brain_render.py, but you will still be able to create a local 3d-render.
# 2. if you keep mouse_id the same, but change the estim_tip_coordinates 
#    re-running create_3d_brain_render.py, will create a new folder, and add in a new 3d-render.html and new 3d-distance-histograms will be created relative to those coordinates.


# ___________________________________________ Update these variables ___________________________________

#
save_render = True
show_gfp_tdTomato_overlapping = False
show_gfp_only = False
show_tdTomato_only = False
overlapping_cells_only = False


# 1. ID of mouse (example: G25)
mouse_id = "test_002"

# 2. path to the cellfinder gfp signal channel output folder 
# this is where all the data from this repository will be saved to, in a folder called mouse_id_Completed_Anaylysis
# analysis from these files will be added to this output folder
# in a new folder titled --> str(mouse_id) + "_Completed_Analysis"
# ADD '/' at the end of your output path example: "/Users/grant/Desktop/mock_cellfinder_output/"
cellfinder_output_path = "/Users/grant/Desktop/work/Denman_Lab/Cal_Light/brainrender/cellfinder_brainrender_output/cellfinder_output/"


# 3. Electrode tip Voxel coordinates. using Paxinos-Franklin coordinate system where:
# the x-coordinate corresponds to the medial-lateral axis, with positive values towards the right and negative values towards the left. 
# The y-coordinate corresponds to the dorsal-ventral axis, with positive values towards the dorsal side and negative values towards the ventral side. 
# The z-coordinate corresponds to the rostral-caudal axis, with positive values towards the rostral side and negative values towards the caudal side. 
# estim_tip_coordinates = [8050., -100., 6150.] ----> [x-coordinate, y-coordinate, z-coordinate]
# this coordinate will create the tip of your electrode (shown as a green sphere), and a yellow cylinder spanning from that point to the brain surface will be added to your 3d-render 
# by changing these coordinates you can re-run create_3d_brain_render.py, and a new 3d-redner with this electrode cylinder and histograms will be created 
#  Some examples to try
# [7750.  300. 7550.] [8400.  450. 4500.] [8900. 1000. 4050.] [4750. 4900. 1900.] [9450. 6050. 2150.] [8550. 6700. 1700.] [7650. 7300. 2550.] [4600. 7150. 8250.] [4500. 7450. 7550.]
# Good example: [4750., 4900., 1900.] (middle of brain)
# [rostral-caudal, z-dpeth, medial-lateral ]
 #[higher# = back of brain, higher# = deeper, higher# = right hemi]
estim_tip_coordinates = [5300., 5350., 3300.]  

opticalfiber_tip_coordinates = [5450., 5500., 3450.] 

opticalfiber_propigation_radius_um = 200
estim_shank_radius_um = 50
estim_tip_radius_um = 50
estim_propigation_radius_um = 300
opticalfiper_radius_um = 10

# 4. How many top brain regions to evaluate. (default is 5)
# This represents how many brain regions brainrender will populate when creating a 3D render.
# it uses the regions with the most labled cells first and works down the list.
# if it fails to render, it may be because there is not enough colors in the color array on line 176 of brainrender_backend.py
# you can add more colors to that list if you would like 
# you can also change the colors in this list. i have the same 5 repreating, but there are more options
brain_regions_to_evalutate = 6

# True will show brain region lables and their cell count in the 3D render
# False will not show the brain region lables in the 3D render
show_lables = True 

# 5. What extra brain regions you to have render
# use the acronym of the brain region you want to load. 
# the acronym_brainregions.csv file in this repoistory  will show you what acronym aligns with what brain regions
# example:  brain_regions = ["CH", "CTX", ...]
# VISp1 = Primary Visual Areas layer 1
# VISp2/3 = Primary Visual Areas layer 2/3
# all these brain regions currently load in pink
# Some brain regions are not apart of brainrender, please double check
extra_brain_region_acryonm = ['VIS','ECT','VISp1','VISp2/3','VISp4','VISp5','VISp6a','VISp6b']

#  _______________ OPTIONAL _____________

# 4. path to local location of allen mouse brain atlas
# you can check which allen atlas you have stored locally by running the allen_atlas_verification.py file
allen_mouse_10um = '/Users/grant/brainglobe/allen_mouse_10um'

