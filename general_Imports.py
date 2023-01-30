# General Imports
import numpy as np
import os
import pandas as pd
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pickle 
from scipy.spatial import distance
from rich import print
from myterial import orange
# brainrender files/function imports
import brainrender
from brainrender.scene import Scene
from brainrender.actors import Points
from brainrender.actors import PointsDensity
from brainrender.actor import Actor
from brainrender import settings
from brainrender import Scene
from brainrender.actors import Cylinder
brainrender.SHADER_STYLE = "cartoon"
# vedo imports
from vedo import Spheres, Sphere
from vedo import Points as vPoints
# bg_atlasapi imports
from bg_atlasapi.bg_atlas import BrainGlobeAtlas
import bg_space as bg
from bg_atlasapi import show_atlases
from bg_atlasapi.bg_atlas import BrainGlobeAtlas
# files and variables from this repo imports
import UpdateME
from UpdateME import cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um, estim_tip_coordinates, extra_brain_region_acryonm, estim_shank_radius_um, estim_tip_radius_um, estim_propigation_radius_um, opticalfiper_radius_um, opticalfiber_tip_coordinates,opticalfiber_propigation_radius_um, show_lables,save_render
import cellfinder_backend
from cellfinder_backend import analyze_data_cellfinder
from distance_calculations_and_histograms import distance_calculations_histograms
from vector_calculations import estim_cell_coordinates
from shared_cells_distance_calculations import shared_cell_distance_calculations_histograms
import UpdateME
from UpdateME import cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um,estim_shank_radius_um ,estim_tip_radius_um,estim_propigation_radius_um,show_gfp_tdTomato_overlapping, show_gfp_only,show_tdTomato_only,overlapping_cells_only
import brainrender_backend
from brainrender_backend import run_brainrender
