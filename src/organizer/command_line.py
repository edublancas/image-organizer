import argparse
from os import listdir, makedirs, rename
from os.path import isfile, join, exists, basename

from .util import folders, get_image_type


def main():
    parser = argparse.ArgumentParser(description='Organize pictures.')
    parser.add_argument('source', type=str,
                        help='Source folder')
    parser.add_argument('destiny', type=str,
                        help='Destiny folder')

    args = parser.parse_args()

    files = [join(args.source, f) for f in listdir(args.source)
             if isfile(join(args.source, f)) and not f.startswith('.')]

    for folder in folders.values():
        path_to_folder = join(args.destiny, folder)
        if not exists(path_to_folder):
            makedirs(path_to_folder)

    for file, media_type in get_image_type(files):
        folder = folders[media_type]
        rename(file, join(args.destiny, folder, basename(file)))
