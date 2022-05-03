from os import listdir
from os.path import isfile, join

import cv2 as cv
import pandas as pd

BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
              "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

BODY_CONNECTIONS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                    ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                    ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                    ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                    ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]

def getVideoData(currentVideo):
    cap = cv.VideoCapture(currentVideo)
    bodyFrames = []

    while(True):
        success, image = cap.read()

        if not success:
            break

        bodyFrame = processFrame(image)
        bodyFrames.append(bodyFrame)

    return bodyFrames

def processFrame(frame):
    net = cv.dnn.readNetFromTensorflow("graph_opt.pb")

    argMap = {"threshold": 0.2, "w": 368, "h": 368}

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (argMap['w'], argMap['h']), (127.5, 127.5, 127.5), swapRB=True,
                                      crop=False))
    out = net.forward()
    out = out[:, :19, :, :]

    assert (len(BODY_PARTS) == out.shape[1])

    output = []
    for i in range(len(BODY_PARTS) - 1):

        heatMap = out[0, i, :, :]

        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]

        if conf > argMap['threshold']:
            output.append(int(x))
            output.append(int(y))
        else:
            output.append(-1)
            output.append(-1)
    return output


def getFrameData(currentFrame):

    cap = cv.VideoCapture(currentFrame if currentFrame else 0)

    success, frame = cap.read()
    if not success:
        return

    return processFrame(frame)

def frameToCSV(currentFrame, fileName):
    frameData = getFrameData(currentFrame)

    dataframe = pd.DataFrame(frameData)
    dataframe.to_csv(fileName, index=False)


def videoToCSV(currentVideo, fileName):
    frameData = getVideoData(currentVideo)

    dataframe = pd.DataFrame(frameData)
    dataframe.to_csv(fileName, index=False)

def allVideosToCSV(startDir, outputFile):
    videoArray = []

    allVideos = [f for f in listdir(startDir) if isfile(join(startDir, f))]

    for filePath in allVideos:
        print(filePath)
        videoArray.append(getVideoData(startDir + filePath))

    print(videoArray)
    frameData = videoArray

    dataframe = pd.DataFrame(frameData)
    dataframe.to_csv(outputFile, index=False)