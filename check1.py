#!/usr/bin/python3
import glob
import os

list_of_files = glob.glob('versions/web_static_*.tgz')
print(list_of_files)
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
