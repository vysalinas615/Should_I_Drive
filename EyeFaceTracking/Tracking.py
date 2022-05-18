from __future__ import print_function
from csv import writer
import cv2
import argparse
import numpy as np


# Appends list_of_elem as a row within a (csv) file
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


# Appends a single frame's location_points array(s) to the output_list
def append_locations(output_list, location_points):
    # If the size of output is less than 8, append the item
    if np.size(output_list) < 8:
        output_list.append(location_points)
        print("EYE LOCATIONS: ", output_list, "\n")


# NOTE: If eyes are not detected, the type of eyes changes from ndarray to a tuple
def is_tuple(location_points):
    if type(location_points) == tuple:
        return True
    return False


def detect_and_display(frame):
    # TODO: Set frame = frame[0: 750, 500: 1300] to isolate right half of the screen if driver has passengers

    # The array to contain tracking values for the left/right eyes for a single frame
    output = []
    default_array = np.array([[-1, -1, -1, -1], [-1, -1, -1, -1]])
    
    # creates a gray version of the video passed in (aka variable named frame)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # improves contrast of an image pixel by pixel for easier face/eye tracking
    frame_gray = cv2.equalizeHist(frame_gray)
    # roiTRY - video frame which will have tracking shapes overlaid (cropped if frame was set to [0: 750, 500: 1300])
    roiTRY = frame

    # Detect faces within the webcam footage/ video capture
    faces = face_cascade.detectMultiScale(roiTRY)

    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        # (B, G, R) controls color shape displayed. Last value (2) controls line thickness
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
        faceROI = frame_gray[y:y + h, x:x + w]
        # In each face, detect eyes (NOTE: type of eyes is an n-dimensional array)
        eyes = eyes_cascade.detectMultiScale(faceROI)

        # NOTE: Eye tracking finds 3 eyes sometimes. Temporarily 'fixed it' by discarding last 4 values
        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            # Creates yellow circles around the centers of the eyes
            roiTRY = cv2.circle(roiTRY, eye_center, radius, (0, 255, 255), 2)

        # This will display our video with the eye/face detection shapes
        cv2.imshow('Capture - Face detection', roiTRY)

        # NOTE: If eyes are not detected, the type of eyes changes from an ndarray to a tuple
        if is_tuple(faces) | is_tuple(eyes):
            # if no faces are detected, append a 2D array of -1's
            append_locations(output, default_array.tolist())

        else:
            # If eyes returns a nd-array & the # of items is > 8, append values to output list
            # An array with more than 8 items indicates a tracking issue
            if eyes.size > 8:
                eyes = np.array([eyes[0], eyes[1]])
                # Discards the last 4 values (only appends the first 8 values.)
                append_locations(output, eyes.tolist())

            # Checks to see if only one eye was tracked
            elif eyes.size == 4:
                # Outputs a 2d array with 4 values in the first array, and 4x -1's in the second
                eyes = np.array([eyes[0], [-1, -1, -1, -1]])
                append_locations(output, eyes.tolist())

            # If the ndarray size is == 8, both eyes tracked properly, append data to output list
            else:
                append_locations(output, eyes.tolist())

    # Appends default_array if the output list is empty for a given frame (aka no eyes/faces tracked)
    if np.size(output) == 0:
        append_locations(output, default_array.tolist())

    return output


videoOutput = []
parser = argparse.ArgumentParser(description='Code for eye/face tracking.')
# TODO: if you want to run this on your local machine you'll need to clone this git repo with the haarcascades first
# TODO: Link to repo - https://github.com/opencv/opencv.git
parser.add_argument('--face_cascade', help='Path to face cascade.',
                    default='C:/Users/VSalinas/Documents/cs490/opencv/data/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.',
                    default='C:/Users/VSalinas/Documents/cs490/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')

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

# TODO: Enter the path to your video file here.
cap = cv2.VideoCapture("C:/Users/VSalinas/Downloads/203_e2.mp4")

# throws error if the passed in video capture cannot be opened
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

# keep reading frames until there are no frames left, or the user presses the escape key
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame found, end program.')
        # TODO: Enter a file path where the csv file is to be stored, and name it below
        append_list_as_row(r"C:\Users\VSalinas\Documents\cs490\dataRedo.csv", videoOutput)
        break

    # Passes a single frame into the detectAndDisplay function from the passed in video capture
    output = detect_and_display(frame)
    # Appends tracking locations from every frame into the videoOutput array
    videoOutput.append(output)

    # NOTE: 27 is the ASCII value of 'esc'
    # If the escape key is pressed during the video, break (each frame waits 1-millisecond before the next)
    if cv2.waitKey(1) == 27:
        break
