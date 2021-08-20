import cv2
import numpy as np
from utils.utils import get_scn_points
from render.ui import ui_path


class UI_Container(object):
	def __init__(self, _id, w, h, margin, padding):
		self.id = _id
		self.width = 1920
		self.hight = 1080
		self.state = None
		self.container = np.zeros((self.hight, self.width, 3), np.uint8)
	
	def _reset(self):
		self.container = np.zeros((self.hight, self.width, 3), np.uint8)

	def place(self, img, pos=False):
		x_offset, y_offset = pos
		y1, y2 = y_offset, y_offset + img.shape[0]
		x1, x2 = x_offset, x_offset + img.shape[1]
		alpha_s = img / 255.0
		alpha_l = 1.0 - alpha_s
		for c in range(0, 3):
			self.container[y1:y2, x1:x2, c] = (alpha_s * img[:, :, c] +	alpha_l * self.container[y1:y2, x1:x2, c])

class DrawImage():
	def __init__(self):
		self.font = cv2.FONT_HERSHEY_SIMPLEX
		self.alpha = 1
		self.first = True
		self.flag = (204,204,204)
		self.i = 0
		self.arrow = {
			"Text_barcode" : {"temp" : [2, 3], "offset_h" : [70, 0], "offset_t" : [12, 0]},
			"Text_connectors" : {"temp" : [1, 2],"offset_h" : [0,70], "offset_t" : [0, 12]},
			"Text_PA" : {"temp" : [1, 2], "offset_h" : [0, 70], "offset_t" : [0, 12]}
		}
		self.screws = {
			"1" : {
				11001: [222, 55, -25, 0], 11002: [243, 55, 15, 0], 11003: [238, 107, 15, 15], 11004: [226, 164, 15, 15], 11005: [242, 286, 7, -15], 
				11006: [219, 286, -7, -15], 11007: [146, 286, 0, -15], 11008: [124, 286, -20, -15], 11009: [127, 164, 15, 15], 11010: [142, 107, 15, 15], 
				11011: [145, 55, 15, 0], 11012: [124, 55, -37, 0], 11013: [318, 55, -37, 0],11014: [342, 55, 15, 0], 11015: [334, 107, 15, 15], 
				11016: [324, 164, 15, 15], 11017: [315, 286, -25, -15], 11018: [340, 286, -5, -15], 11019: [48, 286, -30, -15], 11020: [46, 107, -30, 25], 
				11021: [47, 55, -30, -15], 11022: [415, 55, 15, -10], 11023: [420, 164, 15, -10], 11024: [415, 286, 15, -15]
			},
			"3" : {
				30401: [31, 263, 10, 10], 30402: [75, 379, 10, 10], 30403: [44, 401, 10, 10], 30404: [112, 543, 10, 10], 30405: [74, 610, 10, 10], 
				30406: [74, 697, 10, 10], 30407: [130, 693, 10, 10], 30408: [189, 611, 10, 10], 30409: [149, 469, 10, 10], 30410: [227, 263, 10, 10], 
				30411: [266, 380, 10, 10], 30412: [300, 469, 10, 10], 30413: [265, 688, 10, 10], 30414: [268, 746, 10, 10], 30415: [345, 717, 10, 10], 
				30416: [421, 700, 10, 10], 30417: [358, 611, 10, 10], 30418: [421, 551, 10, 10], 30419: [425, 263, 10, 10]
			},
			"4" : { 
				40301: [276, 14, 10, 10], 40302: [140, 720, 10, 10], 40303: [24, 714, 10, 10], 40304: [27, 602, 10, 10], 40305: [27, 492, 10, 10], 
				40306: [27, 383, 10, 10], 40307: [27, 272, 10, 10], 40308: [27, 160, 10, 10], 40309: [27, 30, 10, 10], 40310: [90, 14, 10, 10], 
				40311: [179, 14, 10, 10], 40312: [364, 14, 10, 10], 40313: [431, 36, 10, 10], 40314: [429, 163, 10, 10], 40315: [429, 272, 10, 10], 
				40316: [426, 383, 10, 10], 40317: [426, 492, 10, 10], 40318: [426, 602, 10, 10], 40319: [426, 710, 10, 10], 40320: [322, 720, 10, 10], 
				40321: [254, 720, 10, 10]
            }
		}

	def __call__(self, width, hight):
		if self.first:
			self.width, self.hight = width, hight
			self.first = False
			self.img_overlay = np.zeros((hight, width, 3), np.uint8)
			self.pts2 = np.float32([
				[0, 0],
				[width, 0],
				[width, hight],
				[0, hight]
			])
	
	def _blink(self, color):
		if self.i == 1:
			self.i = 0
			return (204, 204, 204)
		else:
			self.i = 1
			return color

	def clear_img(self):
		self.img_overlay = np.zeros((self.hight, self.width, 3), np.uint8)

	def _line(self, line_pts):
		len_line_pts = len(line_pts)
		for idx in range(len_line_pts):
			if idx < (len_line_pts - 1):
				cv2.line(self.img_overlay, line_pts[idx], line_pts[idx + 1], (255, 0, 0), 5)

	def _circle(self, o=(0, 0), colour=(0, 255, 0)):
		cv2.circle(self.img_overlay, o, 13, colour, -1)

	def _rectangle(self, top_left, bottom_right, colour=(0, 255, 0)):
		if self.i <= 1:
			cv2.rectangle(self.img_overlay, top_left, bottom_right, self.flag, 10)
			self.flag = (165,77,25)
			self.i += 1
		else:
			cv2.rectangle(self.img_overlay, top_left, bottom_right, self.flag, 10)
			self.flag = (204,204,204)
			self.i = 0

	def _text(self, msg="", x_y=(0,0)):
		x, y =x_y
		cv2.putText(self.img_overlay, msg, (x-9,y+5), self.font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
	
	def screw_display(self, x, y, current, lines_pts):
		self._line(lines_pts[current])
		self._circle(o=(x, y))
		self._circle(o=(x, y))
		self._text(msg=str(current), x_y=(x, y))
		self._text(msg=str(current), x_y=(x, y))

	def on_scn(self, scn_img, H, quad, color):
		quad = np.array(quad, np.int32)
		quad = quad.reshape((-1, 1, 2))
		return cv2.polylines(scn_img, [quad], True, color, 5)

	def on_scn_arrow(self, img, val_name, H, pos, quad, color):
		pt1, pt2 = pos[self.arrow[val_name]["temp"][0]], pos[self.arrow[val_name]["temp"][1]]
		x = int((pt1[0] + pt2[0])/2)
		y = int((pt1[1] + pt2[1])/2)
		tail_x, tail_y = get_scn_points(x+self.arrow[val_name]["offset_t"][0], y+self.arrow[val_name]["offset_t"][1], H, offset=0)
		head_x,head_y = get_scn_points(x+self.arrow[val_name]["offset_h"][0], y+self.arrow[val_name]["offset_h"][1], H, offset=0)
		img = cv2.arrowedLine(img, (head_x, head_y), (tail_x, tail_y), (42,212,255), 8, tipLength=0.5)
		return self.on_scn(img, H, quad, color)

	def on_scn_place_screws(self, scn_img, H, quad, color, station_id, cur_id):
		screw_pos = self.screws[station_id]
		if cur_id == 2:
			screw_pos = {1:[368, 729, 0, 0], 2:[385, 743, 0, 0]}
		for screw in screw_pos.keys():
			x, y, ox, oy = screw_pos.get(screw)
			x, y = get_scn_points(x, y, H, offset=0)
			scn_img = cv2.circle(scn_img, (x, y), 10, color, 3)		
		return scn_img

	def on_scn_template(self, scn_img, H, cur_id, station_id, color):
		extra = {11013:{2:[124,25],3:[318,25]}, 11019:{2:[340,306],3:[48,306]}, 11022:{2:[47,0],3:[415,0]},
				40312:{2:[179,4],3:[364,4]}}
		screw_pos = self.screws[station_id]
		on_scn_pos = {}
		put_text = {}
		new = {}
		for screw in screw_pos.keys():
			hx,hy, ox, oy = screw_pos.get(screw)
			x, y = get_scn_points(hx, hy, H, offset=0)
			tx, ty = get_scn_points(hx+ox, hy+oy, H, offset=0)
			on_scn_pos[screw] = [x, y]
			put_text[screw] = [tx, ty]

		for pos in screw_pos.keys():
			if pos <= cur_id:
				self.line = (0, 255, 0)
				self.blob = (255, 0, 0)
			else:
				self.line = (37, 57, 30)
				self.blob = (0, 255, 255)
			if pos in extra.keys():
				new[1] = (on_scn_pos[pos-1][0],on_scn_pos[pos-1][1])
				new[2] = (get_scn_points(extra[pos][2][0], extra[pos][2][1], H, offset=0))
				new[3] = (get_scn_points(extra[pos][3][0], extra[pos][3][1], H, offset=0))
				new[4] = (on_scn_pos[pos][0],on_scn_pos[pos][1])
				for item in range(1,4):
					cv2.line(scn_img, new[item], new[item+1], self.line, 2)
			elif (pos-1) in screw_pos.keys():
				cv2.line(scn_img,(on_scn_pos[pos-1][0], on_scn_pos[pos-1][1]),(on_scn_pos[pos][0], on_scn_pos[pos][1]),self.line,2)
			else:
				pass
			cv2.circle(scn_img, (on_scn_pos[pos][0], on_scn_pos[pos][1]), 6, self.blob, -1)
			cv2.putText(scn_img,str(pos-min(self.screws[station_id])+1),(put_text[pos][0], put_text[pos][1]),\
						 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
		if cur_id not in [10, 4, 3]:
			cv2.circle(scn_img, (on_scn_pos[cur_id][0], on_scn_pos[cur_id][1]), 10, color, 2)
		return scn_img

from camera.camera import aspectRatio

scale = aspectRatio
S = [[1, 1, scale],
		[1, 1, scale],
		[1/scale, 1/scale, 1]]