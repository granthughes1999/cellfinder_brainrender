import tkinter as tk
from tkinter import *
import subprocess
global show_lables
from general_Imports import *
from tkinter import ttk

#  ---- Basics of GUI -----
root = tk.Tk()
root.configure(bg='gray')
root.geometry("1000x300")

# Create a Notebook widget as the top-level container
notebook = ttk.Notebook()
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)


notebook.add(tab1, text='Imports')
notebook.add(tab2, text='Estim')
notebook.add(tab3, text='Brain Regions')
# ----- Functions -----

# Update the  
def on_checkbutton_click():
    global show_lables
    if checkbutton_var.get() == 1:
        show_lables = True
        print(show_lables)
    else:
        show_lables = False
        print(show_lables)

checkbutton_var = tk.IntVar()
checkbutton = tk.Checkbutton(tab3, text="Show Labels", variable=checkbutton_var, command=on_checkbutton_click)

# Creates the 3D render when the button is clicked 
def on_button_click():
   
    cellfinder_output_path = cellfinder_output_path_entry.get()
    mouse_id  = mouse_id_entry.get()
    brain_regions_to_evalutate = int(brain_regions_to_evalutate_entry.get())
    allen_mouse_10um = allen_mouse_10um_entry.get()
    estim_shank_radius_um = int(estim_shank_radius_um_entry.get())
    estim_tip_radius_um = int(estim_tip_radius_um_entry.get())
    estim_propigation_radius_um = int(estim_propigation_radius_um_entry.get())
    extra_brain_region_acryonm = extra_brain_region_acryonm_entry.get()
    list_of_strings =  extra_brain_region_acryonm.split(', ')
    stripped_string_list = [i.strip() for i in list_of_strings]
    extra_brain_region_acryonm = stripped_string_list
    if extra_brain_region_acryonm == ['']:
        extra_brain_region_acryonm = []
    # Get the value of the Entry widget
    run_brainrender(cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um,estim_shank_radius_um,estim_tip_radius_um,estim_propigation_radius_um,extra_brain_region_acryonm,show_lables)
    print("Button was clicked!")
   

# --------- Variables --------

# /Users/grant/Desktop/work/Denman_Lab/Cal_Light/brainrender/cellfinder_brainrender_output/cellfinder_output/

# ------- Entry windows on GUI for each Variable needed --------
# path to cellfinder output data, also where all data will be stored from these files
cellfinder_output_path = tk.StringVar()
cellfinder_output_path_entry = tk.Entry(tab1, textvariable=cellfinder_output_path, width=110)
cellfinder_output_path_entry.insert(0, '/Users/grant/Desktop/work/Denman_Lab/Cal_Light/brainrender/cellfinder_brainrender_output/cellfinder_output/')
label_cellfinder_output_path = tk.Label(tab1, text="Enter path to cellfinder output data ")
# cellfinder_output_path_entry.pack()
# mouse id used, (ie. G19, G18...)
mouse_id = tk.StringVar()
mouse_id_entry = tk.Entry(root, textvariable=mouse_id, width=20)
label_mouse_id = tk.Label(root, text="Enter Mouse ID ")


# number of top brain regions you want to be seen in the render. (top meaning containing the most labled cells)
brain_regions_to_evalutate = tk.IntVar()
brain_regions_to_evalutate_entry = tk.Entry(tab3, textvariable=brain_regions_to_evalutate, width=20)
label_brain_regions_to_evalutate = tk.Label(tab3, text="Enter number of top labled brain regions you want to render ")

# brain_regions_to_evalutate_entry.pack()
# Path to the local allen brain atlas directory you want to use
allen_mouse_10um = tk.StringVar()
allen_mouse_10um_entry = tk.Entry(tab1, textvariable=allen_mouse_10um, width=50)
allen_mouse_10um_entry.insert(0, '/Users/grant/brainglobe/allen_mouse_10um')
label_allen_mouse_10um = tk.Label(tab1, text="Enter path to you local allen brain atlas ")

estim_shank_radius_um = tk.IntVar()
estim_shank_radius_um_entry = tk.Entry(tab2, textvariable=estim_shank_radius_um, width=20)
estim_shank_radius_um_entry.insert(tk.END, str(50))
label_estim_shank_radius_um = tk.Label(tab2, text="Enter estim shank radius in (um) ")


estim_tip_radius_um = tk.IntVar()
estim_tip_radius_um_entry = tk.Entry(tab2, textvariable=estim_tip_radius_um, width=20)
estim_tip_radius_um_entry.insert(tk.END, str(10))
label_estim_tip_radius_um  = tk.Label(tab2, text="Enter estim tip radius in (um)")



estim_propigation_radius_um = tk.IntVar()
estim_propigation_radius_um_entry = tk.Entry(tab2, textvariable=estim_propigation_radius_um, width=20)
estim_propigation_radius_um_entry.insert(tk.END, str(300))
label_estim_propigation_radius_um = tk.Label(tab2, text="Enter estim propigation radius in (um)")


extra_brain_region_acryonm = tk.StringVar()
extra_brain_region_acryonm_entry = tk.Entry(tab3, textvariable=extra_brain_region_acryonm, width=100)
extra_brain_region_acryonm_entry.insert(tk.END, str('VIS, ECT, VISp1, VISp2/3, VISp4, VISp5,  VISp6a, VISp6b'))
label_extra_brain_region_acryonm = tk.Label(tab3, text="Enter list of brain region acryonms you want to render ")




# ---- Buttons -----
run_button = tk.Button(root, text="Create 3D Render", command=on_button_click)
run_button.grid(row=5, column=0)

# grid for the gui
label_cellfinder_output_path.grid(row=1, column=2)
cellfinder_output_path_entry.grid(row=2, column=2)

label_mouse_id.grid(row=2, column=0)
mouse_id_entry.grid(row=3,column=0)

label_brain_regions_to_evalutate.grid(row=5, column=2)
brain_regions_to_evalutate_entry.grid(row=6,column=2)

label_allen_mouse_10um.grid(row=7, column=2)
allen_mouse_10um_entry.grid(row=8,column=2)

label_estim_shank_radius_um.grid(row=9, column=2)
estim_shank_radius_um_entry.grid(row=10,column=2)

label_estim_tip_radius_um.grid(row=11, column=2)
estim_tip_radius_um_entry.grid(row=12,column=2)

label_estim_propigation_radius_um.grid(row=13, column=2)
estim_propigation_radius_um_entry.grid(row=14,column=2)

label_extra_brain_region_acryonm.grid(row=15, column=2)
extra_brain_region_acryonm_entry.grid(row=16, column=2) 


checkbutton.grid(row=17, column=2)
notebook.grid(row=0, column=0)


checkbutton.bind('<Button-1>', on_checkbutton_click)
run_button.bind('<Button-1>', on_button_click)




# ---- crerate GUI ------
root.mainloop()
