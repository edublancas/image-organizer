import exiftool

from os import listdir
from os.path import isfile, join

import os


class MediaType(object):
    Screenshot = 'screenshot'
    Picture = 'picture'
    Image = 'generic'
    Video = 'video'
    Unknown = 'unknown'


folders = {MediaType.Screenshot: 'Screenshots',
           MediaType.Picture: 'Pictures',
           MediaType.Image: 'Generic',
           MediaType.Video: 'Pictures',
           MediaType.Unknown: 'Unknown'}


def _get_single_image_type(metadata):
    if metadata.get('XMP:UserComment') == 'Screenshot':
        return (metadata['SourceFile'], MediaType.Screenshot)
    elif metadata.get('EXIF:Model'):
        return (metadata['SourceFile'], MediaType.Picture)
    elif 'image' in metadata['File:MIMEType']:
        return (metadata['SourceFile'], MediaType.Image)
    elif 'video' in metadata['File:MIMEType']:
        return (metadata['SourceFile'], MediaType.Video)
    else:
        return (metadata['SourceFile'], MediaType.Unknown)


def get_image_type(filenames):
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(filenames)
        types = [_get_single_image_type(m) for m in metadata]

    return types


files = [f for f in listdir('.')
         if isfile(join('.', f)) and not f.startswith('.')]


for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

for file, media_type in get_image_type(files):
    folder = folders[media_type]
    os.rename(file,
              os.path.join(folder, file))

# https://sno.phy.queensu.ca/~phil/exiftool/
# https://github.com/smarnach/pyexiftool
