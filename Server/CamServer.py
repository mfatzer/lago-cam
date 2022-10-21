import json
from flask import Flask
from flask_cors import CORS
from flask import request
from flask import send_file
from PIL import Image, ImageFilter
from urllib import request 


# Ram-disk is needed on "/mnt/ramdisk"

URL = "http://lago-mio.dyndns.org/cgi-bin/api.cgi?cmd=Snap&channel=0&rs=wuuPhkmUCeI9WG7C&user=surfer&password=lago-mio"
BOTTOM_FILTER_HEIGHT = 720
IMAGE_NAME = "/mnt/ramdisk/image.jpeg"

app = Flask(__name__)
cors = CORS(app)


def getProcessedCamImage(imageName):
    request.urlretrieve(URL, imageName)

    img = Image.open(imageName)

    width, height = img.size
    filterTop = height - BOTTOM_FILTER_HEIGHT

    filteredImg = img.crop((0, filterTop, width, height))
    filteredImg = filteredImg.filter(ImageFilter.GaussianBlur(14))

    img.paste(filteredImg, (0, filterTop))
    img.save(imageName)


@app.route("/get_image", methods=["GET"])
def getCamImage():
    img = getProcessedCamImage(IMAGE_NAME)
    return send_file(IMAGE_NAME, mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
