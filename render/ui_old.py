import os
import time

import cv2
import numpy as np
from render.btn import btnlist

from center import ui_handler, traceback
# from network.analytics import restthread
from network.text_handler import UIheader, station_id
from utils.config import LocalJson, ServerJson


LocalJson_obj = LocalJson()
LocalJson_obj.load_local_json()
token = LocalJson_obj.token

if os.name == "nt":  # windows
	mid = "\\"
	front = str(os.getcwd())
	front = front.split('\\')
	s = '\\'
	front = s.join(front) + "\\"
elif os.name == "posix":  # linux
	mid = "/"
	front = ""

ui_path = "data" + mid + "ui" + mid

steps = [10, 6, 10, 5]

class UI():

	def __init__(self):
		# self.current_step = 17
		self.station = int(station_id)
		self.total_steps = steps[self.station-1]
		self.x_offset = 0
		self.y_offset = 55       
		self.progress = ""
		self.frame = 0
		self.active_btns = []
		self.w,self.h = 1920, 1080
		self.id = 1
		self.text = ""
		self.trx = False
		self.flag, self.check = False, False
		self.count = 0
		self.btns = btnlist[self.station-1]
		self.create_activebtns(self.total_steps)

	def draw_ui( self, img, camera_img, img_pos, alpha_range = 1 ):
		source_image = cv2.imread( img + '.png', -1)
		xpos, ypos = img_pos
		y1, y2 = ypos, ypos+source_image.shape[0]
		x1, x2 = xpos, xpos+source_image.shape[1]
		if source_image.shape[2] == 3:
			source_image = cv2.cvtColor(source_image, cv2.COLOR_RGB2RGBA)			
		alpha_s = source_image[:, :, 3] / 255.0
		alpha_l = alpha_range - alpha_s
		for c in range(0,3):
			camera_img[y1:y2, x1:x2, c] = (alpha_s * source_image[:, :, c] + alpha_l * camera_img[y1:y2, x1:x2, c])	
		return camera_img

	def rotate_bound(self,image, angle):
		(h, w) = image.shape[:2]
		(cX, cY) = (w // 2, h // 2)
		M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
		cos = np.abs(M[0, 0])
		sin = np.abs(M[0, 1])   
		nW = int((h * sin) + (w * cos))
		nH = int((h * cos) + (w * sin))
		M[0, 2] += (nW / 2) - cX
		M[1, 2] += (nH / 2) - cY	
		return cv2.warpAffine(image, M, (nW, nH))

	# def get_pivotstep(self):
	# 	flag = False
	# 	try:
	# 		for i in range(len(self.active_btns)):
	# 			if self.active_btns[i]['status'] == "active":
	# 				pivot_step = self.active_btns[i]['step']
	# 				break
	# 		if self.btns[pivot_step]["child"] != 0:
	# 			if self.btns[pivot_step]["child"] <= 8:
	# 				pivot_step = (self.station*10000) + (pivot_step*100) + self.btns[pivot_step]['child']
	# 			else:
	# 				pivot_step = self.active_btns[i+1]['step']
	# 		for i in range(len(self.active_btns)):
	# 			if self.active_btns[i]['step'] == pivot_step:
	# 				flag = True
	# 		if not flag:
	# 			pivot_step = self.get_parent(pivot_step)
	# 		return self.get_currentindex(pivot_step)
	# 	except Exception as e:
	# 		ui_handler.CreateErrorLog(ui_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1]+" "+pivot_step)

	def get_currentindex(self, step):
		for i in range(len(self.active_btns)):
			if self.active_btns[i]['step'] == step:
				return i

	def get_p(self):
		try:
			flag, active = False, False
			for i in range(len(self.active_btns)):
				if self.active_btns[i]['status'] == "active":
					pivot_step = self.active_btns[i]['step']
					active = True
					break
			if active:
				if self.btns[pivot_step]["child"] != 0:
					if self.btns[pivot_step]["child"] <= 8:
						pivot_step = (self.station*10000) + (pivot_step*100) + self.btns[pivot_step]['child']
					else:
						if len(self.active_btns) ==  self.total_steps:
							pivot_step = self.active_btns[i]['step']
						else:
							pivot_step = self.active_btns[i+1]['step']
					for i in range(len(self.active_btns)):
						if self.active_btns[i]['step'] == pivot_step:
							flag = True
					if not flag:
						pivot_step = self.get_parent(pivot_step)
					return self.get_currentindex(pivot_step)
				return self.get_currentindex(pivot_step)
			else:
				return self.get_currentindex(self.total_steps)
		except Exception as e:
			ui_handler.CreateErrorLog(ui_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])

	def draw_img(self,image):
		bg_img = np.zeros((self.h,self.w, 4), np.uint8)
		resized = cv2.resize(image, None, fx=1.306, fy=1.35, interpolation=cv2.INTER_CUBIC)
		resized = cv2.cvtColor(resized, cv2.COLOR_RGB2RGBA)
		bg_img[ self.y_offset:self.y_offset+resized.shape[0],self.x_offset:self.x_offset+resized.shape[1]] = resized
		bg_img[1080-1050:1080, 1920-640:1920] = (240, 240, 240, 0)
		IMAGE_MAIN = bg_img
		if UIheader.connect == False:
			IMAGE_MAIN = self.draw_ui(ui_path + str(self.station) + mid + 'Station 0' + str(self.station) + '- Header_1', bg_img, img_pos=(0, 0),alpha_range=1)
		elif UIheader.connect == True:
			IMAGE_MAIN = self.draw_ui(ui_path + str(self.station) + mid + 'Station 0' + str(self.station) + '- Header', bg_img, img_pos=(0, 0),alpha_range=1)
		if self.flag:
			IMAGE_MAIN = self.draw_ui(ui_path + str(self.station) + mid + 'Station-' + str(self.station) + '-complete_1' , IMAGE_MAIN, ( 0, 1002 ) )
		else:
			IMAGE_MAIN = self.draw_ui(self.btns[ self.id][ 'progress' ] , IMAGE_MAIN, ( 0, 1002 ) )
		try:
			pivot_index = self.get_p()
			# print(pivot_index)
			# print(self.active_btns)
			if pivot_index < 9:
				i = 0
			else:
				i = pivot_index - 10 + 1
			for j in range(10):
				if i < len(self.active_btns):
					if self.active_btns[i]['step'] < 100:					
						if self.active_btns[i]['status'] == 'active':
							pos_x = 1255
							pos_y = ( 95 * (j+1) ) - 31
							
							IMAGE_MAIN = self.draw_ui( self.btns[self.active_btns[i]['step']][self.active_btns[i]['status']], IMAGE_MAIN, (pos_x, pos_y) ,alpha_range=1)
						else:
							pos_x = 1280
							pos_y = ( 95 * (j+1) ) - 31
							IMAGE_MAIN = self.draw_ui( self.btns[self.active_btns[i]['step']][self.active_btns[i]['status']], IMAGE_MAIN, (pos_x, pos_y) )
					else:
						pos_x = 1280
						pos_y = ( 95 * (j+1) ) - 31
						IMAGE_MAIN = self.draw_ui( self.btns[self.active_btns[i]['step']][self.active_btns[i]['status']], IMAGE_MAIN, (pos_x, pos_y) )
				else:
					pass
				i += 1
		except Exception as e:
			ui_handler.CreateErrorLog(ui_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
		return IMAGE_MAIN

	def get_parent(self, step):
		return int((step - self.station*10000)/100)

	def create_activebtns(self, length):
		self.active_btns.append({ 'status' : 'active', 'step' : 1 })
		for i in range(1, length):
			self.active_btns.append({ 'status' : 'inactive', 'step' : i+1 })
	
	def add_substep(self, step, index):
		self.active_btns.insert(index, { 'status' : 'active', 'step' : (self.station*10000) + (step*100) + 1 })
		self.id = self.active_btns[index]['step']

	def add_multisubstep(self, step, index):
		self.active_btns.insert(index, { 'status' : 'active', 'step' : (self.station*10000) + (step*100) + 1 })
		for i in range(1, self.btns[step]['child']):
			self.active_btns.insert(index+i, { 'status' : 'inactive', 'step' : (self.station*10000) + (step*100) + (i+1) })
		self.id = self.active_btns[index]['step']

	def update_substep(self, step, result):
		index = self.get_currentindex(step)
		parent = self.get_parent(step)
		if result == "error":
			self.active_btns[index]['status'] = result
		else:
			if self.active_btns[index]['step'] < (self.station*10000) + (parent*100) + self.btns[parent]['child']:
				self.active_btns[index]['status'] = "active"
				self.active_btns[index]['step'] += 1
				self.id = self.active_btns[index]['step']
			else:
				del self.active_btns[index]
				self.active_btns[index-1]['status'] = "complete"
				if index < self.total_steps:
					self.active_btns[index]['status'] = "active"
					self.id = self.active_btns[index]['step']
				else:
					pass

	def update_multisubstep_Prasanna(self, step, result):
		index = self.get_currentindex(step)
		parent = self.get_parent(step)
		parent_index = self.get_currentindex(parent)
		child_index = index
		if result == "error":
			self.active_btns[index]['status'] = result
		else:
			if self.active_btns[index]['step'] < (self.station*10000) + (parent*100) + self.btns[parent]['child']:
				self.active_btns[index]['status'] = "complete"
				self.active_btns[index+1]['status'] = "active"
				self.id = self.active_btns[index+1]['step']
			else:
				del self.active_btns[child_index+1-self.btns[parent]['child']:child_index+1]
				self.active_btns[parent_index]['status'] = "complete"
				if parent_index+1 < self.total_steps:
					self.active_btns[parent_index+1]['status'] = "active"
					self.id = self.active_btns[parent_index+1]['step']
				else:
					pass

	def update_multisubstep(self, step, result):
		index = self.get_currentindex(step)
		parent = self.get_parent(step)
		if result == "error":
			self.active_btns[index]['status'] = result
		else:
			if self.active_btns[index]['step'] < (self.station*10000) + (parent*100) + self.btns[parent]['child']:
				self.active_btns[index]['status'] = "complete"
				self.active_btns[index+1]['status'] = "active"
				self.id = self.active_btns[index+1]['step']
			elif self.active_btns[index]['step'] == (self.station*10000) + (parent*100) + self.btns[parent]['child']:
				self.active_btns[index]['status'] = "complete"

	def delete_multistep(self, step):
		try:
			child_index = self.get_currentindex(step)
			parent = self.get_parent(step)
			parent_index = self.get_currentindex(parent)
			if step == (self.station*10000) + (parent*100) + self.btns[parent]['child']:
				del self.active_btns[child_index+1-self.btns[parent]['child']:child_index+1]
				self.active_btns[parent_index]['status'] = "complete"
				if parent_index+1 < self.total_steps:
					self.active_btns[parent_index+1]['status'] = "active"
					self.id = self.active_btns[parent_index+1]['step']
				else:
					pass
			else:
				pass
		except Exception as e:
			ui_handler.CreateErrorLog(ui_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])

	def update_mainstep(self, step, result):
		index = self.get_currentindex(step)
		if self.btns[step]['child'] == 0:
			if result == "error":
				self.active_btns[index]['status'] = result
			elif result == "complete":
				self.active_btns[index]['status'] = "complete"
				self.active_btns[index+1]['status'] = "active"
				self.id = self.active_btns[index+1]['step']
		elif self.btns[step]['child'] <= 8:		
			self.add_multisubstep(step, index+1)
		else:
			self.add_substep(step, index+1)