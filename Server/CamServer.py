from camlib import *
from flask import Flask
from flask import send_file
from flask_cors import CORS


# Ram-disk is needed on "/mnt/ramdisk"
IMAGE_NAME = "/mnt/ramdisk/image.jpeg"

app = Flask(__name__)
cors = CORS(app)


@app.route("/get_image", methods=["GET"])
def get_cam_image():
    get_processed_cam_image(IMAGE_NAME)
    return send_file(IMAGE_NAME, mimetype='image/jpeg')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
