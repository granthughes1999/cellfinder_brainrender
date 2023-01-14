# cellfinder_brainrender
this combines cellfinder and brainrender into one repository for simplicity 

### Step 1
#### Clone repository 

### Step 2
#### in working_with_cellfinder_data_combined.py, edit the following 2 variables
##### 1. mouse_id = "test_001"
##### 2. cellfinder_output_path = "/Users/grant/Desktop/mock_df/cellfinder_output/"

### Step 3
#### Run this file

### Step 4
#### open brainrender_mac_combined.py

### step 5 (optional)
#### in brainrender_mac_combined.py, edit two variables
##### 1. How many top brain regions to evaluate. (default is 5)
###### brain_regions_to_evalutate = 5
##### 2. path to local location of allen mouse brain atlas
###### allen_mouse_10um = '/Users/grant/brainglobe/allen_mouse_10um'

### step 6 (skip if you already have a brainrender env)
#### create brainrender anaconda env
##### open terminal 
##### conda create -n brainrender python=3.9
##### conda activate brainrender
##### pip install brainrender
