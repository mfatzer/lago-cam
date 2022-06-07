from PIL import Image, ImageFilter
from urllib import request 
from datetime import datetime, time, date, timedelta
import time as timer 
import os
import cv2
import numpy as np
import glob


imageDir = "./images/"
tempImageDir = "./tempImages/"
fileType = ".jpg"
url = "http://lago-mio.dyndns.org/cgi-bin/api.cgi?cmd=Snap&channel=0&rs=wuuPhkmUCeI9WG7C&user=surfer&password=lago-mio"
bottomFilterHeight = 720

snapshotStartTime = time(7, 0)
snapshotEndTime = time(21, 0)
snapshotInterval = timedelta(minutes=1)


def getProcessedCamImage():
    TEMP_FILE_NAME = tempImageDir + "temp.jpeg"
    request.urlretrieve(url, TEMP_FILE_NAME)

    img = Image.open(TEMP_FILE_NAME)

    # if (os.path.exists(TEMP_FILE_NAME)):
    #     os.remove(TEMP_FILE_NAME)

    width, height = img.size
    filterTop = height - bottomFilterHeight

    filteredImg = img.crop((0, filterTop, width, height))
    filteredImg = filteredImg.filter(ImageFilter.GaussianBlur(14))

    img.paste(filteredImg, (0, filterTop))
    return img


def createDirNameForTime(time):
    return time.strftime("%Y_%m_%d")

def createPathNameForTime(time):
    return imageDir + createDirNameForTime(time) + "/"

def createFileNameForTime(time):
    dateString = time.strftime("%Y_%m_%d")
    timeString = time.strftime("%Y_%m_%d %H-%M-%S")
    dirName = imageDir + dateString + "/"
    fileName = createPathNameForTime(time) + timeString + fileType
    return fileName

def captureAndSaveCamImage():
    currentTime = datetime.now()
    img = getProcessedCamImage()
    dirName = createPathNameForTime(currentTime)
    if (not os.path.isdir(dirName)):
        os.mkdir(dirName)
    fileName = createFileNameForTime(currentTime)
    img.save(fileName)
    return fileName


def isInRecordingTimeSpan(timeToCheck):
    return timeToCheck >= snapshotStartTime and timeToCheck <= snapshotEndTime

def findStartTimeStamp(time):
    if (isInRecordingTimeSpan(time)):
        return time
    else:
        return snapshotEndTime


def findNextTimeStamp(time): 
    currentTimeStamp = datetime.combine(date(2000, 1, 1), time)
    nextSnapshotTime = (currentTimeStamp + snapshotInterval).time()
    if (nextSnapshotTime > snapshotEndTime):
        nextSnapshotTime = snapshotStartTime
    return nextSnapshotTime


def makeVideoOutOfDir(pathName, fileName):
    frameSize = (1920, 1080)
    codec = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(pathName + fileName + ".avi", codec, 25, frameSize)

    for imgFilename in glob.glob(pathName + "*.jpg"):
        img = cv2.imread(imgFilename)
        # cv2.imshow("test", img)
        writer.write(img)

    writer.release()
    print("Movie saved as: " + pathName + fileName + ".avi")



def main():
    nextSnapShotTimeStamp = findStartTimeStamp(datetime.now().time())
    while(True):
        currentTime = datetime.now()

        if (currentTime.time() >= nextSnapShotTimeStamp):
            fileName = captureAndSaveCamImage()
            nextSnapShotTimeStamp = findNextTimeStamp(nextSnapShotTimeStamp)
            print("Image saved as: " + fileName)
            makeVideoOutOfDir(createPathNameForTime(currentTime), createDirNameForTime(currentTime))

        else:
            timer.sleep(1)
        


if __name__ == "__main__":
    main()