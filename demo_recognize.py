import face_recognition

sam_image = face_recognition.load_image_file('sam.jpg')
sam_face_encoding = face_recognition.face_encodings(sam_image)

print(len(sam_face_encoding[0]))