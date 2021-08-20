import cv2
import numpy as np
import math
import base64
import winsound
import threading
from render.ui import ui_path

def rotationAngle(coord):
	a = coord[0]
	b = coord[1]
	x1 = b[0][0] - a[0][0]
	y1 = b[0][1] - a[0][1]
	c = coord[3]
	d = coord[2]
	x2 = d[0][0] - c[0][0]
	y2 = d[0][1] - c[0][1]
	return 90.0 - math.degrees(math.atan2((y1 + y2) / 2.0, (x1 + x2) / 2.0))

from camera.camera import aspectRatio

def get_quardrents(p0, p1, w, h, MIN_MATCH_COUNT=10):
	p0_arr, p1_arr = np.float32((p0, p1))
	H, status = cv2.findHomography(p0_arr, p1_arr, cv2.RANSAC, 3.0)

	# H, status = cv2.findHomography(p0, p1, cv2.LMEDS, 5.0)
	# H = S * H
	status = status.ravel() != 0

	if status.sum() < MIN_MATCH_COUNT:
		return False

	quad = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
	quad = cv2.perspectiveTransform(quad.reshape(1, -1, 2), H).reshape(-1, 2)

	perimeter = cv2.arcLength(quad, True)
	approx = cv2.approxPolyDP(quad, 0.01*perimeter, True)

	if len(approx) == len(quad) and np.allclose(quad.reshape((1, -1)), approx.reshape((1, -1))):
		approx *= aspectRatio
		return (H, approx)
	else:
		return False


def proper_img(img, quard, w, h):
	pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
	M = cv2.getPerspectiveTransform(quard, pts2)
	# return cv2.warpPerspective(img, M, (w, h))
	img = cv2.warpPerspective(img, M, (w, h))
	# from time import time
	# cv2.imwrite("out/" + str(time()) + ".jpg", img)
	return img

def get_patch(img, x, y, w, h, mask):
	# return img[x-w:x+w, y-h:y+h]
	img = img[x-w:x+w, y-h:y+h]
	from time import time
	cv2.imwrite("out/" + str(time()) + ".jpg", img)
	return img

def get_scn_points(x, y, H, offset=2):
	src_pts = np.float32([[x, y]])
	scn_pts = cv2.perspectiveTransform(src_pts.reshape(1, -1, 2),
										H).reshape(-1, 2)[0]
	return (int(scn_pts[0]) - offset, int(scn_pts[1]) - offset)

def draw(img, tracked):
	for tr in tracked:
		cv2.polylines(img, [np.int32(tr.quad)], True, (0, 255, 0), 2)
	return img


def place_text(img, msg="", pos=(210, 120), color=((32, 255, 165))):
	cv2.putText(img, msg, pos, cv2.FONT_HERSHEY_SIMPLEX,
				1.5, color, 3)


# def place_text1(img, msg="Done", pos=(500, 20), color=(50, 170, 50)):
def place_text1(img, msg="Done", pos=(500, 20), color=(255, 255, 255)):
	return cv2.putText(img, msg, pos, cv2.FONT_HERSHEY_SIMPLEX,
				1.25, color, 3)

def encode_img(img):
	_, buffer = cv2.imencode('.jpg', img)
	return base64.b64encode(buffer)

def mse(l):
	# if(self.l == 2):
	err = np.sum((l[0].astype("float") -
					l[1].astype("float")) ** 2)
	err /= float(l[0].shape[0] * l[1].shape[1])
	return err

def beep(status):
	if (status=="right"):
		winsound.PlaySound(ui_path+'correct.wav', winsound.SND_FILENAME)
	elif (status=="wrong"):
		winsound.PlaySound(ui_path+'incorrect.wav', winsound.SND_FILENAME)
	else:
		winsound.PlaySound(ui_path+'complete.wav', winsound.SND_FILENAME)

def alert(status):
	b = threading.Thread(target=beep,args=(status,))
	b.daemon=True
	b.start()