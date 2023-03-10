import json
import xml.etree.ElementTree as ET
import pickle
from scipy import stats
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def analyze_data_cellfinder(cellfinder_output_path, mouse_id):


    # Create new folder in your cellfinder output folder
    new_folder_path = cellfinder_output_path + \
        str(mouse_id) + "_Completed_Analysis"  # create the path for the new folder

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        print(' ')
        print('folder with output data has been created.')
        print(f'{new_folder_path}')
        print('')
        print('running cellfinder_backend.py analysis')
        
        output_folder_path = new_folder_path + '/' + 'cellfinder_summary'
        os.makedirs(output_folder_path)

        # ### Read in tdTomato & GFP output data from cellfinder

        # import cellfinder summary csv, containing cell counts and more
        # IMPORTANT
        # gfp_summary.csv & tdTomato_summary.csv do not exist as a natural ouput of cellfinder
        # the normal output is just summary.csv
        # there for these will need to be changed before really running (these were for testing only)
        gfp_df = pd.read_csv(cellfinder_output_path +
                             'analysis/' + 'gfp_summary.csv')
        tdTomato_df = pd.read_csv(cellfinder_output_path +
                                  'analysis/' + 'tdTomato_summary.csv')

        # output path for created csv
        output_path_csv = output_folder_path + '/' + mouse_id + '_labled_cells.csv'

        # # GFP Data

        # make list of each brain region with labeled cells
        all_gfp_brain_regions = gfp_df['structure_name'].to_list()
        # print("All Brain Regions: " + str(len(all_gfp_brain_regions)))

        # make a list of total cell count for each brain region labeled with GFP
        all_gfp_brain_regions_cell_count = gfp_df['total_cells'].to_list()
        # print("total cells: " + str(sum(all_gfp_brain_regions_cell_count)))

        # make dict of brain_regions & cell_count
        all_gfp_dictionary = dict(
            zip(all_gfp_brain_regions, all_gfp_brain_regions_cell_count))
        all_gfp_df = pd.DataFrame.from_dict(all_gfp_dictionary, orient='index')

         # File path to the desktop
        file_path_0 = output_folder_path + '/all_brainregion_cell_count_list.pkl'
        with open(file_path_0 , 'wb') as f:
            pickle.dump(all_gfp_dictionary, f)

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
        file_path = output_folder_path + '/gfp_brainregions_list.json'

        # Open a file
        with open(file_path, 'w') as f:
            # Save the list to the file
            json.dump(gfp_brain_regions, f)

        # File path to the desktop
        count_file_path = output_folder_path + '/gfp_brainregions_count.json'

        # Open a file
        with open(count_file_path, 'w') as f:
            # Save the list to the file
            json.dump(gfp_brain_regions_cell_count, f)

        #  tdTomato Data

        # make list of each brain region with labeled cells
        all_tdTomato_brain_regions = tdTomato_df['structure_name'].to_list()
        # print("All Brain Regions: " + str(len(all_tdTomato_brain_regions)))

        # make a list of total cell count for each brain region labeled with GFP
        all_tdTomato_brain_regions_cell_count = tdTomato_df['total_cells'].to_list(
        )
        # print("total cells: " + str(sum(all_tdTomato_brain_regions_cell_count)))

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
        summary_df.to_csv(output_folder_path + '/' + mouse_id + '_summary_df.csv')

        # making a df with percent of gfp cells labled compared to tdTomato
        percent_labled = []
        i = 0
        for count in all_tdTomato_brain_regions_cell_count:
            if count >= 1:
                percent_labled.append(
                    all_gfp_brain_regions_cell_count[i] / count * 100)
                i += 1
            else:
                percent_labled.append('0')
                i += 1
        # ## df for percentage of labled gfp cells vs tdTomato cells

        # create df with gfp and tdTomato cell counts, and percent labled
        all_gfp_df['tdTomato cell count'] = all_tdTomato_brain_regions_cell_count
        all_gfp_df['percent labled gfp/tdTomato'] = percent_labled

        # Add the header 'New Column Name' to column at index 0
        all_gfp_df.rename(
            columns={gfp_df_01.columns[0]: 'gfp cell count'}, inplace=True)

        # Find all brain regions with labeled gfp cells, make gfp_df
        # labled_cells_df = all_gfp_df[all_gfp_df['gfp cell count'] >= 1]
        labled_cells_df = all_gfp_df

        labled_cells_df
        print(labled_cells_df.head(3))
        print('')
        print(gfp_df.head(3))
        print('')
        print(tdTomato_df.head(3))

        # divide the values in each column of the gfp_df against the values of the tdTomato_df, and add a new column for that divided data to the labled cells df
        labled_cells_df = labled_cells_df.assign(percent_cell_count_left=gfp_df['left_cell_count']/tdTomato_df['left_cell_count']*100)
        labled_cells_df = labled_cells_df.assign(percent_cell_count_right=gfp_df['right_cell_count']/tdTomato_df['right_cell_count']*100)

        labled_cells_df = labled_cells_df.assign(percent_volume_per_mm3_left=gfp_df['right_volume_mm3']/tdTomato_df['right_volume_mm3']*100)
        labled_cells_df = labled_cells_df.assign(percent_percent_volume_per_mm3_right=gfp_df['left_volume_mm3']/tdTomato_df['left_volume_mm3']*100)

        labled_cells_df = labled_cells_df.assign(percent_cells_per_mm3_right=gfp_df['right_cells_per_mm3']/tdTomato_df['right_cells_per_mm3']*100)
        labled_cells_df = labled_cells_df.assign( percent_cells_per_mm3_left=gfp_df['left_cells_per_mm3']/tdTomato_df['left_cells_per_mm3']*100)

        labled_cells_df.to_csv(output_path_csv)

    else:
        print('path already exists, skipping analysis...')
        print(f'{new_folder_path}')
        print('')
        print('to re-run analysis chane mouseid in variables.py or delete previously created mouseid_completed_analysis folder')


