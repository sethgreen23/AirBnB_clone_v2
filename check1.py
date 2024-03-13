#!/usr/bin/python3
import glob
import os
import time
"""
list_of_files = glob.glob('versions/web_static_*.tgz')
latest_file = max(list_of_files, key=os.path.getctime)
print((time.time() - os.path.getctime(latest_file))/60)
"""
list_names = None
try:
    list_names = glob.glob('versions/web_static_*.tgz')
except Exception as e:
    pass

if list_names is None:
    print("[list none] i create new file")
else:
    print("list exists")
    print(list_names)
    archive_path = max(list_names, key=os.path.getctime)
    print(archive_path)
    time_elapsed = (time.time() - os.path.getctime(archive_path))/60
    if time_elapsed  > 1:
        print(archive_path)
        print("[archive exist but old] i create new one")
