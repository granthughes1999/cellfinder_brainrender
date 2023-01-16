# cellfinder_brainrender
This repository is designed to work with light-sheet images. 
Specifaclly GFP-labled-cells as a result of DBS prefromed on Cal-light mice, and tdTomato-labled-cells used as a control.
Note you may need to retrain the cellfinder network before procceding to the analysis.
You can/should verify correct cell labling using napari .
Please check out my napari repository for how to accomplish network retraining.

All the output data from these files, will be saved to a folder titled mouseid_completed_analysis. This folder can be found inside the cellfinder_output folder that cellfinder created when you ran it (this will be the file path you used in the varibles file of this repositry).


# Step 1
#### Clone this repository 

# Step 2
create two Anaconda environments 
1. cellfinder (pip install cellfinder)
##### conda create -n cellfinder python=3.9
##### pip install cellfinder
2. brainrender env
##### conda create -n brainrender python=3.9
##### pip install brainrender
##### pip install "numpy<1.24"



# Step 2 (skip this step if you already have cellfinder output data, and just want to analyze the data & create a 3D render)
## updating the information that cellfinder will use to analyze your light-sheet images
##### follow the instructions for updating the variables here https://docs.brainglobe.info/cellfinder/user-guide/command-line
##### use this link to understand voxel & orentation variables https://docs.brainglobe.info/cellfinder/image-orientation
### open run_cellfinder.bat
##### update the variables 6 variables, and add extra signal channels if needed
##### line 6: cellfinder -s, -b, -o, --orentation, -v, --atlas allen_mouse_50um


# Step 3 (skip this step if you have already run cellfinder on your light-sheet images, and have verfied correct cell labling using napari)
## Running cellfinder
#### open a Anaconda prompt
#### activate your cellfinder env
#### for the Denman Lab Neuropixel Aquisition Computer use "conda activate cellfinder2"
#### drop in run_cellfinder.bat
#### (cellfinder2) >> path/to/run_cellfinder.bat
#### click enter
#### this step may take 2-8 hours to complete
## Verify correct cell labling using napari 
#### please reference my napari repository for these steps 


# Step 4
## Updating the information needed to execute these files 
### variables.py
##### Update all the varibales in this folder
### run this file
#### If the file does not run 
##### 1. Check that the folder mouseid_completed_analysis does not already exist in the cellfinder_output folder
##### if it does you can either delete this folder and run the variables file again 
##### 2. change your mouseid and run the variables file again


## Step 5
#### conda activate brainrender
#### >> python /path/to/brainrender_mac.py
