from __future__ import print_function
import cv2 as cv
import argparse
def detectAndDisplay(frame):
    #creates a gray version of the video passed in (aka variable named frame)
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #improves contrast of an image pixel by pixel for easier face/eye tracking
    frame_gray = cv.equalizeHist(frame_gray)

    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
    #this will display our video with the eye/face detection shapes
    cv.imshow('Capture - Face detection', frame)


parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')

#NOTE: if you want to run this on your local machine you'll need to clone this git repo with the haarcascades first
parser.add_argument('--face_cascade', help='Path to face cascade.', default='C:/Users/VSalinas/Documents/cs490/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='C:/Users/VSalinas/Documents/cs490/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')

#parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)

args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()

#-- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)

if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

#only need camera_device variable for webcam face/eye tracking
#camera_device = args.camera
#-- 2. Read the video stream
#cap = cv.VideoCapture(camera_device)

#testing our video capture here (face and eye tracking is working but it's reading the frames too slowly
#even with a 5 milisecond delay between frames
cap = cv.VideoCapture("C:/Users/VSalinas/Downloads/10_e0.mp4")

if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)

    #NOTE: 27 is the ASCII value of 'esc' (so think of it as pressing escape)
    # if the escape key is pressed during the video, break (each frame waits 5 miliseconds before the next)
    if cv.waitKey(5) == 27:
        break
