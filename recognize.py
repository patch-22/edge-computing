import face_recognition
import cv2
import numpy as np
import urllib.request

# Load a sample picture and learn how to recognize it.
sam_image = face_recognition.load_image_file("sam.jpg")
sam_face_encoding = face_recognition.face_encodings(sam_image)[0]

# Load a second sample picture and learn how to recognize it.
gytis_image = face_recognition.load_image_file("gytis.jpg")
gytis_face_encoding = face_recognition.face_encodings(gytis_image)[0]

# Load a sample picture and learn how to recognize it.
adam_image = face_recognition.load_image_file("adam.jpg")
adam_face_encoding = face_recognition.face_encodings(adam_image)[0]

colm_image = face_recognition.load_image_file("colm.jpg")
colm_face_encoding = face_recognition.face_encodings(colm_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    sam_face_encoding,
    gytis_face_encoding,
    adam_face_encoding,
    colm_face_encoding
]
known_face_names = [
    "Sam",
    "Gytis",
    "Adam",
    "Colm"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# 
# 
# while True:
#     
#         cv2.imshow('i', i)
#         if cv2.waitKey(1) == 27:
#             exit(0)

stream = urllib.request.urlopen('http://twinepi.local:8000/stream.mjpg')
bytes = bytes()

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

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

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

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()