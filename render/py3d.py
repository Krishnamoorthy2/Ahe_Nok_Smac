#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
from time import time
import pi3d
import pickle
from utils.config import assets_path
import paho.mqtt.publish as publish
import os
import tkinter as tk
import ctypes
from center import ui_handler, traceback

user32 = ctypes.windll.user32
screen_res = str(user32.GetSystemMetrics(0))+" "+str(user32.GetSystemMetrics(1)) 

class pclose:
	status = False

	@classmethod
	def update(cls, value):
		cls.status = value

	def __init__(self, value):
		self.value = value
		self.update(value)

resolution_Dict = {
        "1920 1080" : [29.5, 16.5],
        "1680 1050" : [27.0, 16.55],
        "1600 900" : [29, 16.55],
        "1440 900" : [26.5, 16.5],
        "1400 1050" : [22.5, 17.0],
        "1366 768" : [29.5, 16.5],
        "1360 768" : [29.5, 16.52],
        "1280 1024" : [20.6, 16.5],
        "1280 960" : [22.6, 16.52],
        "1280 800" : [26.5, 16.5],
        "1280 768" : [28.0, 16.5],
        "1280 720" : [29.5, 16.5],
        "1280 600" : [35.5, 16.5],
        "1152 864" : [22.5, 16.5],
        "1024 768" : [22.5, 16.5],
        "800 600" : [22.5, 16.5]
    }

a = 22.5
b = 16.5

if screen_res in resolution_Dict:
	size = resolution_Dict.get(screen_res)
	a = size[0]
	b = size[1]
else:
	pass

screen_res = list(map(int, screen_res.split()))
X,Y = screen_res[0]/2, screen_res[1]/2

X_off = (66 / 1920.0) * 100
X_off = (X_off *  screen_res[0]) / 100
Y_off = (66 / 1080.0) * 100
Y_off = (Y_off *  screen_res[1]) / 100
# print(int(X_off), int(Y_off))
offset = (int(X_off), int(Y_off))

class Interface3d:
	def __init__(self):
		self.wsx, self.wsy = 25, 15
		self.width = 1245
		self.hight = 830
		self.pi3d = pi3d
		self.pickle = pickle
		self.models = {}
		background = (0.0, 0.0, 0.0, 0.0)
		self.pi3d.Light(lightpos=(1.0, 1.0, 0), lightcol=(1.0, 1.0, 0.8), lightamb=(0.5, 0.5, 0.5))
		self.display = self.pi3d.Display.create(background=background, w=None, h=None, x=None, y=None, window_title="", frames_per_second=None)
		self.display.time = time()
		self.shader = {
			"uv_flat":self.pi3d.Shader("uv_flat"),
			"uv_light":self.pi3d.Shader("uv_light"),
		}
		self.mykeys = self.pi3d.Keyboard()
		self.mouse = pi3d.Mouse()
		self.mouse.start()

	def load_obj(self, model_list):
		try:
			for model in model_list:
				model = model_list[model]
				self.models[model.name] = self.pickle.load(open(model.path, "rb"))
		except Exception as e:
			print(e)
			ui_handler.CreateErrorLog(ui_handler.LogObject, str(type(e))+" "+model.name+" "+traceback.format_exc().splitlines()[1])

	def loadChassis(self, station):
		self.models["Chassis_"+str(station)].set_draw_details(self.shader["uv_flat"], [self.pi3d.Texture(assets_path+"Chassis_"+str(station)+"\\base.png", flip=True)])
		self.models["Chassis_"+str(station)].draw()

	def place_screw(self, obj, x, y, angle):
		p2dx, p2dy = (x / self.width), (y / self.hight)
		wpx, wpy = (self.wsx * p2dx), (self.wsy * p2dy)
		opx, opy = (wpx - (self.wsx / 2)), (wpy - (self.wsy / 2))
		if(opy>0.1):
			opy=opy+0.4
		else:
			opy=opy
		opx=opx-1.5
		self.models[obj.name].positionX(opx)
		self.models[obj.name].positionY(-opy)
		self.models[obj.name].rotateIncZ(angle)
		details =[]
		if obj.base:
			details.append(self.pi3d.Texture(obj.base, flip=True))
		if obj.bump:
			details.append(self.pi3d.Texture(obj.bump, flip=True))
		self.models[obj.name].set_draw_details(self.shader[obj.shader], details)
		self.models[obj.name].draw()
		self.models[obj.name].rotateIncZ(-angle)

	def place_img(self, frame):
		sprite = self.pi3d.ImageSprite(frame, self.shader["uv_flat"], w = a, h = b)
		# sprite.rotateIncZ(90)
		# x = -(self.display.width - img.shape[1])/2
		# print (img.shape[1])
		# sprite = self.pi3d.ImageSprite(
		#     img,
		#     self.shader["uv_flat"],
		#     w=20,
		#     h=5, x=0 ,y=0 , z=10)
		sprite.draw()

	def flush_screen(self):
		self.pi3d.screenshot("img1.jpg")
	
	def keyboard_interrupt(self, nokia, rest, tracking):
		x, y = self.mouse.position()
		k = self.mykeys.read()
		m = self.mouse.button_status()
		# print("mouse: "+str(m))
		if k == 137 and tracking:
			nokia._nextStep()
		elif k == 27 :
			nokia._exit()
			self.mykeys.close()
			self.display.destroy()
			return True
		elif m == 9:
			x,y = self.mouse.position()
			# print("x, y: ",x, y)
			if X >= x >= X-offset[0] and Y >= y >= offset[1]:
				nokia._exit()
				self.mouse.stop()
				self.mykeys.close()
				self.display.destroy()
				return True
		self.display._loop_end()
