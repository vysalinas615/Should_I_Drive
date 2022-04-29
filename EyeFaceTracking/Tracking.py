from __future__ import print_function
from csv import writer
import cv2
import argparse
import numpy as np


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def detectAndDisplay(frame):

    # Changed the algorithm to only use frame_gray as the cropped grayed out version of the video
    # roiTRY is essentially the video with the tracking shapes overlaid (it's also cropped)

    # creates a gray version of the video passed in (aka variable named frame)
    frame_gray = cv2.cvtColor(frame[0: 750, 700: 1300], cv2.COLOR_BGR2GRAY)
    # improves contrast of an image pixel by pixel for easier face/eye tracking
    frame_gray = cv2.equalizeHist(frame_gray)

    #This gives us the right half of the screen (might have to adjust it depending on the video)
    roiTRY = frame[0: 750, 700: 1300]

    # Detect faces within the webcam footage/ video capture
    faces = face_cascade.detectMultiScale(roiTRY)
    # Prints arrays with 4 values (looks to be a multi-dimensional array)

    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        # (B, G, R) controls color shape displayed. Last value (2) controls line thickness
        # Changed shape and shape color around face from circle to rectangle

        frame = cv2.rectangle(frame[0: 750, 700: 1300], (x, y), (x + w, y + h), (255, 255, 0), 2)
        faceROI = frame_gray[y:y + h, x:x + w] #faceROI = roiTRY[y:y + h, x:x + w]
        # In each face, detect eyes (NOTE: type of eyes is an n-dimensional array)
        eyes = eyes_cascade.detectMultiScale(faceROI)
        # TODO:// Eye tracking finds 3 eyes sometimes. See if that can be fixed

        # NOTE: If eyes are not detected, the type of eyes changes from an ndarray to a tuple
        if type(eyes) == tuple:
            # x1, x2, y1, y2 are filled with -1's if eyes aren't detected so the lstm has values for each frame
            noEyesArray = np.array([-1, -1, -1, -1])
            print("\t NO EYES DETECTED:\n\t\t", noEyesArray, "\n")
            # set values to -1 so that the lstm always has a numerical value for each frame
            append_list_as_row(r"C:\Users\VSalinas\Documents\cs490\Test.csv", noEyesArray)

        else:
            # If eyes returns a ndarray and the # of items is <8 print the array
            if eyes.size > 8:
                # An array with more than 8 items indicates a tracking issue
                print("INVALID TACKING POINTS \n ")
                append_list_as_row(r"C:\Users\VSalinas\Documents\cs490\Test.csv", eyes)

            else:
                print("EYES: ", eyes, "\n")
                append_list_as_row(r"C:\Users\VSalinas\Documents\cs490\Test.csv", eyes)


        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            # Creates yellow circles around the centers of the eyes
            roiTRY = cv2.circle(roiTRY, eye_center, radius, (0, 255, 255), 2)
    # this will display our video with the eye/face detection shapes
    cv2.imshow('Capture - Face detection', roiTRY)


parser = argparse.ArgumentParser(description='Code for eye/face tracking.')

# NOTE: if you want to run this on your local machine you'll need to clone this git repo with the haarcascades first
parser.add_argument('--face_cascade', help='Path to face cascade.',
                    default='C:/Users/VSalinas/Documents/cs490/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.',
                    default='C:/Users/VSalinas/Documents/cs490/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')

# uncomment the line below, remove passed in mp4's before using the code to run in realtime on a webcam
# parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)

args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
# allows us to utilize pretrained eye and face models gathered from the haarcascades repo
face_cascade = cv2.CascadeClassifier()
eyes_cascade = cv2.CascadeClassifier()

# Load the cascades
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
    if cv2.waitKey(1) == 27:
        break
