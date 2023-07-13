# From https://stackoverflow.com/questions/13872331/rotating-an-image-with-orientation-specified-in-exif-using-python-without-pil-in

from PIL import Image, ExifTags


# This remains from before QML auto-rotated the picture and is not used any longer
def get_orientation(filepath):
    try:
        image = Image.open(filepath)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())
        image.close()

        if exif[orientation] == 3:
            return 180
        elif exif[orientation] == 6:
            return 270
        elif exif[orientation] == 8:
            return 90
        else:
            return 0

    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        return 0


def get_timestamp(filepath):
    try:
        exifdata = Image.open(filepath)._getexif()
        if exifdata is None:
            return ''
        s = exifdata[36867]
        return s.replace(':', '_').replace(' ', '-')
    except (AttributeError, KeyError, IndexError):
        return ''
