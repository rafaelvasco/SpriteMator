from io import BytesIO

from PIL import Image, ImageChops, ImageQt
from PyQt5.QtCore import QBuffer, QIODevice


def qimage_to_pil_image(image):
    buffer = QBuffer()

    buffer.open(QIODevice.ReadWrite)

    image.save(buffer, "PNG")

    bytesio = BytesIO()
    bytesio.write(buffer.data())

    buffer.close()

    bytesio.seek(0)

    pil_image = Image.open(bytesio)

    return pil_image


def _most_popular_edge_color(image):
    im = image
    if im.mode != 'RGB':
        im = image.convert("RGB")

    # Get pixels from the edges of the image:
    width, height = im.size
    left = im.crop((0, 1, 1, height - 1))
    right = im.crop((width - 1, 1, width, height - 1))
    top = im.crop((0, 0, width, 1))
    bottom = im.crop((0, height - 1, width, height))
    pixels = left.tostring() + right.tostring() + top.tostring() + bottom.tostring()

    # Compute who's the most popular RGB triplet
    counts = {}
    for i in range(0, len(pixels), 3):
        rgb = pixels[i] + pixels[i + 1] + pixels[i + 2]
        if rgb in counts:
            counts[rgb] += 1
        else:
            counts[rgb] = 1

    # Get the colour which is the most popular:
    most_popular_color = \
        sorted([(count, rgba) for (rgba, count) in counts.items()], reverse=True)[0][1]

    return ord(most_popular_color[0]), ord(most_popular_color[1]), ord(most_popular_color[2])


def crop(image, background_color=None):
    pil_image = qimage_to_pil_image(image)

    bbox = None

    # If the image has an alpha (tranparency) layer, we use it to crop the image.
    # Otherwise, we look at the pixels around the image (top, left, bottom and right)
    # and use the most used color as the color to crop.

    # --- For transparent images -----------------------------------------------
    if 'A' in pil_image.getbands():  # If the image has a transparency layer, use it.
        # This works for all modes which have transparency layer
        bbox = pil_image.split()[list(pil_image.getbands()).index('A')].getbbox()
    # --- For non-transparent images -------------------------------------------
    elif pil_image.mode == 'RGB':
        if not background_color:
            background_color = _most_popular_edge_color(pil_image)
        # Crop a non-transparent image.
        # .getbbox() always crops the black color.
        # So we need to substract the "background" color from our image.
        bg = Image.new("RGB", pil_image.size, background_color)
        diff = ImageChops.difference(pil_image, bg)  # Substract background color from image
        bbox = diff.getbbox()  # Try to find the real bounding box of the image.

    if bbox:
        pil_image = pil_image.crop(bbox)

    return ImageQt.ImageQt(pil_image)
