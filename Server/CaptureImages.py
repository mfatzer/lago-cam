import os
import time as timer
from datetime import datetime, time, date, timedelta
import cv2
import glob
from CamLibrary import *

# Ram-disk on "mnt/ramdisk" is needed (1TB)

imageDir = "/mnt/ramdisk/images/"
tempImageDir = "/mnt/ramdisk/tempImages/"
fileType = ".jpg"

snapshotStartTime = time(7, 0)
snapshotEndTime = time(22, 0)
snapshotInterval = timedelta(minutes=1)


def get_processed_cam_image():
    temp_file_name = tempImageDir + "temp.jpeg"
    img = get_processed_cam_image(temp_file_name)
    return img


def create_dir_name_for_time(time_val):
    return time_val.strftime("%Y_%m_%d")


def create_path_name_for_time(time_val):
    return imageDir + create_dir_name_for_time(time_val) + "/"


def create_file_name_for_time(time_val):
    date_string = time_val.strftime("%Y_%m_%d")
    time_string = time_val.strftime("%Y_%m_%d %H-%M-%S")
    dir_name = imageDir + date_string + "/"
    file_name = create_path_name_for_time(time_val) + time_string + fileType
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
    return snapshotStartTime <= time_to_check <= snapshotEndTime


def find_start_time_stamp(time_val):
    if is_in_recording_time_span(time_val):
        return time_val
    else:
        return snapshotEndTime


def find_next_time_stamp(time_val):
    current_time_stamp = datetime.combine(date(2000, 1, 1), time_val)
    next_snapshot_time = (current_time_stamp + snapshotInterval).time()
    if next_snapshot_time > snapshotEndTime:
        next_snapshot_time = snapshotStartTime
    return next_snapshot_time


def make_video_out_of_dir(path_name, file_name):
    frame_size = (1920, 1080)

    for imgFilename in glob.glob(path_name + "*.jpg"):
        img = cv2.imread(imgFilename)
        # TODO

    print("Movie saved as: " + path_name + file_name + ".avi")


def main():
    next_snap_shot_time_stamp = find_start_time_stamp(datetime.now().time())
    if not os.path.isdir(imageDir):
        os.mkdir(imageDir)

    if not os.path.isdir(tempImageDir):
        os.mkdir(tempImageDir)

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
