import tkinter as tk
from tkinter import *
import subprocess
global show_lables
global estim_tip_coordinates
global save_render
global show_gfp_only
global show_tdTomato_only
global overlapping_cells_only
global show_gfp_tdTomato_overlapping
global brain_region_estim
from general_Imports import *
from tkinter import ttk
import tkinter.filedialog as filedialog
from PIL import Image
from PIL import ImageTk




#  ---- Basics of GUI -----
root = tk.Tk()
root.configure(bg='gray')
root.geometry("1000x1000")

# Create a Notebook widget as the top-level container
notebook = ttk.Notebook()
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab5 = ttk.Frame(notebook)



notebook.add(tab1, text='Imports')
notebook.add(tab2, text='Estim')
notebook.add(tab3, text='Channels')
notebook.add(tab4, text='Brain Regions')
notebook.add(tab5, text='Histogram Viewer')



# ---------- TESTING histogram viewing window ---------------------------------------------
# Create a new tab

# Create a label to display the images
image_label = tk.Label(tab5)
image_label.grid(row=0, column=0, columnspan=5)

# Create a variable to store the path to the directory of images
image_directory = tk.StringVar()

# Create a button to open a file explorer to select the image directory
def browse_image_directory():
    directory = filedialog.askdirectory()
    image_directory.set(directory)

browse_image_directory_button = tk.Button(tab5, text="Browse for histogram image directory", command=browse_image_directory)
browse_image_directory_button.grid(row=1, column=0)

# Create an entry to display the selected image directory
image_directory_entry = tk.Entry(tab5, textvariable=image_directory)
image_directory_entry.grid(row=1, column=1,columnspan=5)

# Create a list of images
images = []

# Create a function to load the images from the selected directory
def load_images():
    directory = image_directory.get()
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            image = Image.open(image_path)
            images.append(image)

# Create a button to load the images
load_images_button = tk.Button(tab5, text="Load Images", command=load_images)
load_images_button.grid(row=2, column=0, columnspan=2)

# Create a variable to store the current image index
current_image_index = 0

# Create a function to display the current image
def show_current_image():
    global current_image_index
    image = images[current_image_index]
    image = ImageTk.PhotoImage(image)
    image_label.config(image=image)
    image_label.image = image

# Create a button to show the previous image
def show_previous_image():
    global current_image_index
    current_image_index = (current_image_index - 1) % len(images)
    show_current_image()

previous_image_button = tk.Button(tab5, text="<", command=show_previous_image)
previous_image_button.grid(row=3, column=0)

# Create a button to show the next image
def show_next_image():
    global current_image_index
    current_image_index = (current_image_index + 1) % len(images)
    show_current_image()

next_image_button = tk.Button(tab5, text=">", command=show_next_image)
next_image_button.grid(row=3, column=1)

# ---------- END OF TESTING histogram viewing window ---------------------------------------------



# Create a variable to store the path to the directory of images
cellfinder_output_path_01 = tk.StringVar()

# Create a button to open a file explorer to select the image directory
def browse_image_directory():
    directory = filedialog.askdirectory()
    directory = directory + "/"
    cellfinder_output_path_01.set(directory)

browse_image_directory_button_01 = tk.Button(tab1, text="Browse for cellfinder output directory", command=browse_image_directory)

# Create an entry to display the selected image directory
cellfinder_output_path_01_entry = tk.Entry(tab1, textvariable=cellfinder_output_path_01)
# cellfinder_output_path_01_entry.grid(row=1, column=1,columnspan=5)

# # Create a button for selecting the file path
# select_file_path_button = tk.Button(tab1, text="Select cellfinder output directory", command=browse_file)

# ------ brain region acryonm and names ----------

atlas = BrainGlobeAtlas("allen_mouse_50um")
brain_regions_df = atlas.lookup_df.head(1000)

brain_regions_acronym = brain_regions_df['acronym'].to_list()
brain_regions_name = brain_regions_df['name'].to_list()

BrainGlobeAtlas_dictionary = dict(
    zip(brain_regions_acronym, brain_regions_name))

BrainGlobeAtlas_dictionary['Acronym'] = brain_regions_acronym
BrainGlobeAtlas_dictionary['Brain Region'] = brain_regions_name

# Create the listbox to display the data
listbox = tk.Listbox(tab4)

for acronym, name in BrainGlobeAtlas_dictionary.items():
    listbox.insert(tk.END, f" {acronym},  {name}")

# --------- add click on brainregion acryonm to list -----------

selected_items = []
def add_selected_item_to_list(event):
    # Get the selected item from the listbox
    selected_index = listbox.curselection()[0]
    selected_item = listbox.get(selected_index)

    # acronym, brain_region = selected_item.split(', ',1)
    acronym, brain_region = selected_item.split(',  ')

    if acronym not in selected_items:
        # Add the brain region name to the list of selected items
        selected_items.append(acronym)
    
        # extra_brain_region_acryonm_entry.insert(0, acronym + ',')
         # Check if the list has more than one item
        if len(selected_items) > 1:
            extra_brain_region_acryonm_entry.insert(0, acronym + ',' )
        else:
            extra_brain_region_acryonm_entry.insert(0, acronym)
    
      
    print(selected_items)

# --------- Search bar for extra brain regions -----------
# Create a search bar
search_var = tk.StringVar()
search_entry = tk.Entry(tab4, textvariable=search_var)

# Function to filter the listbox based on the search query
def filter_listbox(event):
    search_query = search_var.get().lower()
    listbox.delete(0, tk.END)
    for acronym, brain_region in BrainGlobeAtlas_dictionary.items():
        if search_query in brain_region.lower():
            listbox.insert(tk.END, f" {acronym},  {brain_region}")

# Call the filter function whenever the search bar changes
search_entry.bind("<KeyRelease>", filter_listbox)
  
  

# Bind the function to the listbox's `<Button-1>` event
listbox.bind('<Button-1>', add_selected_item_to_list)

# Bind the function to the listbox
listbox.bind('<ButtonRelease-1>', add_selected_item_to_list)

# ----- Functions -----

# show_lables function
def on_checkbutton_click():
    global show_lables
    if checkbutton_var.get() == 1:
        show_lables = True
        print(show_lables)
    else:
        show_lables = False
        print(show_lables)

checkbutton_var = tk.IntVar()
checkbutton = tk.Checkbutton(tab4, text= "Show Brain Region Labels", variable=checkbutton_var, command=on_checkbutton_click)

# estim render in slected brain region function
def on_estim_checkbutton_click():
    global brain_region_estim
    if checkbutton_var_estim.get() == 1:
        brain_region_estim = True
    else:
        brain_region_estim = False

checkbutton_var_estim = tk.IntVar()
checkbutton_estim = tk.Checkbutton(tab2, text= "Render Estim at center of selected brain region", variable=checkbutton_var_estim, command=on_estim_checkbutton_click)

def on_gfp_checkbutton_click():
    global show_gfp_only
    global show_tdTomato_only
    global show_gfp_tdTomato_overlapping
    global overlapping_cells_only
    if checkbutton_var_02.get() == 1:
        checkbutton_var_03.set(0)
        checkbutton_var_04.set(0)
        checkbutton_var_05.set(0)
        show_gfp_only = True
        show_tdTomato_only = False
        overlapping_cells_only = False
        show_gfp_tdTomato_overlapping = False

    else:
        show_gfp_only = False

checkbutton_var_02 = tk.IntVar()
checkbutton_02 = tk.Checkbutton(tab3, text= "show GFP cells only", variable=checkbutton_var_02, command=on_gfp_checkbutton_click)

def on_tdTomato_checkbutton_click():
    global show_tdTomato_only
    global show_gfp_only
    global show_gfp_tdTomato_overlapping
    global overlapping_cells_only
    if checkbutton_var_03.get() == 1:
        checkbutton_var_02.set(0)
        checkbutton_var_04.set(0)
        checkbutton_var_05.set(0)
        show_tdTomato_only = True
        show_gfp_only = False
        overlapping_cells_only = False
        show_gfp_tdTomato_overlapping = False
    else:
        show_tdTomato_only = False

checkbutton_var_03 = tk.IntVar()
checkbutton_03 = tk.Checkbutton(tab3, text="show tdTomato cells only", variable=checkbutton_var_03, command=on_tdTomato_checkbutton_click)

def on_overlapping_checkbutton_click():
    global overlapping_cells_only
    global show_gfp_only
    global show_tdTomato_only
    global show_gfp_tdTomato_overlapping
    if checkbutton_var_04.get() == 1:
        checkbutton_var_02.set(0)
        checkbutton_var_03.set(0)
        checkbutton_var_05.set(0)
        overlapping_cells_only = True
        show_gfp_only = False
        show_tdTomato_only = False
        show_gfp_tdTomato_overlapping = False
    else:
        overlapping_cells_only = False

checkbutton_var_04 = tk.IntVar()
checkbutton_04 = tk.Checkbutton(tab3, text="show gfp/tdTomato overlapping cells only", variable=checkbutton_var_04, command=on_overlapping_checkbutton_click)

def on_all_cells_checkbutton_click():
    global show_gfp_tdTomato_overlapping
    global show_gfp_only
    global show_tdTomato_only
    global overlapping_cells_only
    if checkbutton_var_05.get() == 1:
        checkbutton_var_02.set(0)
        checkbutton_var_03.set(0)
        checkbutton_var_04.set(0)
        show_gfp_tdTomato_overlapping = True
        show_gfp_only = False
        show_tdTomato_only = False
        overlapping_cells_only = False
    else:
        show_gfp_tdTomato_overlapping = False

checkbutton_var_05 = tk.IntVar()
checkbutton_05 = tk.Checkbutton(tab3, text="show gfp, tdTomato and overlapping cells", variable=checkbutton_var_05, command=on_all_cells_checkbutton_click)


# save_render function
def on_render_checkbutton_click():
    global save_render
    if checkbutton_var_render.get() == 1:
        save_render = True
        print(save_render)
    else:
        save_render = False
        print(save_render)

checkbutton_var_render = tk.IntVar()
checkbutton_render = tk.Checkbutton(root, text="Save 3D Render", variable=checkbutton_var_render, command=on_render_checkbutton_click)

# estim coordinates function 
def create_coordinates():
    global estim_tip_coordinates
    x = float(x_entry.get())
    y = float(y_entry.get())
    z = float(z_entry.get())
    estim_tip_coordinates = [x, y, z]
    print(estim_tip_coordinates)

estimCoord_label = tk.Label(tab2, text="Estim Tip Coordinates [y,z,x]")
x_label = tk.Label(tab2, text="Rotral/Caudal")
x_entry = tk.Entry(tab2)
x_entry.insert(tk.END, str(9000.))
y_label = tk.Label(tab2, text="Superior/Inferior or Dorsal/Venntral")
y_entry = tk.Entry(tab2)
y_entry.insert(tk.END, str(1200.))
z_label = tk.Label(tab2, text="Medial/Lateral")
z_entry = tk.Entry(tab2)
z_entry.insert(tk.END, str(3000.))

x = float(x_entry.get())
y = float(y_entry.get())
z = float(z_entry.get())
estim_tip_coordinates = [x, y, z]
print(estim_tip_coordinates)



# Creates the 3D render when the button is clicked 
def on_button_click():
    cellfinder_output_path = cellfinder_output_path_01_entry.get()
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
    x = float(x_entry.get())
    y = float(y_entry.get())
    z = float(z_entry.get())
    estim_tip_coordinates = [x, y, z]
    print(estim_tip_coordinates)
    # for acryonm in extra_brain_region_acryonm:
    #     acryonm[-1].remove(',')
    
    # Get the value of the Entry widget
    run_brainrender(cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um,estim_shank_radius_um,estim_tip_radius_um,estim_propigation_radius_um,extra_brain_region_acryonm,show_lables,estim_tip_coordinates,save_render,show_gfp_tdTomato_overlapping,show_gfp_only,show_tdTomato_only,overlapping_cells_only,brain_region_estim)
    print("Button was clicked!")
   

# --------- Variables --------

# /Users/grant/Desktop/work/Denman_Lab/Cal_Light/brainrender/cellfinder_brainrender_output/cellfinder_output/

# ------- Entry windows on GUI for each Variable needed --------
# path to cellfinder output data, also where all data will be stored from these files
cellfinder_output_path = tk.StringVar()
cellfinder_output_path_entry = tk.Entry(tab1, textvariable=cellfinder_output_path, width=110)
# cellfinder_output_path_entry.insert(0, "/Users/grant/Desktop/cellfinder_brainrender_output/cellfinder_output/")
label_cellfinder_output_path = tk.Label(tab1, text="Enter path to cellfinder output data ")
# cellfinder_output_path_entry.pack()
# mouse id used, (ie. G19, G18...)
mouse_id = tk.StringVar()
mouse_id_entry = tk.Entry(root, textvariable=mouse_id, width=20)
label_mouse_id = tk.Label(root, text="Enter Mouse ID ")


# number of top brain regions you want to be seen in the render. (top meaning containing the most labled cells)
# brain_regions_to_evalutate = tk.IntVar()
brain_regions_to_evalutate_entry = tk.Entry(tab4, textvariable=brain_regions_to_evalutate, width=20)
brain_regions_to_evalutate_entry.insert(tk.END, str(0))
label_brain_regions_to_evalutate = tk.Label(tab4, text="Enter number of top labled brain regions you want to render ")

# brain_regions_to_evalutate_entry.pack()
# Path to the local allen brain atlas directory you want to use
allen_mouse_10um = tk.StringVar()
allen_mouse_10um_entry = tk.Entry(tab1, textvariable=allen_mouse_10um, width=50)
allen_mouse_10um_entry.insert(0, '/Users/grant/brainglobe/allen_mouse_10um')
label_allen_mouse_10um = tk.Label(tab1, text="Enter path to you local allen brain atlas ")

# -------- Estim text boxes ---------------
estim_shank_radius_um = tk.IntVar()
estim_shank_radius_um_entry = tk.Entry(tab2)
# estim_shank_radius_um_entry = tk.Entry(tab2, textvariable=estim_shank_radius_um, width=20,insertwidth=1)
estim_shank_radius_um_entry.insert(tk.END, str(50))
label_estim_shank_radius_um = tk.Label(tab2, text="Enter estim shank radius in (um) ")


estim_tip_radius_um = tk.IntVar()
estim_tip_radius_um_entry = tk.Entry(tab2)
estim_tip_radius_um_entry.insert(tk.END, str(10))
estim_shank_radius_um_entry.config(insertwidth=1)
label_estim_tip_radius_um  = tk.Label(tab2, text="Enter estim tip radius in (um)")



estim_propigation_radius_um = tk.IntVar()
estim_propigation_radius_um_entry = tk.Entry(tab2)
estim_propigation_radius_um_entry.insert(tk.END, str(300))
label_estim_propigation_radius_um = tk.Label(tab2, text="Enter estim propigation radius in (um)")

# ---------- brain region text boxes -------------
extra_brain_region_acryonm = tk.StringVar()
extra_brain_region_acryonm_entry = tk.Entry(tab4, textvariable=extra_brain_region_acryonm, width=100)
label_extra_brain_region_acryonm = tk.Label(tab4, text="Select Brain Regions from list below that you want to see in the render ")

# Search bar label
label_search_bar = tk.Label(tab4, text="Search for Brain Regions")



# estim_tip_coordinates = tk.StringVar()
# estim_tip_coordinates_entry = tk.Entry(tab2, textvariable=extra_brain_region_acryonm, width=50)
# estim_tip_coordinates_entry.insert(tk.END, str("5300., 5350., 3300."))
# label_estim_tip_coordinates = tk.Label(tab2, text="Enter the coordinates of your estim tip ")


# ---- Buttons -----
run_button = tk.Button(root, text="Create 3D Render", command=on_button_click)


# grid for the gui\
# ------- import Tab ----------------
# select_file_path_button.grid(row=1, column=1, padx=10, pady=10)
# # label_cellfinder_output_path.grid(row=1, column=2)
# cellfinder_output_path_entry.grid(row=2, column=2)

# label_allen_mouse_10um.grid(row=7, column=2)
# allen_mouse_10um_entry.grid(row=8,column=2)

# select_file_path_button.pack()
browse_image_directory_button_01.pack()
cellfinder_output_path_01_entry.pack()


# label_cellfinder_output_path.grid(row=1, column=2)
# cellfinder_output_path_entry.pack()

label_allen_mouse_10um.pack()
allen_mouse_10um_entry.pack()

# ------- Estim Tab ----------------

estimCoord_label.grid(row=0, column=4)
x_label.grid(row=1, column=4)
x_entry.grid(row=2, column=4)
y_label.grid(row=3, column=4)
y_entry.grid(row=4, column=4)
z_label.grid(row=5, column=4)
z_entry.grid(row=6, column=4)
checkbutton_estim.grid(row=7, column=4)


label_estim_shank_radius_um.grid(row=0, column=2)
estim_shank_radius_um_entry.grid(row=1,column=2,)

label_estim_tip_radius_um.grid(row=2, column=2)
estim_tip_radius_um_entry.grid(row=3,column=2)

label_estim_propigation_radius_um.grid(row=4, column=2)
estim_propigation_radius_um_entry.grid(row=5,column=2)

# ----------- channels tab -------------------
# checkbutton_02.grid(row=0, column = 2)
checkbutton_02.pack()
checkbutton_03.pack()
checkbutton_04.pack()
checkbutton_05.pack()
# -----------Brain region Tab --------------
label_extra_brain_region_acryonm.grid(row=15, column=2)
extra_brain_region_acryonm_entry.grid(row=16, column=2) 

label_brain_regions_to_evalutate.grid(row=5, column=2)
brain_regions_to_evalutate_entry.grid(row=6,column=2)

checkbutton.grid(row=18, column=2)

label_search_bar.grid(row=19, column=2)
search_entry.grid(row=20, column=2)
listbox.grid(row=21, column=2,columnspan=3,sticky='ew')



# --------- Not in a tab -------

label_mouse_id.grid(row=2, column=0)
mouse_id_entry.grid(row=3,column=0)
checkbutton_render.grid(row=4, column=0)
run_button.grid(row=5, column=0)

notebook.grid(row=0, column=0)


checkbutton.bind('<Button-1>', on_checkbutton_click)
# checkbutton_render.bind('<Button-1>', on_render_checkbutton_click)
run_button.bind('<Button-1>', on_button_click)

# clear the exra brain region acryonm list when you hit the backspace or delete key
def clear_selected_items(event):
    selected_items.clear()

extra_brain_region_acryonm_entry.bind("<BackSpace>", clear_selected_items)
extra_brain_region_acryonm_entry.bind("<Delete>", clear_selected_items)



# ---- crerate GUI ------
root.mainloop()
