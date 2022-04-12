import cv2 as cv
import argparse as ap

BODY_PARTS = {"Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
              "LEye": 15, "REar": 16, "LEar": 17, "Background": 18}

BODY_CONNECTIONS = [["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                    ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                    ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                    ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                    ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"]]

wrists = 0
eyes = 0

parser = ap.ArgumentParser()

# Uncomment the line below, and line 33 to run it with a webcam. Be sure to comment out line 36 if using a webcam instead. 
# parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)

args = parser.parse_args()

parser.add_argument('--threshold', default=0.2, type=float, help='Threshold for body connections')
parser.add_argument('--w', default=368, type=int, help='Resize width')
parser.add_argument('--h', default=368, type=int, help='Resize height.')

argMap = parser.parse_args()
# Be sure to load in the graph file from your own directory location
net = cv.dnn.readNetFromTensorflow("C:/Users/VSalinas/Downloads/graph_opt.pb")

# cap = cv.VideoCapture(args.camera) 

# Here we load in one of the trimmed videos from our dataset. Change it to match your own directories.
cap = cv.VideoCapture("C:/Users/VSalinas/Downloads/44_e0.mp4")

while cv.waitKey(1) < 0:
    hasFrame, frame = cap.read()
    if not hasFrame:
        cv.waitKey()
        break

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (argMap.w, argMap.h), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert (len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponding body's part.
        heatMap = out[0, i, :, :]

        # Originally, we try to find all the local maximums. To simplify a sample
        # we just find a global one. However only a single pose at the same time
        # could be detected this way.
        _, conf, _, point = cv.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > argMap.threshold else None)

    for pair in BODY_CONNECTIONS:
        partFrom = pair[0]
        partTo = pair[1]

        assert (partFrom in BODY_PARTS)
        assert (partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:

            if partFrom == "LEye" or partFrom == "REye":
                eyes += 1

            if partTo == "LWrist" or partTo == "RWrist":
                wrists += 1

            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (255, 0, 0), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

    t, _ = net.getPerfProfile()
    freq = cv.getTickFrequency() / 1000
    cv.putText(frame, '%.2fms' % (t / freq), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    cv.imshow('OpenPose using OpenCV', frame)

    print("Num eyes: ", eyes)
    print("Num wrists: ", wrists)
