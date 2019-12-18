# -*- coding: utf-8 -*-
import face_recognition
import cv2
#from pygame import mixer

def load_filesn():
    global video_capture
    global face_locations
    global face_encodings


def videocapturen():
    # Get a reference to webcam #0 (the default one)
    vc =  cv2.VideoCapture(0)
    return vc



def genn(video_capture, process_this_frame=True):

    # Grab a single frame of video
    ret, frame = video_capture.read()
    encodedImage = None
    lgt = 0

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    process_this_frame = not process_this_frame

    frame = cv2.resize(frame,(300,200))
    cv2.imshow('frame', frame)
    cv2.destroyAllWindows()
    # encode the frame in JPEG format
    (flag, encodedImage) = cv2.imencode(".jpg", frame)


    # Dectect number to see face
    if len(face_locations) == 1:
        # For Beep audio
        #mixer.init()
        #mixer.music.load('utils/beep_new.mp3')
        #mixer.music.play()
        lgt = 1

    return encodedImage, frame, lgt

