"""
Organize images. It takes a folder with images and organizes them in
Screenshots/, Pictures/ (from camera), Images/, Videos/ or
Unknown/ depending on the metadata
"""
from os import listdir, makedirs, rename
from os.path import isfile, join, exists, basename

from .util import folders, get_image_type
from .clean import clean_raw_folder

import click
from tqdm import tqdm


@click.group()
def cli():
    """Command line group
    """
    pass


@cli.command()
@click.argument('source', type=click.Path(exists=True, file_okay=False,
                                          resolve_path=True))
@click.argument('destiny', type=click.Path(exists=True, file_okay=False,
                                           resolve_path=True))
def organize(source, destiny):
    """Organize pictures in folders
    """
    # get all files in source directory
    files = [join(source, f) for f in listdir(source)
             if isfile(join(source, f)) and not f.startswith('.')]

    # create folders if they do not exist
    for folder in folders.values():
        path_to_folder = join(destiny, folder)
        if not exists(path_to_folder):
            makedirs(path_to_folder)

    # go through every image and place it in the folder they belong
    for file, media_type in tqdm(get_image_type(files)):
        folder = folders[media_type]
        rename(file, join(destiny, folder, basename(file)))


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False,
                                        resolve_path=True))
def clean(path):
    """Clean RAW folder
    """
    clean_raw_folder(path)
