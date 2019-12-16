import sys
import datetime as dt
from time import sleep
import os
import face_recognition
import argparse
import pickle
import cv2
import requests, json
import datetime as dt
import time
import subprocess


ap = argparse.ArgumentParser()
ap.add_argument("-m", "--method", type=int, default='hog',
	help="method of detection - CNN or HOG")


args = vars(ap.parse_args())
# Variable for counting frames after face is detected
facecount = 0

# Declare endpoint url for post request
endpoint_url = 'http://httpbin.org/post'


# haarcascade
cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

# load the known faces and embeddings
print("hr.ai is loading weights...")
data = pickle.loads(open("encodings.pickle", "rb").read())
print("weights have been loaded...")


video_capture = cv2.VideoCapture(0)
anterior = 0
prevTime = 0
while True:
    if not video_capture.isOpened():
        print('Unable to load camera.')
        sleep(5)
        pass
    curTime = time.time()
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Increasing "facecount" variable for every frame during the time face is detected
    facecount += 1


    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
       cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
       #cv2.imshow('Video', frame)


     # If face(s) is/are present on the 20th frame, saving it to an array,
     # and passing it to face recognition module
    
    if facecount%20 == 0 and len(faces) != 0:
       
        start = time.time()

        # load the array of detected faces and convert it from BGR to RGB
        rgb = frame


        # detect the (x, y)-coordinates of the bounding boxes corresponding
        # to each face in the input image, then compute the facial embeddings
        # for each face
        boxes = face_recognition.face_locations(rgb, model=args['method'])
        encodings = face_recognition.face_encodings(rgb, boxes)

        # initialize the list of names for each face detected
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number of votes
                name = max(counts, key=counts.get)
                print(counts)
            # update the list of names
            names.append(name)
            print(name)
            # end
        # loop over the recognized faces
        # for ((top, right, bottom, left), name) in zip(boxes, names):
        # 	# draw the predicted face name on the image
        # 	cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
        # 	y = top - 15 if top - 15 > 15 else top + 15
        # 	cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
        # 		0.75, (0, 255, 0), 2)

        # endtime for recognition time check
        end = time.time()

        #dump json with array of recognized faces and current DateTime
        json_dump = json.dumps({'Recognized':names, 'DateTime':str(dt.datetime.now())})
        r = requests.post(endpoint_url, json_dump)
        #print(json_dump)

        print("Recognition took ", end-start, "seconds")

        facecount = 0

    if anterior != len(faces):
        anterior = len(faces)

    sec = curTime - prevTime
    prevTime = curTime
    fps = 1 / (sec)
    string = 'FPS: %2.3f' % fps
    text_fps_x = len(frame[0]) - 150
    text_fps_y = 20
    cv2.putText(frame, string, (text_fps_x, text_fps_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 0), thickness=1, lineType=2)

    # Display the resulting frame
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Clearing memory from "facecount" value after every half hour
    if facecount >= 18000:
        facecount = 0



# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
