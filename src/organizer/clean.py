"""
Clean a folder with JPG and RAW files by removing RAW files that do not have
a JPG match
"""
from pathlib import Path
from os import listdir
from collections import namedtuple

File = namedtuple('File', ['filename', 'extension'])


def _make_file(filename):
    """Instantiate File objects
    """
    parts = filename.split('.')

    if len(parts) > 1:
        return File(*parts)
    else:
        return File(filename=filename, extension='')


def clean_raw_folder(path):
    """
    Given a folder with JPG and ARW files, remove ARW that do not
    have a corresponding JPG, then remove all JPG
    """

    # list all files in path
    files = [_make_file(f) for f in listdir(path)]

    # split in JPG and RAW
    jpg = [f for f in files if f.extension == 'JPG']
    raw = [f for f in files if f.extension == 'ARW']

    raw_filenames = set([f.filename for f in raw])
    jpg_filenames = set([f.filename for f in jpg])

    # if no JPG is found, remove corresponding RAW
    missing = raw_filenames - jpg_filenames
    to_remove = [f+'.ARW' for f in missing]
    to_remove_paths = [Path(path, f) for f in to_remove]

    for p in to_remove_paths:
        print(f'Removing {p}')
        p.unlink()

    # also remove JPG
    for p in jpg:
        file = Path(path, p.filename+'.JPG')
        print(f'Removing {file}')
        file.unlink()
