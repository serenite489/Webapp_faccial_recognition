# -*- coding: utf-8 -*-
from flask import Flask, session, escape, render_template, Response, request, redirect, url_for
import cv2
#import os
#import sys
import os.path
import time
from pygame import mixer
import numpy as np
import face_recognition as fr
from utils.verify import load_files, videocapture, initVar, gen
from utils.newer import load_filesn, videocapturen, genn
from utils.loadinit import get_known_face_encodings, get_known_face_names, picture_encodings, create_pickle


app = Flask(__name__)

app.secret_key = 'any random string'

@app.route('/')
def index():
    session['name'] = "noname"
    return render_template('index.html')


#@app.route('/back')
#def back():
#    os.system('python main.py')
#    time.sleep(6)

def picture_encodings():
    box_image = fr.load_image_file("filenew.jpg")
    box_face_encoding = fr.face_encodings(box_image)
    set_face_encodings(box_face_encoding)


def generate():

    load_files()
    video_capture = None
    video_capture = videocapture()

    process_this_frame = True
    loop2 = 0
    tolerance = 0.50

    known_face_encodings, known_face_names = initVar()

    while True:
        encodedImage, loop1, name, frame = gen(video_capture,known_face_encodings,known_face_names,process_this_frame,tolerance)
        loop2 += loop1
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

        if (name != "Unknown") or (loop2 == 5) :
        	if name != "Unknown":
        		#cv2.imwrite('fileok.jpg', frame)
        		with open('fileok.txt', 'w') as f:
        			f.write(name)
        	if (loop2 == 5) and (name == "Unknown"):
        		cv2.imwrite('filenok.jpg', frame)
        	video_capture.release()
        	cv2.destroyAllWindows()
        	break



def gen_user():

    load_filesn()
    video_capturen = None
    video_capturen = videocapturen()
    encodedImages = None

    process_this_frame = True
    debut = time.time()
    lgts = 0

    while True:
        (encodedImages, frames, lgt) = genn(video_capturen,process_this_frame)
        lgts = lgt
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImages) + b'\r\n')

        fin = time.time()
        dure = fin - debut
        if dure > 5 :
            if lgts == 1:
                cv2.imwrite('filenew.jpg', frames)
                cv2.destroyAllWindows()
                # For Beep audio
                mixer.init()
                mixer.music.load('utils/beep_new.mp3')
                mixer.music.play()
                break



@app.route('/verify', methods = ['POST', 'GET'])
def verify():
#	if 'visits' in session:
        #session['visits'] = session.get('visits') + 1
    return render_template('verify.html')


@app.route('/fileok', methods = ['GET'])
def fileok():
	data = 'noname'
	if os.path.isfile('fileok.txt'):
		with open('fileok.txt') as f:
			data = f.readline()
		os.remove('fileok.txt')
		session['name'] = data.upper()
		return data
	else:
		return '0'


@app.route('/filenok', methods = ['GET'])
def filenok():
	if os.path.isfile('filenok.jpg'):
		os.remove('filenok.jpg')
		return '1'
	else:
		return '0' 


@app.route('/video_feed')
def video_feed():
	return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/dashboard', methods = ['POST', 'GET'])
def dashboard():
	return render_template('dashboard.html', name = session['name'] )


@app.route('/createresponse', methods = ['POST', 'GET'])
def createresponse():
    username = request.form['name']
    create_pickle(username)
    return render_template('createresponse.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/video_new')
def video_new():
    return Response(gen_user(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/filenew', methods = ['GET'])
def filenew():
    if os.path.isfile('filenew.jpg'):
        #picture_encodings()
        #os.remove('filenew.jpg')
        os.rename('filenew.jpg', 'user/filenew.jpg')
        return '1'
    else:
        return '0' 


@app.route('/newregister')
def newregister():
    return render_template('newregister.html')