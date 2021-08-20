import cv2
# <<<<<<< Updated upstream
from render.ui import UI

# =======
from utils.config import debug
from center import hardware_handler, traceback
# >>>>>>> Stashed changes



new_width = 980
aspectRatio = 1280/float(new_width)
aspectRatio = 1

class AccessCamera(object):
	def __init__(self,ui_obj, src=0):
		self.timer = None
		self.curr_gray_frame, self.curr_frame = None, None
		self.camera = cv2.VideoCapture(src)
		# shape = (640, 480)
		# shape = (1024, 748) # 720 x 960
		# shape = (1280, 1024)  # 960 x 1280
		shape = (1920, 1080)  # 1080 x 1920
		self.camera.set(3, shape[0])
		self.camera.set(4, shape[1])
		

		self.resize = True
		# self.resize = False

		ret, self.curr_frame = self.camera.read()
		self.dd = self.curr_frame
		if not ret:
			hardware_handler.CreateErrorLog(hardware_handler.LogObject, " <type 'Camera not found'>   File \"camera.py\", line 31, in <module>")
			raise RuntimeError('Where is the Camera?')
		# (h, w) = self.curr_frame.shape[:2]
		# print ("{} * {}".format(h, w))
		self._save_video()
		self.ui_obj= ui_obj
		# self.nokia = nokia

	def _save_video(self, fps=15):
		from time import time
		output = "cam/" + str(time()) + ".mp4"
		fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
		height, width, _ = self.curr_frame.shape
		self.out = cv2.VideoWriter(output, fourcc, fps, (width, height))

	def _access_frame(self):

		self.df = self.dd

		self.timer = cv2.getTickCount()
		ret, self.display_frame1 = self.camera.read()
		# x, y, w, h = 600,300, 600, 700
		# cv2.imshow("display frame ",self.display_frame1)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

		if not ret:
			return False
		self.display_frame = self.display_frame1[155:985, 210:1355]
		# from time import time
		# cv2.imwrite("cam/" + str(time()) + ".jpg", self.curr_frame)
		self.out.write(self.display_frame1)
		# cv2.imshow("display frame 2 ",self.display_frame)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

		# self.curr_frame = self.adjust_gamma(self.curr_frame, gamma=0.75)

		
		if self.resize:
			self.curr_frame = self.image_resize(
				self.display_frame, width=new_width)

		self.display_frame = self.curr_frame

		# (h, w) = self.curr_frame.shape[:2]
		# print ("{} * {}".format(h, w))

		self.curr_gray_frame = cv2.cvtColor(self.curr_frame,
											cv2.COLOR_BGR2GRAY)
		return True
	def image_resize(self, image, width = None, height = None, inter = cv2.INTER_AREA):
		dim = None
		(h, w) = image.shape[:2]

		if width is None and height is None:
			return image

		if width is None:
			r = height / float(h)
			dim = (int(w * r), height)
		else:
			r = width / float(w)
			dim = (width, int(h * r))
		resized = cv2.resize(image, dim, interpolation = inter)
		return resized

	def BGR2RGB(self, img):
		# fps = cv2.getTickFrequency() / (cv2.getTickCount() - self.timer)
		# cv2.putText(img, "fps : " + str(int(fps)), (10, 20),
					# cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
		# a = self.nokia.get_id()
		output=self.ui_obj.draw_img(img)
		return cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
		# return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


	# def status(self,stage):
	#     print("statuscalled")
	#     print type(stage)
	#     if stage == "yes":
	#         print("triggered")
	#         self.ui_obj.trigger_state(1,"error")
	#     elif stage == "no":
	#         self.ui_obj.trigger_state(2,"complete")

	def _release_cam(self):
		self.out.release()
		self.camera.release()


	# def adjust_gamma(self, img , gamma=1.0):
	#     # build a lookup table mapping the pixel values [0, 255] to
	#     # their adjusted gamma values
	#     invGamma = 1.0 / gamma
	#     table = np.array([((i / 255.0) ** invGamma) * 255
	#                 for i in np.arange(0, 256)]).astype("uint8")

	#     # apply gamma correction using the lookup table
	#     return cv2.LUT(img, table)

# import numpy as np
