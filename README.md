# cellfinder_brainrender
this repository is designed to work with light-sheet images, obtained from DBS prefromed on Cal-light mice.
Note you may need to retrain the cellfinder network before procceding to the analysis, you can/should verify correct cell labling using napari
if the labled cells and non-labled cells appear incorrectly labled, please check out my napari repository 


# Step 1
#### Clone repository 

# Step 2
## updating the information that cellfinder will use to analyze your light-sheet images
##### follow the instructions for updating the variables here https://docs.brainglobe.info/cellfinder/user-guide/command-line
##### use this link to understand voxel & orentation variables https://docs.brainglobe.info/cellfinder/image-orientation
### open run_cellfinder.bat
##### update the variables 6 variables, and add extra signal channels if needed
##### line 6: cellfinder -s, -b, -o, --orentation, -v, --atlas allen_mouse_50um

# Step 3 (skip this step if you have already run cellfinder on your light-sheet images)
## Running cellfinder
#### open a Anaconda prompt
#### activate your cellfinder env
#### for the Denman Lab Neuropixel Aquisition Computer use "conda activate cellfinder2"
#### drop in run_cellfinder.bat
#### (cellfinder2) >> path/to/run_cellfinder.bat
#### click enter

# Step 4
## Updating the information needed to execute these files 
### variables.py
##### Update all the varibales in this folder
### run this file
#### If the file does not run 
##### 1. Check that the folder mouseid_completed_analysis does not already exist in the cellfinder_output folder
##### if it does you can either delete this folder and run the variables file again 
##### 2. change your mouseid and run the variables file again

## step 5 (skip if you already have a brainrender env)
#### create brainrender anaconda env
##### open terminal 
##### >> conda create -n brainrender python=3.9
##### >> conda activate brainrender
##### >> pip install brainrender
##### >> pip install numpy<1.22

## Step 6
#### conda activate brainrender
#### >> python /path/to/brainrender_mac.py
