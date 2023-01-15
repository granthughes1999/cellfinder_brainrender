# Run this file inside an Anaconda env with brainrender installed 
# (brainrender) python path/to/run_to_create_3D_render.py

import variables
from variables import cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um
import brainrender_mac_combined
from brainrender_mac_combined import run_brainrender

run_brainrender(cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um)
