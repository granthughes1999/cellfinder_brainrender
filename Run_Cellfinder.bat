@echo off
title Run Cellfinder2
echo cd C:\data\Denman_B2-2-whole-brain_GFP\488nm_GFP
call conda activate cellfinder2 
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
cellfinder -s C:\data\Denman_B2-2-whole-brain_GFP\488nm_GFP -b C:\data\Denman_B2-2-whole-brain_GFP\488nm_GFP -o C:\Users\denma\Desktop\Grant\cellfinder\cellfinder_output_010623 --orientation spl -v 4 1.8 1.8 --atlas allen_mouse_50um