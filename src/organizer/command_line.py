import argparse
import os
from os import listdir
from os.path import isfile, join

from .util import folders, get_image_type


def main():
    parser = argparse.ArgumentParser(description='Organize pictures.')
    parser.add_argument('source', type=str,
                        help='Source folder')
    parser.add_argument('destiny', type=str,
                        help='Destiny folder')

    args = parser.parse_args()

    files = [os.path.join(args.source, f) for f in listdir(args.source)
             if isfile(join(args.source, f)) and not f.startswith('.')]

    for folder in folders.values():
        path_to_folder = os.path.join(args.destiny, folder)
        if not os.path.exists(path_to_folder):
            os.makedirs(path_to_folder)

    for file, media_type in get_image_type(files):
        folder = folders[media_type]
        os.rename(file,
                  os.path.join(args.destiny, folder, os.path.basename(file)))
