import logging
from os import listdir, makedirs, rename
from os.path import isfile, join, exists, basename

import exiftool
from tqdm import tqdm

logger = logging.getLogger(__name__)


class MediaType(object):
    """Files are classified in one of this classes
    """
    Screenshot = 'screenshot'
    Photo = 'photo'
    Image = 'image'
    Video = 'video'
    Unknown = 'unknown'
    GenericVideo = 'generic_video'


# each class goes to a single folder
folders = {MediaType.Screenshot: 'screenshots',
           MediaType.Photo: 'photos',
           MediaType.Image: 'generic-images',
           MediaType.Video: 'videos',
           MediaType.Unknown: 'unknown-files',
           MediaType.GenericVideo: 'generic-videos'}


def organize_phone_photos(source, destiny):
    """Organize a phone import
    """
    # get all files in source directory
    files = [join(source, f) for f in listdir(source)
             if isfile(join(source, f)) and not f.startswith('.')]

    logger.info('Files in source directory: %s', files)

    # create folders if they do not exist
    for folder in folders.values():

        path_to_folder = join(destiny, folder)

        if not exists(path_to_folder):
            logger.info('Making directory: %s', path_to_folder)
            makedirs(path_to_folder)

    # go through every image and place it in the folder they belong
    for file, media_type in tqdm(get_image_type(files)):
        folder = folders[media_type]
        rename(file, join(destiny, folder, basename(file)))


def _get_single_image_type(metadata):
    if metadata.get('XMP:UserComment') == 'Screenshot':
        return (metadata['SourceFile'], MediaType.Screenshot)

    elif metadata.get('EXIF:Model'):
        return (metadata['SourceFile'], MediaType.Photo)

    elif (metadata.get('File:MIMEType') and
          'image' in metadata.get('File:MIMEType')):
        return (metadata['SourceFile'], MediaType.Image)

    elif (metadata.get('File:MIMEType') and
          'video' in metadata.get('File:MIMEType')):
        if metadata.get('QuickTime:Model'):
            return (metadata['SourceFile'], MediaType.Video)
        else:
            return (metadata['SourceFile'], MediaType.GenericVideo)
    else:
        return (metadata['SourceFile'], MediaType.Unknown)


def get_image_type(files):
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(files)
        types = [_get_single_image_type(m) for m in metadata]

    return types
