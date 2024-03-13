#!/usr/bin/python3

import os
import fnmatch

def find_files(base, pattern):
    '''Return list of files matching pattern in base folder.'''
    return [n for n in fnmatch.filter(os.listdir(base), pattern) if
        os.path.isfile(os.path.join(base, n))]
l = None
try:
    l = find_files("versions", "web_static_*.tgz")
except Exception as e:
    pass
if l is None:
    print("There is not file")
else:
    print("There is file")
    print(l)
    print(os.path.join("versions", l[0]))
