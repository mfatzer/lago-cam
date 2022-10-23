import os
import time as timer
from datetime import datetime, time, date, timedelta
import cv2
import glob
from camlib import *

# Ram-disk on "mnt/ramdisk" is needed (1TB)

IMAGE_DIR = "/mnt/ramdisk/images/"
TEMP_IMAGE_DIR = "/mnt/ramdisk/tempImages/"
FILE_TYPE = ".jpg"
TEMP_IMAGE_NAME = TEMP_IMAGE_DIR + "temp" + FILE_TYPE

RECORDING_START_TIME = time(7, 0)
RECORDING_END_TIME = time(22, 0)
RECORDING_SNAPSHOT_INTERVAL = timedelta(minutes=1)


def get_processed_cam_image():
    img = get_processed_cam_image(TEMP_IMAGE_NAME)
    return img


def create_dir_name_for_time(time_val):
    return time_val.strftime("%Y_%m_%d")


def create_path_name_for_time(time_val):
    return IMAGE_DIR + create_dir_name_for_time(time_val) + "/"


def create_file_name_for_time(time_val):
    date_string = time_val.strftime("%Y_%m_%d")
    time_string = time_val.strftime("%Y_%m_%d %H-%M-%S")
    dir_name = IMAGE_DIR + date_string + "/"
    file_name = create_path_name_for_time(time_val) + time_string + FILE_TYPE
    return file_name


def capture_and_save_cam_image():
    current_time = datetime.now()
    img = get_processed_cam_image()
    dir_name = create_path_name_for_time(current_time)
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    file_name = create_file_name_for_time(current_time)
    img.save(file_name)
    return file_name


def is_in_recording_time_span(time_to_check):
    return RECORDING_START_TIME <= time_to_check <= RECORDING_END_TIME


def find_start_time_stamp(time_val):
    if is_in_recording_time_span(time_val):
        return time_val
    else:
        return RECORDING_END_TIME


def find_next_time_stamp(time_val):
    current_time_stamp = datetime.combine(date(2000, 1, 1), time_val)
    next_snapshot_time = (current_time_stamp + RECORDING_SNAPSHOT_INTERVAL).time()
    if next_snapshot_time > RECORDING_END_TIME:
        next_snapshot_time = RECORDING_START_TIME
    return next_snapshot_time


def make_video_out_of_dir(path_name, file_name):
    frame_size = (1920, 1080)

    for imgFilename in glob.glob(path_name + "*.jpg"):
        img = cv2.imread(imgFilename)
        # TODO

    print("Movie saved as: " + path_name + file_name + ".avi")


def main():
    next_snap_shot_time_stamp = find_start_time_stamp(datetime.now().time())
    if not os.path.isdir(IMAGE_DIR):
        os.mkdir(IMAGE_DIR)

    if not os.path.isdir(TEMP_IMAGE_DIR):
        os.mkdir(TEMP_IMAGE_DIR)

    while True:
        current_time = datetime.now()

        if current_time.time() >= next_snap_shot_time_stamp:
            file_name = capture_and_save_cam_image()
            next_snap_shot_time_stamp = find_next_time_stamp(next_snap_shot_time_stamp)
            print("Image saved as: " + file_name)
            # makeVideoOutOfDir(createPathNameForTime(currentTime), createDirNameForTime(currentTime))

        else:
            timer.sleep(1)


if __name__ == "__main__":
    main()
