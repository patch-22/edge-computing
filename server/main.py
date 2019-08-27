import cv2
import urllib.request
import numpy as np
import uuid
import time

from recognize import Recognizer

# OPTIONS
PREVIEW = True
STREAM_URL = 'http://172.16.1.174:8080/video'
USE_WEBCAM = True

if USE_WEBCAM:
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(STREAM_URL)

# Initialize the recognization system
recognize = Recognizer()
recognize.load_samples()

# Ignore certain frames to process faster
process_this_frame = True

while True:
    ret, frame = cap.read()
    if ret == True:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]


        if PREVIEW:
            if process_this_frame:
                face_locations, face_names = recognize.recognize(rgb_small_frame)

            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        elif process_this_frame:
                recognize.recognize_threaded(rgb_small_frame)
            
        process_this_frame = not process_this_frame

cap.release()
# out.release()
cv2.destroyAllWindows()

