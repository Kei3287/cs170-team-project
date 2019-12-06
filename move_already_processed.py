import os
from os import path
import shutil

output_dir = "C:\\Users\\****\\Desktop\\test1\\"
input_dir = "C:\\Users\\****\\Desktop\\test2\\"
dest_dir = "C:\\Users\\****\\Desktop\\test3\\"

output_files = os.listdir(output_dir)
for f in output_files:
    shutil.move(path.join(input_dir, f.split(".")[0]+".out"), dest_dir)