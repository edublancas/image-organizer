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

    files = [f for f in listdir(args.source)
             if isfile(join(args.source, f)) and not f.startswith(args.source)]

    for folder in folders.values():
        if not os.path.exists(folder):
            os.makedirs(folder)

    for file, media_type in get_image_type(files):
        folder = folders[media_type]
        os.rename(os.path.join(args.source, file),
                  os.path.join(args.destiny, folder, file))
