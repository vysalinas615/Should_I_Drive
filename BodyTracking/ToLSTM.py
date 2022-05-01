import cv2 as cv

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
    bodyFrames = [[]]

    while(True):
        success, image = cap.read()

        if not success:
            cv.waitKey()
            break

        bodyFrame = processFrame(image)
        print(bodyFrame)
        bodyFrames.append(bodyFrame)

    return bodyFrames


    # count = 0
    # while success:
    #     # currentFrame = cap.
    #
    #     cv.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
    #     cv.im
    #
    #     success, image = cap.read()
    #     getFrameData("frame%d.jpg" % count)
    #     print(count)
    #
    #     # print('Read a new frame: ', success)
    #     count += 1

def processFrame(frame):
    argMap = {"img": "abc", "threshold": 0.2, "w": 368, "h": 368}

    net = cv.dnn.readNetFromTensorflow("graph_opt.pb")
    # cap = cv.VideoCapture(argMap['img'] if argMap['img'] else 0)

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

    argMap = {"img": currentFrame, "threshold": 0.2, "w": 368, "h": 368}

    net = cv.dnn.readNetFromTensorflow("graph_opt.pb")
    cap = cv.VideoCapture(argMap['img'] if argMap['img'] else 0)

    while cv.waitKey(1) < 0:
        hasFrame, frame = cap.read()
        if not hasFrame:
            cv.waitKey()
            break

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        net.setInput(cv.dnn.blobFromImage(frame, 1.0, (argMap['w'], argMap['h']), (127.5, 127.5, 127.5), swapRB=True, crop=False))
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


bodyFrames = getVideoData("43_e0.mp4")
print(bodyFrames)


# output = getFrameData("s4.jpeg")
# print(output)