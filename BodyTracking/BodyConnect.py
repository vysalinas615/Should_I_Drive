import cv2 as cv

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

BODY_CONNECTIONS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

def outputDefaults(inputFile):

    net = cv.dnn.readNetFromTensorflow("graph_opt.pb")
    cap = cv.VideoCapture(inputFile)

    #Defaults
    w = 360
    h = 360
    threshold = 0.2

    while cv.waitKey(1) < 0:
        hasFrame, frame = cap.read()
        if not hasFrame:
            cv.waitKey()
            break

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        net.setInput(cv.dnn.blobFromImage(frame, 1.0, (w, h), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        out = net.forward()
        out = out[:, :19, :, :]

        assert(len(BODY_PARTS) == out.shape[1])

        points = []
        for i in range(len(BODY_PARTS) - 1):
            heatMap = out[0, i, :, :]

            _, conf, _, point = cv.minMaxLoc(heatMap)
            x = (frameWidth * point[0]) / out.shape[3]
            y = (frameHeight * point[1]) / out.shape[2]

            print((int(x), int(y))  if conf > threshold else (-1, -1))

            points.append((int(x), int(y)) if conf > threshold else None)


        for pair in BODY_CONNECTIONS:
            partFrom = pair[0]
            partTo = pair[1]

            assert(partFrom in BODY_PARTS)
            assert(partTo in BODY_PARTS)

            idFrom = BODY_PARTS[partFrom]
            idTo = BODY_PARTS[partTo]

            if points[idFrom] and points[idTo]:

                cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (255, 0, 0), cv.FILLED)
                cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

        t, _ = net.getPerfProfile()
        freq = cv.getTickFrequency() / 1000
        cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        cv.imshow('BodyConnect', frame)



def output(inputFile, w, h, threshold):

    net = cv.dnn.readNetFromTensorflow("graph_opt.pb")
    cap = cv.VideoCapture(inputFile)

    while cv.waitKey(1) < 0:
        hasFrame, frame = cap.read()
        if not hasFrame:
            cv.waitKey()
            break

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        net.setInput(cv.dnn.blobFromImage(frame, 1.0, (w, h), (127.5, 127.5, 127.5), swapRB=True, crop=False))
        out = net.forward()
        out = out[:, :19, :, :]

        assert(len(BODY_PARTS) == out.shape[1])

        points = []
        for i in range(len(BODY_PARTS) - 1):
            heatMap = out[0, i, :, :]

            _, conf, _, point = cv.minMaxLoc(heatMap)
            x = (frameWidth * point[0]) / out.shape[3]
            y = (frameHeight * point[1]) / out.shape[2]

            print((int(x), int(y))  if conf > threshold else (-1, -1))

            points.append((int(x), int(y)) if conf > threshold else None)


        for pair in BODY_CONNECTIONS:
            partFrom = pair[0]
            partTo = pair[1]

            assert(partFrom in BODY_PARTS)
            assert(partTo in BODY_PARTS)

            idFrom = BODY_PARTS[partFrom]
            idTo = BODY_PARTS[partTo]

            if points[idFrom] and points[idTo]:

                cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (255, 0, 0), cv.FILLED)
                cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

        t, _ = net.getPerfProfile()
        freq = cv.getTickFrequency() / 1000
        cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        cv.imshow('BodyConnect', frame)

