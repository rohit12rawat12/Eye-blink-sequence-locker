import cv2
import dlib
import numpy as np
import time
from check import check

cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat/shape_predictor_68_face_landmarks.dat")
L_time1 = time.time()
R_time1 = time.time()
userInput = '0'

def distance(point_1, point_2): # function to find distance between two points
	dis = ((point_2[0] - point_1[0])**2 + (point_2[1] - point_1[1])**2)**0.5
	return dis

def eyeRatio(eyePts): # function to find eye ratio
		mid_point_upper = (int((eyePts[1][0] + eyePts[2][0])/2), int((eyePts[1][1] + eyePts[2][1])/2))
		mid_point_lower = (int((eyePts[4][0] + eyePts[5][0])/2), int((eyePts[4][1] + eyePts[5][1])/2))

		eye_horizontal_lenght = distance(eyePts[0], eyePts[3])
		eye_vertical_lenght = distance(mid_point_upper, mid_point_lower)

		eye_ratio = eye_horizontal_lenght / eye_vertical_lenght
		return eye_ratio


while True:
	ret, frame = cap.read()

	if not ret:
		break

	frame = cv2.flip(frame, 1)
	# converting to gray frame
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	# detecting faces
	faces = detector(gray_frame)
	for face in faces:
		landmarks = predictor(gray_frame, face)

		left_eye = []
		right_eye = []
		for i in range(36, 42):
			x = landmarks.part(i).x
			y = landmarks.part(i).y
			left_eye.append([x, y])

		for i in range(42, 48):
			x = landmarks.part(i).x
			y = landmarks.part(i).y
			right_eye.append([x, y])

		left_eye = np.array(left_eye)
		right_eye = np.array(right_eye)

		cv2.polylines(frame, [left_eye], True, (0, 0, 255), 1)
		cv2.polylines(frame, [right_eye], True, (0, 0, 255), 1)

		# left eye ratio
		left_eye_ratio = eyeRatio(left_eye)

		#right eye ratio
		right_eye_ratio =eyeRatio(right_eye)

		if left_eye_ratio < 5:
			L_time1 = time.time()
		else:
			L_time2 = time.time()
			if L_time2 - L_time1 >= 1:
				userInput += 'L'
				print(userInput)
				L_time1 = time.time()

		if right_eye_ratio < 5:
			R_time1 = time.time()
		else:
			R_time2 = time.time()
			if R_time2 - R_time1 >= 1:
				userInput += 'R'
				print(userInput)
				R_time1 = time.time()

	cv2.imshow("frame", frame)
	key = cv2.waitKey(1)
	if key == ord('r'):
		userInput = '0'
	if key == 27:
		break;

cap.release()
cv2.destroyAllWindows()

print("User's Input : " + userInput)
if check(userInput):
	print("Correct Password")
else:
	print("Incorrect Password")
