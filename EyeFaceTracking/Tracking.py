from __future__ import print_function
from csv import writer
from os import listdir
from os.path import isfile, join
import cv2
import argparse
import numpy as np
import pandas as pd


def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


def getVideoData(currentVideo):
    cap = cv2.VideoCapture(currentVideo)
    eyeFrames = []

    while(True):
        success, image = cap.read()
        if not success:
            break
        eyeFrame = detectAndDisplay(image)
        eyeFrames.append(eyeFrame)
    return eyeFrames

def getFrameData(currentFrame):

    cap = cv2.VideoCapture(currentFrame if currentFrame else 0)

    success, frame = cap.read()
    if not success:
        return
    return detectAndDisplay(frame)

def frameToCSV(currentFrame, fileName):
    frameData = getFrameData(currentFrame)
    dataframe = pd.DataFrame(frameData)
    dataframe.to_csv(fileName, index=False)


def allVideosToCSV(startDir, outputFile):
    videoArray = []
    allVideos = [f for f in listdir(startDir) if isfile(join(startDir, f))]

    for filePath in allVideos:
        print(filePath)
        videoArray.append(getVideoData(filePath))

    frameData = getVideoData(videoArray)
    dataframe = pd.DataFrame(frameData)
    dataframe.to_csv(outputFile, index=False)

# Almost works perfectly currently except sometimes the output is like this [[[116, 65, 42, 42], [38, 56, 49, 49]], [[-1, -1, -1, -1], [-1, -1, -1, -1]]]
def appendLocations(outputList, item):
    outputList.append(item)
    print("TESTING: ", outputList)

def isTuple(item):
    if type(item) == tuple:
        return True
    return False

def detectAndDisplay(frame):

    # Changed the algorithm to only use frame_gray as the cropped grayed out version of the video
    # roiTRY is essentially the video with the tracking shapes overlaid (it's also cropped)

    output = []
    defaultArray = np.array([[-1, -1, -1, -1], [-1, -1, -1, -1]])

    # creates a gray version of the video passed in (aka variable named frame)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #for 44 frame[0: 750, 700: 1300] or [0: 750, 500: 1300]
    # improves contrast of an image pixel by pixel for easier face/eye tracking
    frame_gray = cv2.equalizeHist(frame_gray)

    #This gives us the right half of the screen (might have to adjust it depending on the video)
    roiTRY = frame#[0: 750, 500: 1300]

    # Detect faces within the webcam footage/ video capture
    faces = face_cascade.detectMultiScale(roiTRY)

    for (x, y, w, h) in faces:
        center = (x + w // 2, y + h // 2)
        # (B, G, R) controls color shape displayed. Last value (2) controls line thickness
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2) # frame[0: 750, 700: 1300]
        faceROI = frame_gray[y:y + h, x:x + w] # faceROI = roiTRY[y:y + h, x:x + w]
        # In each face, detect eyes (NOTE: type of eyes is an n-dimensional array)
        eyes = eyes_cascade.detectMultiScale(faceROI)

        # NOTE: Eye tracking finds 3 eyes sometimes. 'Fixed it' by discarding last 3 values
        for (x2, y2, w2, h2) in eyes:
            eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            radius = int(round((w2 + h2) * 0.25))
            # Creates yellow circles around the centers of the eyes
            roiTRY = cv2.circle(roiTRY, eye_center, radius, (0, 255, 255), 2)

        # This will display our video with the eye/face detection shapes
        cv2.imshow('Capture - Face detection', roiTRY)

        # if no faces are detected, append -1's
        #if len(faces) == 0 | len(eyes) == 0:
            #appendLocations(output, defaultArray.tolist())
            #return output

        if isTuple(faces) | isTuple(eyes):
            # noFaceArray = np.array([[-1, -1, -1, -1], [-1, -1, -1, -1]])
            # output.append(noFaceArray.tolist())
            # return output

            appendLocations(output, defaultArray.tolist())
            return output


        # NOTE: If eyes are not detected, the type of eyes changes from an ndarray to a tuple
        #elif type(eyes) == tuple:
            # x1, x2, y1, y2 are filled with -1's if eyes aren't detected so the lstm has values for each frame
            #noEyesArray = np.array([[-1, -1, -1, -1], [-1, -1, -1, -1]])
            #print("\t NO EYES DETECTED:", noEyesArray, "\n")
            # set values to -1 so that the lstm always has a numerical value for each frame
           # append_list_as_row(r"C:\Users\VSalinas\Documents\cs490\90_e1.csv", noEyesArray)
            #print("CHECK1: ", noEyesArray.tolist())

            #uncomment out for csv
            #output.append(noEyesArray.tolist())
            #return output

            #appendLocations(output, defaultArray.tolist())
            #return output

        else:
            # If eyes returns a nd-array & the # of items is > 8 print the array
            if eyes.size > 8:
                # An array with more than 8 items indicates a tracking issue
                # Discard the last 4 values
                eyes = np.array([eyes[0], eyes[1]])
                #print("INVALID TACKING POINTS, EYES:", eyes, "\n")
            #    append_list_as_row(r"C:\Users\VSalinas\Documents\cs490\90_e1.csv", eyes)
                #print("CHECK2: ", eyes.tolist())

                #uncomment out for csv
                #output.append(eyes.tolist())
                #return output

                appendLocations(output, eyes.tolist())
                return output

            # This checks to see if only one eye was tracked
            elif eyes.size == 4:
                # Outputs a 2d array with 4 values in the first array, and 4x -1's in the second
                eyes = np.array([eyes[0], [-1, -1, -1, -1]])
                #print("** INVALID TACKING POINTS, EYES:", eyes, "\n")
             #   append_list_as_row(r"C:\Users\VSalinas\Documents\cs490\90_e1.csv", eyes)
                #print("CHECK3: ", eyes.tolist())

               # uncomment this out for csv
                #output.append(eyes.tolist())
                #return output
                appendLocations(output, eyes.tolist())
                return output

            # If the ndarray size is == 8, both eyes tracked properly, append data to csv
            else:
                #print("EYES: ", eyes, "\n")
             #   append_list_as_row(r"C:\Users\VSalinas\Documents\cs490\90_e1.csv", eyes)
                #print("CHECK4: ", eyes.tolist())

                #uncomment out for csv
                #output.append(eyes.tolist())
                #return output
                appendLocations(output, eyes.tolist())
                return output
    return output


videoOutput = []
parser = argparse.ArgumentParser(description='Code for eye/face tracking.')
# NOTE: if you want to run this on your local machine you'll need to clone this git repo with the haarcascades first
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

# testing our video capture here (face and eye tracking is working, but it's reading the frames too slowly
cap = cv2.VideoCapture("C:/Users/VSalinas/Downloads/203_e2_EyeDemoTrim_AdobeCreativeCloudExpress.mp4") # DO NOT RUN WHEN APPENDING TO CSV

# throws error if the passed in video capture cannot be opened
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)

# keep reading frames until there are no frames left, or the user presses the escape key
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame found, end program.')
        #append_list_as_row(r"C:\Users\VSalinas\Documents\cs490\dataRedo.csv", videoOutput)
        print("OUTPUT: ", videoOutput)
        break

    # passes one frame at a time into the detectAndDisplay function from the passed in video capture
    output = detectAndDisplay(frame)
    videoOutput.append(output)

    # NOTE: 27 is the ASCII value of 'esc' (so think of it as pressing escape)
    # if the escape key is pressed during the video, break (each frame waits 5-milliseconds before the next)
    if cv2.waitKey(1) == 27:
        break
