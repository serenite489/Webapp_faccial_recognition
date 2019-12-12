# -*- coding: utf-8 -*-
import pickle
import numpy as np
import os
import face_recognition
import cv2
from pygame import mixer
from utils.loadinit import get_known_face_encodings, get_known_face_names

known_face_encodings = None
known_face_names = None

def load_files():
    global known_face_encodings
    global known_face_names
    global video_capture
    global face_locations
    global face_encodings
    global face_names


def videocapture():
    # Get a reference to webcam #0 (the default one)
    vc =  cv2.VideoCapture(0)
    return vc


def initVar():
    known_face_encodings = get_known_face_encodings()
    known_face_names = get_known_face_names()

    return known_face_encodings, known_face_names


def gen(video_capture,known_face_encodings,known_face_names,process_this_frame=True,tolerance=0.50):

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    loop = 0

    color = (0, 0, 255)
    name = "Unknown"
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Dectect number to see face
        if len(face_locations) > 0:
            loop = 1

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance)

            # Or instead, use the known face with the smallest distance to the new face
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

        if name != "Unknown":
            color = (0, 255, 0)
            # For Beep audio
            mixer.init()
            mixer.music.load('utils/beep.mp3')
            mixer.music.play()
                
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        

    frame = cv2.resize(frame,(300,200))
        
    cv2.imshow('frame', frame)
    cv2.destroyAllWindows()

    # encode the frame in JPEG format
    (flag, encodedImage) = cv2.imencode(".jpg", frame)


    return encodedImage, loop, name, frame

