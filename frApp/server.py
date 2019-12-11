# -*- coding: utf-8 -*-
from flask import Flask, session, escape, render_template, Response, request, redirect, url_for
import cv2
import time
from utils.verify import load_files, videocapture, initVar, gen


app = Flask(__name__)

app.secret_key = 'any random string'


@app.route('/')
def index():
	return render_template('index.html')


#def video_feed():
#	return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


def redirect_reponse():
	print('Ok here')


def generate():

    load_files()
    video_capture = None
    video_capture = videocapture()

    process_this_frame = True
    loop2 = 0
    tolerance = 0.50
    dectect = False

    known_face_encodings, known_face_names = initVar()

    while True:
        encodedImage, loop1, name, letgo = gen(video_capture,known_face_encodings,known_face_names,process_this_frame,tolerance)
        loop2 += loop1
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

        if (name != "Unknown") or (loop2 == 5) :
            video_capture.release()
            cv2.destroyAllWindows()
            dectect = True
            break



@app.route('/verify', methods = ['POST', 'GET'])
def verify():
	if 'visits' in session:
		#session['visits'] = session.get('visits') + 1
		session['visits'] = 0
	return render_template('verify.html')


# time.sleep(0.05)

#@app.route('/video_feed')
#def video_feed():
#	obj = generate()
#	print(next(obj))
#	return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

