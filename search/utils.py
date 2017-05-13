import magic

VALID_IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]
VALID_IMAGE_MIMETYPES = [
    "image"
]


def get_mimetype(fobject):
    """
    Guess mimetype of a file using python-magic
    """
    mime = magic.Magic(mime=True)
    mimetype = mime.from_buffer(fobject.read(1024))
    fobject.seek(0)
    return mimetype


def valid_image_mimetype(fobject):
    """
    Look inside the file using python-magic to make sure the mimetype
    is an image

    - http://stackoverflow.com/q/20272579/396300
    """
    mimetype = get_mimetype(fobject)
    if mimetype:
        return mimetype.startswith('image')
    else:
        return False
