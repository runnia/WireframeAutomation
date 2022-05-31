from io import BytesIO
import numpy as np
import cv2


def image_from_bytes(image_bytes) -> np.ndarray:  # returns rgb pls
    file_bytes = np.asarray(bytearray(BytesIO(image_bytes).read()), dtype=np.uint8)
    colored_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    cv2.cvtColor(colored_image, cv2.COLOR_BGR2RGB)
    return colored_image


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized
