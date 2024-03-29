from PIL import Image, ImageFilter
from urllib import request
import constant

BLUR_FILTER_HEIGHT_BOTTOM = 720


def get_processed_cam_image(image_name):
    request.urlretrieve(constant.SNAPSHOT_URL, image_name)

    img = Image.open(image_name)

    width, height = img.size
    filter_top = height - BLUR_FILTER_HEIGHT_BOTTOM

    filtered_img = img.crop((0, filter_top, width, height))
    filtered_img = filtered_img.filter(ImageFilter.GaussianBlur(14))

    img.paste(filtered_img, (0, filter_top))
    img.save(image_name)
    return img
