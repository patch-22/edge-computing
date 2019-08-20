import face_recognition
import cv2
import urllib.request
import numpy as np
import uuid
from threading import Thread

class Recognizer:
    def __init__(self):
        self.encodings = []
        self.names = []
        
        # Manage Multithreading
        self.threads = []


    def train(self, encoding, name=str(uuid.uuid4())):
        self.encodings.append(encoding)
        self.names.append(name)

    def load_samples(self):
        files = ['data/sam.jpg', 'data/gytis.jpg', 'data/adam.jpg', 'data/colm.jpg']
        names = ['Sam', 'Gytis', 'Adam', 'Colm']


        # Get the images
        for idx, location in enumerate(files):
            # Assumes one person is in the recognition image
            image = face_recognition.load_image_file(location)
            encoding = face_recognition.face_encodings(image)[0]

            self.train(encoding, names[idx])

    def recognize_threaded(self, frame):
        process = Thread(target=self.recognize, args=[frame])
        process.start()

        self.threads.append(process)

    def recognize(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        local_names = []

        for encoding in face_encodings:
            # See if the face matches known face(s)
            matches = face_recognition.compare_faces(self.encodings, encoding)
            name = 'Unknown'

            face_distances = face_recognition.face_distance(self.encodings, encoding)
            if len(face_distances) != 0:
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = self.names[best_match_index]
            
            local_names.append(name)
        
        print(local_names)
        return face_locations, local_names


STREAM_URL = 'http://192.168.1.12:8080/video'

bytes = bytes()
stream = urllib.request.urlopen(STREAM_URL)

recognize = Recognizer()
recognize.load_samples()

process_this_frame = True
preview = False
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]


        if preview:
            # Only process every other frame of video to save time
            if process_this_frame:
                face_locations, face_names = recognize.recognize(rgb_small_frame)

            process_this_frame = not process_this_frame


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
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            if process_this_frame:
                recognize.recognize_threaded(rgb_small_frame)
            
            process_this_frame = not process_this_frame

cv2.destroyAllWindows()