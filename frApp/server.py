# -*- coding: utf-8 -*-
from flask import Flask, session, escape, render_template, Response, request, redirect, url_for
import cv2
import os.path
from utils.verify import load_files, videocapture, initVar, gen


app = Flask(__name__)

app.secret_key = 'any random string'

@app.route('/')
def index():
	session['name'] = "noname"
	return render_template('index.html')


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


@app.route('/verify', methods = ['POST', 'GET'])
def verify():
	if 'visits' in session:
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