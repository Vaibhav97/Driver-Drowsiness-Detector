from scipy.spatial import distance as dist
from imutils import face_utils
from threading import Thread

import json ## to send email to the relatives
import requests

import numpy as np
import time
import dlib
import argparse
import imutils
import cv2

def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
 
#threshold
mythresh = 0.25
framecheck = 20

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["/home/dipak/test/shape_predictor_68_face_landmarks.dat"])

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	grayframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	faces = detector(grayframe, 0)

	for face in faces:
		shape = predictor(gray, face)
		shape = face_utils.shape_to_np(shape) 
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0

		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		if ear < EYE_AR_THRESH:
			flag += 1
			print (flag)

			if flag >= framecheck:
				cv2.putText(frame, "Detected ! Open your eyes !", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
					
				API_URL = "https://esiot.000webhostapp.com/sendSinglePush.php"
				data = {'title':'Alert!',
					'message':'Drowsiness Detected',
					'email':'dipak@messedup.in'}
				r = requests.post(url = API_URL, data = data)
				

		else:
			flag = 0

		cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	if key == ord("q"):
		break

cv2.destroyAllWindows()
vs.stop()
