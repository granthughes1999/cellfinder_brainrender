1#!/usr/bin/env python
# coding: utf-8

# In[109]:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import os
from scipy import stats
import pickle
import xml.etree.ElementTree as ET
import json


def analyze_data_cellfinder(cellfinder_output_path, mouse_id):

    # Create new folder in your cellfinder output folder
    new_folder_path = cellfinder_output_path + \
        str(mouse_id) + "_Completed_Analysis"  # create the path for the new folder

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print('folder has been created.')
        print(f'{new_folder_path}')
        print('')
        print('running analysis')

        # ### Read in tdTomato & GFP output data from cellfinder

        # import cellfinder summary csv, containing cell counts and more
        # IMPORTANT
        # gfp_summary.csv & tdTomato_summary.csv do not exist as a natural ouput of cellfinder
        # the normal output is just summary.csv
        # there for these will need to be changed before really running (these were for testing only)
        gfp_df = pd.read_csv(cellfinder_output_path +
                             'analysis/' + 'summary.csv')
        tdTomato_df = pd.read_csv(cellfinder_output_path +
                                  'analysis/' + 'tdTomato_summary.csv')

        # output path for created csv
        output_path_csv = new_folder_path + '/' + mouse_id + '_labled_cells.csv'

        # # GFP Data

        # make list of each brain region with labeled cells
        all_gfp_brain_regions = gfp_df['structure_name'].to_list()
        print("All Brain Regions: " + str(len(all_gfp_brain_regions)))

        # make a list of total cell count for each brain region labeled with GFP
        all_gfp_brain_regions_cell_count = gfp_df['total_cells'].to_list()
        print("total cells: " + str(sum(all_gfp_brain_regions_cell_count)))

        # make dict of brain_regions & cell_count
        all_gfp_dictionary = dict(
            zip(all_gfp_brain_regions, all_gfp_brain_regions_cell_count))
        all_gfp_df = pd.DataFrame.from_dict(all_gfp_dictionary, orient='index')

        # Find all brain regions with labeled gfp cells, make gfp_df
        gfp_cells_df = gfp_df[gfp_df['total_cells'] >= 1]

        # make list of each brain region with labeled cells
        gfp_brain_regions = gfp_cells_df['structure_name'].to_list()
        gfp_brain_regions_sum = len(gfp_brain_regions)
        print("GFP Brain Regions With labeled Cells: " +
              str(gfp_brain_regions_sum))

        # make a list of total cell count for each brain region labeled with GFP
        gfp_brain_regions_cell_count = gfp_cells_df['total_cells'].to_list()
        gfp_labled_cells_sum = sum(gfp_brain_regions_cell_count)
        print("total labeled GFP cells: " + str(gfp_labled_cells_sum))

        # make dict of brain_regions & cell_count
        gfp_dictionary = dict(
            zip(gfp_brain_regions, gfp_brain_regions_cell_count))
        gfp_df_01 = pd.DataFrame.from_dict(gfp_dictionary, orient='index')

        # File path to the desktop
        file_path = new_folder_path + '/gfp_brainregions_list.json'
        print(file_path)

        # Open a file
        with open(file_path, 'w') as f:
            # Save the list to the file
            json.dump(gfp_brain_regions, f)

        # File path to the desktop
        count_file_path = new_folder_path + '/gfp_brainregions_count.json'
        print(count_file_path)

        # Open a file
        with open(count_file_path, 'w') as f:
            # Save the list to the file
            json.dump(gfp_brain_regions_cell_count, f)

        #  tdTomato Data

        # make list of each brain region with labeled cells
        all_tdTomato_brain_regions = tdTomato_df['structure_name'].to_list()
        print("All Brain Regions: " + str(len(all_tdTomato_brain_regions)))

        # make a list of total cell count for each brain region labeled with GFP
        all_tdTomato_brain_regions_cell_count = tdTomato_df['total_cells'].to_list(
        )
        print("total cells: " + str(sum(all_tdTomato_brain_regions_cell_count)))

        # make dict of brain_regions & cell_count
        all_tdTomato_dictionary = dict(
            zip(all_tdTomato_brain_regions, all_tdTomato_brain_regions_cell_count))
        all_tdTomato_df = pd.DataFrame.from_dict(
            all_tdTomato_dictionary, orient='index')

        # create a dictonary of only the
        # Find all brain regions with labeled gfp cells, make gfp_df
        tdTomato_cells_df = tdTomato_df[tdTomato_df['total_cells'] >= 1]

        # make list of each brain region with labeled cells
        tdTomato_brain_regions = tdTomato_cells_df['structure_name'].to_list()
        tdTomato_brain_regions_sum = len(tdTomato_brain_regions)
        print("tdTomato Brain Regions With labeled Cells: " +
              str(tdTomato_brain_regions_sum))

        # make a list of total cell count for each brain region labeled with GFP
        tdTomato_brain_regions_cell_count = tdTomato_cells_df['total_cells'].to_list(
        )
        tdTomato_labled_cells_sum = sum(tdTomato_brain_regions_cell_count)
        print("total labeled tdTomato cells: " +
              str(tdTomato_labled_cells_sum))

        # make dict of brain_regions & cell_count
        tdTomato_dictionary = dict(
            zip(tdTomato_brain_regions, tdTomato_brain_regions_cell_count))
        tdTomato_df_01 = pd.DataFrame.from_dict(
            tdTomato_dictionary, orient='index')

        # ## Create csv file with summary of gfp and tdTomato Cellcount and Brain Regions

        data = {'total whole-brain cell count': [gfp_labled_cells_sum, tdTomato_labled_cells_sum],
                'total brain regions': [gfp_brain_regions_sum, tdTomato_brain_regions_sum],
                'brain regions list': [gfp_brain_regions, all_tdTomato_brain_regions]}

        summary_df = pd.DataFrame(data)
        summary_df.rename(index={0: 'GFP'}, inplace=True)
        summary_df.rename(index={1: 'tdTomato'}, inplace=True)

        # Save out summary df
        summary_df.to_csv(new_folder_path + '/' + mouse_id + '_summary_df.csv')

        # making a df with percent of gfp cells labled compared to tdTomato
        percent_labled = []
        i = 0
        for count in all_tdTomato_brain_regions_cell_count:
            percent_labled.append(
                all_gfp_brain_regions_cell_count[i] / count * 100)
            i += 1

        # ## df for percentage of labled gfp cells vs tdTomato cells

        # create df with gfp and tdTomato cell counts, and percent labled
        all_gfp_df['tdTomato cell count'] = all_tdTomato_brain_regions_cell_count
        all_gfp_df['percent labled gfp/tdTomato'] = percent_labled

        # Add the header 'New Column Name' to column at index 0
        all_gfp_df.rename(
            columns={gfp_df_01.columns[0]: 'gfp cell count'}, inplace=True)

        # Find all brain regions with labeled gfp cells, make gfp_df
        labled_cells_df = all_gfp_df[all_gfp_df['gfp cell count'] >= 1]
        labled_cells_df

        labled_cells_df.to_csv(output_path_csv)

    else:
        print('path already exists, skipping analysis...')
        print(f'{new_folder_path}')
        print('')
        print('to re-run analysis chane mouseid in variables.py or delete previously created mouseid_completed_analysis folder')


# >>>> EXTRA CODE, NOT CURRENTLY USED
# # There are several ways to statistically compare the values at each index location of two lists in Python. Here are a few options:
# ### 1. Using the scipy library's stats.ttest_ind() function, you can perform a t-test to compare the means of the two lists at each index location. For example:

# t, p = stats.ttest_ind(gfp_brain_regions_cell_count, mock_tdTomato_cellcount)

# ### 2. Using the numpy library's corrcoef() function, you can calculate the correlation coefficient between the two lists at each index location. For example:

# corr = np.corrcoef(gfp_brain_regions_cell_count, mock_tdTomato_cellcount)[0, 1]

# # ### 3.  Using the pandas library, you can create a dataframe from the two lists and use the corr() function to calculate the correlation between the two lists:

# df = pd.DataFrame({'list1': gfp_brain_regions_cell_count, 'list2': mock_tdTomato_cellcount})
# corr = df['list1'].corr(df['list2'])

# # # load voxel locations of cells

# # In[81]:

# data = np.load("/Users/grant/Desktop/mock_df/points.npy")

# # # Load cell_classification data

# tree = ET.parse("/Users/grant/Desktop/mock_df/cell_classification.xml")
# root = tree.getroot()

# # Iterate over child elements
# for child in root:
#     print(child.tag, child.attrib)


# # # load all point
# all_points = pd.read_csv("/Users/grant/Desktop/mock_df/all_points.csv")

# # # load volumes
# volumes = pd.read_csv("/Users/grant/Desktop/mock_df/volumes.csv")
