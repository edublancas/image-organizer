import exiftool


class MediaType(object):
    Screenshot = 'screenshot'
    Picture = 'picture'
    Image = 'image'
    Video = 'video'
    Unknown = 'unknown'


folders = {MediaType.Screenshot: 'Screenshots',
           MediaType.Picture: 'Pictures',
           MediaType.Image: 'Generic',
           MediaType.Video: 'Videos',
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


def get_image_type(files):
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(files)
        types = [_get_single_image_type(m) for m in metadata]

    return types
