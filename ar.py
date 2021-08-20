#!/usr/bin/env python
import cv2
from center import start
from entry import startsync,sync,close,nclose
from core.detector import PlaneDetector
from core.tracker import PlaneTracker
from camera.camera import AccessCamera
# from network.publish import ConnectToServer
import glob,json
import argparse
from render.py3d import Interface3d
from nokia import NokiaLogic,trigger,pclose #,Dicts
from utils.utils import place_text
from utils.config import rootDir, testLocal, LocalJson,stat,ServerJson
# from network.text_handler import ContactServer, station_id
import threading
import Object_detection_testing_single as obb
from Object_detection_testing_single import *
from render.ui import UI 
sync()
ap = argparse.ArgumentParser()


LocalJson_obj = LocalJson()
LocalJson_obj.load_local_json()
server_ip = LocalJson_obj.server_ip
station_id = LocalJson_obj.station_id



ap.add_argument("-c", "--cam", required=False,
				help="<Camera Source>")

args = vars(ap.parse_args())

if args["cam"]:
	video_src = args["cam"]
	if len(args["cam"]) == 1:
		video_src = int(args["cam"])
else:
	video_src = 0



class App:
	def __init__(self):
		# ran = 0
		# d = 1	
		self.kill_me= True
		self.REST = None
		# self.REST = ConnectToServer()
		# self.REST.main()
		self.ui_obj=UI()

		# if not testLocal:
		# 	self.server_thread = ContactServer()
		# 	self.server_thread.daemon = True
		self.tracking = False

		self.PI3D = Interface3d()
		self.NOKIA = NokiaLogic(self.PI3D,self.ui_obj, station_id)
		
		# if not testLocal:
		# 	self.server_thread(self.NOKIA)
		# 	self.server_thread.start()
		local_json_file = station_id+".json"

		# if station_id == 1:
		# print("staaaaaaaaaaaaaa",station_id)
		# print("staaaaaatttttttttttttttttttttttt",type(station_id)) ##########################################
		with open(local_json_file, "r") as read_file:
			data = json.load(read_file)
		json_data_obj = ServerJson(data)
		model_data = json_data_obj.get_model()
		self.PI3D.load_obj(model_data)
		msg = json_data_obj.station_msg
		msg_pos = json_data_obj.station_msg_pos
		new_var = (msg, msg_pos)
		client_id = json_data_obj.client_id
		self.NOKIA.pass_data(new_var, client_id)
		step_data = json_data_obj.get_steps()
		self.DETECTOR = PlaneDetector(step_data)
		# model_data = self.server_thread.get_model_data()
		# self.PI3D.load_obj(model_data)

		# msg_data = self.server_thread.get_msg_data()
		# client_id = self.server_thread.get_client_id()
		# self.NOKIA.pass_data(msg_data, client_id)
 
		# step_data = self.server_thread.get_step_data()
		# self.DETECTOR = PlaneDetector(step_data)
 
		self.TRACKER = PlaneTracker()
		if int(station_id) != 1:
			imag_list = sorted(glob.glob(rootDir+str(station_id)+"/*.jpg"))
			# print('(()()()()()()()',imag_list)
			for img_path in imag_list:
				
				self.DETECTOR.add_marker(img_path)

# <<<<<<< Updated upstream
		self.CAM = AccessCamera(self.ui_obj,video_src)

		
# =======
#         self.CAM = AccessCamera(video_src)
		self.msg = "Place The Chassis"
		self.ui_obj.text = "empty"
# >>>>>>> Stashed changes

	def run(self):

		ran = 0
		d = 1		
		while not self.tracking:
			
			self.PI3D.display._loop_begin()

			if not self.CAM._access_frame():
				break
			# if ran == 0:
			# cv2.imshow("ffffff",self.CAM.display_frame)
			# 	ran =1
			cv2.waitKey(0)
			cv2.destroyAllWindows()
			# print(ran)
			if int(station_id) ==1 and d :
				
				ran=ran+1
				# print("FRAME NUMBER",ran,' d ',d)
			
				if (ran %5 == 0) and (d):
					c = obb.ob(self.CAM.curr_frame)
					x = threading.Thread(target=obb.ob,args=(self.CAM.curr_frame,) )
					x.daemon = True
					x.start()
					# obb.ob(self.CAM.curr_frame)
					# print(type(x))
					# print("thrrrrrreaddddddddd",x)	
								
					# print("Returned Value : ",obb.nn)
					if obb.nn == 1 :
						d = 0
						# print('Exited from object detection')
						imag_list = sorted(glob.glob(rootDir+str(station_id)+"/*.jpg"))
						# print('Temp image has been created..........',imag_list)
						for img_path in imag_list:			
							self.DETECTOR.add_marker(img_path)
					# print(" Selected Frame:                        ",ran)				

			found = self.DETECTOR.detect(
				self.CAM.curr_gray_frame, self.CAM.curr_frame)
			# print('=================',type(found))

			if self.kill_me:
				self.ui_obj.text ="chassis"
				self.PI3D.loadChassis(self.ui_obj.station)
			place_text(img=self.CAM.display_frame, msg=self.msg,
					   pos=(20, 900), color=(255, 255, 255))
			self.PI3D.place_img(self.CAM.BGR2RGB(self.CAM.display_frame))

			if self.PI3D.keyboard_interrupt(self.NOKIA, self.REST, self.tracking):
				break
			if (pclose.status==True):
				break

			for tracker_data in found:
				self.NOKIA(tracker_data)  # <----- Nokia interface
				self.TRACKER(tracker_data, self.CAM.curr_gray_frame)

				while True:
					self.kill_me = False
					self.ui_obj.trx = True
					self.msg = "Adjust The Chassis"
					# self.ui_obj.text = "adjust"
					self.PI3D.display._loop_begin()

					if not self.CAM._access_frame():
						break

					meta_data = self.TRACKER.track(self.CAM.curr_frame, self.CAM.curr_gray_frame)

					if not meta_data:
						self.tracking = False
						self.ui_obj.text = "adjust"
						break

					self.tracking = True
					self.ui_obj.text = "empty"

					if(trigger.tracking == False):
						trigger(True)
					else:
						pass
					frame_out = self.NOKIA.main(
						self.CAM.display_frame, meta_data)  # <----- Nokia interface
				

					# print(type(frame_out))  ####################################
						# print("dist",)
					startsync(False)
					self.PI3D.place_img(self.CAM.BGR2RGB(frame_out))

					if self.PI3D.keyboard_interrupt(self.NOKIA, self.REST, self.tracking):
						break
					if (pclose.status==True):
						break
			# while int(station_id) == 1 and d:
				
			# 	ran=ran+1
			# 	print("FRAME NUMBER",ran,' d ',d)
			
			# 	if (ran %5 == 0) and (d):
			# 		# c = obb.ob(self.CAM.curr_frame)
			# 		# x = threading.Thread(target=obb.ob,args=(self.CAM.curr_frame,) )
			# 		# x.daemon = True
			# 		# x.start()
			# 		obb.ob(self.CAM.curr_frame)
			# 		# print(type(x))
			# 		# print("thrrrrrreaddddddddd",x)				
			# 		print("Returned Value : ",obb.nn)
			# 		if obb.nn == 1 :
			# 			d = 0
			# 			print('Exited from object detection')
			# 			imag_list = sorted(glob.glob(rootDir+str(station_id)+"/*.jpg"))
			# 			print('Temp image has been created..........',imag_list)
			# 			for img_path in imag_list:			
			# 				self.DETECTOR.add_marker(img_path)
			# 		print(" Selected Frame:                        ",ran)			

		self.CAM._release_cam()

# import sys
# import os

# if __name__ == '__main__':
# 	if close.startflag == True:
# 		#print "applicationRUN"
# 		video = App()
# 		video.run()
# 	else:
# 		print("Application closed!!!!!!")

# 	# try:
# 	#     video = App()
# 	#     video.run()
# 	# except Exception as e:
# 	#     exc_type, exc_obj, exc_tb = sys.exc_info()
# 	#     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
# 	#     print(exc_type, fname, exc_tb.tb_lineno)
# 	#     return img
