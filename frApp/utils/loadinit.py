# -*- coding: utf-8 -*-
import pickle
import os


DATA_DIR = "utils/data/"

def get_known_face_encodings():
    #print("Loading known_face_encodings dict")
    with open(os.path.join(DATA_DIR, 'known_face_encodings.pkl'), 'rb') as input:
        known_face_encodings = pickle.load(input)
    return known_face_encodings

def get_known_face_names():
    #print("Loading known_face_names dict")
    with open(os.path.join(DATA_DIR, 'known_face_names.pkl'), 'rb') as input:
        known_face_names = pickle.load(input)
    return known_face_names

