import cv2
import urllib.request
import numpy as np
import time

url = 'http://172.16.1.69:8080/video'

cap = cv2.VideoCapture(url)

start_time = time.time()

# Display the frame rate every one second
report_time = 0.25

frame_count = 0
# Start the frame loop
while True:
    ret, frame = cap.read()
    frame_count += 1

    if (time.time() - start_time) > report_time:
        print("FPS: ", frame_count / (time.time() - start_time))
        frame_count = 0
        start_time = time.time()

cap.release()
out.release()
cv2.destroyAllWindows()