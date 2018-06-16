"""
Organize images. It takes a folder with images and organizes them in
Screenshots/, Pictures/ (from camera), Images/, Videos/ or
Unknown/ depending on the metadata
"""
import argparse
from os import listdir, makedirs, rename
from os.path import isfile, join, exists, basename

from .util import folders, get_image_type

from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=str,
                        help='Source folder')
    parser.add_argument('destiny', type=str,
                        help='Destiny folder')

    args = parser.parse_args()

    # get all files in source directory
    files = [join(args.source, f) for f in listdir(args.source)
             if isfile(join(args.source, f)) and not f.startswith('.')]

    # create folders if they do not exist
    for folder in folders.values():
        path_to_folder = join(args.destiny, folder)
        if not exists(path_to_folder):
            makedirs(path_to_folder)

    # go through every image and place it in the folder they belong
    for file, media_type in tqdm(get_image_type(files)):
        folder = folders[media_type]
        rename(file, join(args.destiny, folder, basename(file)))
