"""
Clean a folder with JPG and RAW files by removing RAW files that do not have
a JPG match
"""
from pathlib import Path
from os import listdir
from collections import namedtuple

path = '/Users/edu/Tresors/Pictures/Sony/cabos-day-1'

File = namedtuple('File', ['filename', 'extension'])

files = [File(*f.split('.')) for f in listdir(path)]

jpg = [f for f in files if f.extension == 'JPG']
raw = [f for f in files if f.extension == 'ARW']


raw_filenames = set([f.filename for f in raw])
jpg_filenames = set([f.filename for f in jpg])

missing = raw_filenames - jpg_filenames

to_remove = [f+'.ARW' for f in missing]

to_remove_paths = [Path(path, f) for f in to_remove]

for p in to_remove_paths:
    print(f'Removing {p}')
    p.unlink()
