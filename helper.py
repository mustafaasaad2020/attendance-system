import Utilities
import face_extractor
import face_recognition
import glob
from PIL import Image
import csv
import Student


def get_registered_students_encoded_faces():
    registered_students_faces = []
    encoded_students_faces = []
    for filename in glob.glob('./database/*.jpg'):
        face = face_recognition.load_image_file(filename)
        registered_students_faces.append(face)
    for eachFace in registered_students_faces:
        encoded_students_faces.append(face_recognition.face_encodings(eachFace)[0])
    return encoded_students_faces


def get_present_students_encoded_faces():
    present_students_faces = []
    encoded_present_student_faces = []
    for filename in glob.glob('./attendees/extracted_faces/*.jpg'):
        face = face_recognition.load_image_file(filename)
        present_students_faces.append(face)
    for eachFace in present_students_faces:
        encoded_present_student_faces.append(face_recognition.face_encodings(eachFace)[0])
    return encoded_present_student_faces


def encode_faces(faces):
    encoded_faces = []
    for eachFace in faces:
        height, width, _ = eachFace.shape
        eachFace_location = (0, width, height, 0)
        encoded_faces.append(face_recognition.face_encodings(eachFace, known_face_locations=[eachFace_location])[0])
    print("Total number of encoded faces with replicas : {}".format(len(encoded_faces)))
    return encoded_faces


def get_students_from_database():
    students = []
    with open('./database/registered_students.csv', newline='') as file:
        reader = csv.reader(file)
        for eachRow in reader:
            print('{} {} {}'.format(eachRow[0], eachRow[1], eachRow[2]))
            student = Student.Student(eachRow[0], eachRow[1], eachRow[2])
            students.append(student)
    print("Total number of students in database : {}".format(len(students)))
    return students


def get_students_encoded_faces(students):
    encoded_faces = []
    for student in students:
        encoded_faces.append(student.encoded_face)
    print("Total number of encoded student faces : {}".format(len(encoded_faces)))
    return encoded_faces


def export_attendance_results(attendees, path):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for attendee in attendees:
            writer.writerow([attendee.id, attendee.name, attendee.votes])
