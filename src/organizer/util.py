import exiftool


class MediaType(object):
    Screenshot = 'screenshot'
    Photo = 'photo'
    Image = 'image'
    Video = 'video'
    Unknown = 'unknown'
    GenericVideo = 'generic_video'


folders = {MediaType.Screenshot: 'Screenshots',
           MediaType.Photo: 'Photos',
           MediaType.Image: 'Images',
           MediaType.Video: 'My Videos',
           MediaType.Unknown: 'Unknown',
           MediaType.GenericVideo: 'Videos'}


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
