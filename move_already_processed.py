import os
from os import path
import shutil

output_dir = "/home/cc/eecs151/fa19/class/eecs151-aao/cs170-team-project/outputs"
input_dir = "/home/cc/eecs151/fa19/class/eecs151-aao/cs170-team-project/inputs"
dest_dir = "/home/cc/eecs151/fa19/class/eecs151-aao/cs170-team-project/processed_inputs"

if os.path.exists(dest_dir) == False:
    os.makedirs(dest_dir)

output_files = os.listdir(output_dir)
for f in output_files:
    if os.path.exists(path.join(input_dir, f.split(".")[0]+".in")):
        shutil.move(path.join(input_dir, f.split(".")[0]+".in"), dest_dir)