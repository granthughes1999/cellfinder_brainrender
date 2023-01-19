# Analyze and Visualize Electrical Brain Stimuluation Data 
This repository is designed to work with light-sheet images. 
Specifaclly GFP-labled-cells as a result of DBS prefromed on Cal-light mice, and tdTomato-labled-cells used as a control.
Note you may need to retrain the cellfinder network before procceding to the analysis.
You can/should verify correct cell labling using napari .
Please check out my napari repository for how to accomplish network retraining.

All the output data from this repository will be saved in a folder titled mouseid_completed_analysis. This folder can be found inside the cellfinder output folder that cellfinder created when you ran it (this will be the file path you used in updateME.py).

# Before you can run these files 
### Create Two Anaconda environments 
### 1. cellfinder env
##### conda create -n cellfinder python=3.9
##### pip install cellfinder

### 2. brainrender env
##### conda create -n brainrender python=3.9
##### pip install brainrender
##### pip install "numpy<1.24"

# Step 1 
#### Clone this repository 

# Step 2
## updating the information that cellfinder will use to analyze your light-sheet images
##### follow the instructions for updating the variables here https://docs.brainglobe.info/cellfinder/user-guide/command-line
##### use this link to understand voxel & orentation variables https://docs.brainglobe.info/cellfinder/image-orientation
### open run_cellfinder.bat
##### update the variables 6 variables, and add extra signal channels if needed
##### line 6: cellfinder -s, -b, -o, --orentation, -v, --atlas allen_mouse_50um

# Step 3 
## Running cellfinder
#### open a Anaconda prompt
#### activate your cellfinder env
#### for the Denman Lab Neuropixel Aquisition Computer use "conda activate cellfinder2"
#### drop in run_cellfinder.bat
#### (cellfinder2) >> path/to/run_cellfinder.bat
#### click enter
#### this step may take 2-8 hours to complete per brain

# Step 4
## Verify correct cell labling using napari 
#### please reference my napari repository for these steps 

# Step 5
## Updating UpdateME.py
##### Update all the varibales in this folder

## Step 6
#### conda activate brainrender
#### >> python /path/to/create_3d_render.py

# Step 7
## Updating UpdateME.py
##### Update all the varibales in this folder

# Step 8
#### conda activate brainrender
#### >> python /path/to/create_3d_render.py
