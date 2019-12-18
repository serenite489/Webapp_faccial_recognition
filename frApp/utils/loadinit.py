# -*- coding: utf-8 -*-
import pickle
import os
import face_recognition
import glob

DATA_DIR = "utils/data/"
known_face_encodingsN = []
known_face_namesN = []

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


def picture_encodings(picture):
    box_image = face_recognition.load_image_file("user/"+picture+".jpg")
    box_face_encoding = face_recognition.face_encodings(box_image)[0]
    known_face_encodingsN.append(box_face_encoding)
    known_face_namesN.append(picture)


def create_pickle(name):
    for path in glob.glob('user/*.jpg'):
        filename = path.split('user/')[1].split('.')[0]
        if filename == 'filenew':
            os.rename('user/filenew.jpg', 'user/'+name+'.jpg')
            filename = name
        picture_encodings(filename)

    pickle.dump(known_face_namesN, open(DATA_DIR+"known_face_names.pkl", "wb"))
    pickle.dump(known_face_encodingsN, open(DATA_DIR+"known_face_encodings.pkl", "wb"))






#def set_face_name(name):
    #print("Set known_face_names dict")
#    old_face_name = get_known_face_names()
#    new_face_name = old_face_name.append(name)
#    pickle.dump(new_face_name, open(DATA_DIR+"known_face_names.pkl", "wb"))


#def set_face_encodings(face_enco):
    #print("Set known_face_encodings dict")
#    if len(face_enco) > 0:
    	#print("face_enco Type: \n", type(face_enco))
    	#print("\n\n face_enco: \n", face_enco)
#    	old_face_enco = get_known_face_encodings()
    	#print("\n\n old_face_enco Type: \n", type(old_face_enco))
    	#print("\n\n old_face_enco: \n", old_face_enco)
#    	if old_face_enco != None:
#    		new_face_enco = old_face_enco.append(np.array(face_enco))
#    		pickle.dump(new_face_enco, open(DATA_DIR+"known_face_encodings.pkl", "wb"))

