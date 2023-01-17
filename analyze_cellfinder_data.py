

# Run this file in an Ananconda enviroment that has had cellfinder installed
# (cellfinder2) path/to/run_to_analyze_cellfinder_data
# You may need to downgrade numpy inisde this enviroment to get the file to run

import UpdateME
from UpdateME import cellfinder_output_path, mouse_id, brain_regions_to_evalutate, allen_mouse_10um
import analyze_cellfinder_data
from analyze_cellfinder_data import analyze_data_cellfinder


analyze_data_cellfinder(cellfinder_output_path, mouse_id)
