import datetime

from PIL import ExifTags, Image


def get_timestamp(filepath):
    try:
        with Image.open(filepath) as img:
            exif = img.getexif()
            if not exif:
                return ''
            ifd = exif.get_ifd(ExifTags.IFD.Exif)
            s = ifd.get(ExifTags.Base.DateTimeOriginal) or exif.get(ExifTags.Base.DateTimeOriginal)
        if not s:
            return ''
        return datetime.datetime.strptime(s, '%Y:%m:%d %H:%M:%S')
    except (AttributeError, KeyError, IndexError, ValueError, OSError):
        return ''
