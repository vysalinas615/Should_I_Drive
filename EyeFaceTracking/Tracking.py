from __future__ import print_function
import cv2
import argparse


# function which will take in a single frame at a time and identify face/eyes within the frame utilizing pre-trained face/eye detection models
def detectAndDisplay(frame):
    # creates a gray version of the video passed in (aka variable named frame)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # improves contrast of an image pixel by pixel for easier face/eye tracking
    frame_gray = cv2.equalizeHist(frame_gray)

    # Detect faces within the webcam footage/ video capture from the grayed out footage
    faces = face_cascade.detectMultiScale(frame_gray)

    for (x, y, w, h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv2.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h, x:x+w]
        # In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv2.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
    # this will display our video with the eye/face detection shapes
    cv2.imshow('Capture - Face detection', frame)


parser = argparse.ArgumentParser(description='Code for eye/face tracking.')

# NOTE: if you want to run this on your local machine you'll need to clone this git repo with the haarcascades first
parser.add_argument('--face_cascade', help='Path to face cascade.', default='C:/Users/VSalinas/Documents/cs490/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='C:/Users/VSalinas/Documents/cs490/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')

# uncomment the line below, remove passed in mp4's before using the code to run in realtime on a webcam
# parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)

args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
# allows us to utilize pretrained eye and face models gathered from the haarcascades repo
face_cascade = cv2.CascadeClassifier()
eyes_cascade = cv2.CascadeClassifier()

# Load the cascades (the pre-trained models which will help us detect eyes/faces within a frame)
if not face_cascade.load(cv2.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)

if not eyes_cascade.load(cv2.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

# only need camera_device variable for webcam face/eye tracking
# camera_device = args.camera
# Read the video stream using the line below
# cap = cv.VideoCapture(camera_device)

# testing our video capture here (face and eye tracking is working, but it's reading the frames too slowly
# even with a 5-millisecond delay between frames -- try to mutli-thread it later)
cap = cv2.VideoCapture("C:/Users/VSalinas/Downloads/44_e0.mp4")

# throws error if the passed in video capture cannot be opened
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

# keep reading frames until there are no frames left, or the user presses the escape key
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame found, end program.')
        break

    # passes one frame at a time into the detectAndDisplay function from the passed in video capture
    detectAndDisplay(frame)

    # NOTE: 27 is the ASCII value of 'esc' (so think of it as pressing escape)
    # if the escape key is pressed during the video, break (each frame waits 5-milliseconds before the next)
    if cv2.waitKey(5) == 27:
        break
