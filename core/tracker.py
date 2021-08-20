import cv2
import numpy as np

from utils.utils import get_quardrents


class PlaneTracker(object):
	def __init__(self):
		self.lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(
			cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
		self.get_quardrents = get_quardrents
		self.TRACKING_RATION = 0.75
		self.MEASURE_ERROR = 0.75

	def __call__(self, tracker_data, gray_frame):
		self.curr_pts, self.tracks = tracker_data.p0, tracker_data.p1
		self.curr_gray_frame = gray_frame
		self.h, self.w = tracker_data.target.image.shape
		self.number_good_pts = float(len(self.curr_pts))

	def track(self, vis, next_gray_frame):
		img0, img1 = self.curr_gray_frame, next_gray_frame

		p0_arr = np.float32([tr for tr in self.tracks]).reshape(-1, 1, 2)
		p1, st, err = cv2.calcOpticalFlowPyrLK(
			img0, img1, p0_arr, None, **self.lk_params)
		p0r, st, err = cv2.calcOpticalFlowPyrLK(
			img1, img0, p1, None, **self.lk_params)

		d = abs(p0_arr - p0r).reshape(-1, 2).max(-1)
		good = d < self.MEASURE_ERROR  # 1 # magic number ?
		# print "good"
		# print sum(good)
		if sum(good) / self.number_good_pts <= self.TRACKING_RATION:  # magic number 0.75 ?
			# print "*tracking ration {}".format(sum(good) / self.number_good_pts)
			return False

		# print "tracking ration {}".format(sum(good) / self.number_good_pts)
		old_pts_updated, new_tracks = [], []

		for good_old_pts, (x, y), good_flag in zip(self.curr_pts,
												   p1.reshape(-1, 2), good):
			if not good_flag:
				continue
			old_pts_updated.append((good_old_pts))
			# if len(tr) > self.track_len:
			#     del tr[0]
			new_tracks.append((x, y))
			# cv2.circle(vis, (x, y), 2, (0, 255, 0), -1) # to debug

		self.curr_pts, self.tracks = old_pts_updated, new_tracks
		self.curr_gray_frame = next_gray_frame

		return self.get_quardrents(old_pts_updated, new_tracks, self.w, self.h)
		# H, quad = get_quardrents(old_pts_updated, new_tracks, self.w, self.h)
		# return (H, quad)
		# return (meta_data)
		# vis = self._draw_track(vis, quad) 
	
