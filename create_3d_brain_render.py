# Run this file inside an Anaconda env with brainrender installed 
# (brainrender) python path/to/run_to_create_3D_render.py
import UpdateME
from UpdateME import cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um,estim_shank_radius_um ,estim_tip_radius_um,estim_propigation_radius_um
import brainrender_backend
from brainrender_backend import run_brainrender



run_brainrender(cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um,estim_shank_radius_um,estim_tip_radius_um,estim_propigation_radius_um)
