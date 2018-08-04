"""Organize images. It takes a folder with images and organizes them in
Screenshots/, Pictures/ (from camera), Images/, Videos/ or
Unknown/ depending on the metadata
"""
import logging

import click

from .clean import clean_raw_folder
from .phone import organize_phone_photos


logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    """Organize pictures from phone and camera
    """
    pass


@cli.command()
@click.argument('source', type=click.Path(exists=True, file_okay=False,
                                          resolve_path=True))
@click.argument('destiny', type=click.Path(exists=True, file_okay=False,
                                           resolve_path=True))
def phone(source, destiny):
    """Organize import from phone
    """
    organize_phone_photos(source, destiny)


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False,
                                        resolve_path=True))
def clean(path):
    """Clean RAW folder
    """
    clean_raw_folder(path)
