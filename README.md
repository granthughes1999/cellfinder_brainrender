# Analyze and Visualize Electrical Brain Stimuluation Data 
This repository is designed to work with light-sheet images. 
Specifaclly GFP-labled-cells as a result of DBS prefromed on Cal-light mice, and tdTomato-labled-cells used as a control.
Note you may/likely need to retrain the cellfinder cell_classification network before procceding to Step 5.
Please check out my napari repository for how to accomplish network retraining.

All the output data from this repository will be saved in a folder titled mouse_id_Completed_Analysis. This folder will be added to the cellfinder output folder that cellfinder created when you ran it (this should be the file path you use for cellfinder_output_path variable in updateME.py).

# Before you can run these files 
### Create This Anaconda environment

### 2. brainrender env
##### conda create -n brainrender python=3.9
##### pip install brainrender
##### pip install "numpy<1.24"

# Step 1 
#### Clone this repository 

# Step 2
#### activate brainrender env
### type the following
#### (brainrender) python path/to/GUI.py
#### you can drag and drop GUI.py behind the word python
#### click enter 

# Step 3
## on the imports tab of the GUI 
#### browse your computer and select the cellfinder output director 

# Step 4
## Add a mouse ID

# Step 5
## Update any features you want in the GUI

# Step 6
## Click Create 3D Render 







# OLD STEPS 
## Create cellfinder Anaconda ENV
### 1. cellfinder env
##### conda create -n cellfinder python=3.9
##### pip install cellfinder

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

# Step 6
#### activate your brainrender env
#### >> python /path/to/create_3d_brain_render.py
