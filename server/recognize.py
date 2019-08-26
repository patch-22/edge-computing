from threading import Thread
import uuid
import face_recognition
import numpy as np

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
        files = ['server/data/sam.jpg', 'server/data/gytis.jpg', 'server/data/adam.jpg', 'server/data/colm.jpg']
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
        
        # print(local_names)
        print('Recognized: {}'.format(local_names), end='\r')
        return face_locations, local_names
