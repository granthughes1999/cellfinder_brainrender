# cellfinder_brainrender
this combines cellfinder and brainrender into one repository for simplicity 

## Step 1
#### Clone repository 

## Step 2
#### open run_cellfinder.bat
#### follow the instructions for updating the variables here https://docs.brainglobe.info/cellfinder/user-guide/command-line
#### use this link to understand voxel & orentation variables https://docs.brainglobe.info/cellfinder/image-orientation
### update the variables in final line 6
##### -s, -b, -o, --orentation, -v, --atlas allen_mouse_50um

## Step 3
#### open anaconda prompt
#### drop in run_cellfinder.bat
#### click enter

## Step 4
#### open >> variables.py
##### update all the varibales

## Step 5
#### run >> working_with_cellfinder_data_combined.py

## step 6 (skip if you already have a brainrender env)
#### create brainrender anaconda env
##### open terminal 
##### conda create -n brainrender python=3.9
##### conda activate brainrender
##### pip install brainrender
##### pip install numpy<1.22

## Step 7
#### conda activate brainrender
#### >> python /path/to/brainrender_mac.py
