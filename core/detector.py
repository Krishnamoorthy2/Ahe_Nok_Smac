from collections import namedtuple
from utils.utils import get_quardrents, draw
import cv2


# from config import data

PlanarTarget = namedtuple('PlaneTarget', 'image, keypoints, descrs, data')
TrackedTarget = namedtuple('TrackedTarget', 'target, p0, p1, H, quad')


class PlaneDetector:
	def __init__(self, data):
		self.DISTANCE = 0.7
		self.MIN_MATCH_COUNT = 10  # 10
		self.draw = draw
		self.data = data
		self.targets = []
		self.frame_kpts = []
		self.detector = cv2.AKAZE_create(descriptor_size=0, descriptor_channels=3,
										 threshold=0.00001, nOctaves=4, nOctaveLayers=4,
										#  threshold=0.001, nOctaves=4, nOctaveLayers=4,
										 diffusivity=0)#, descriptor_type = AKAZE::DESCRIPTOR_MLDB,
										#  diffusivity=0)#KAZE::DIFF_PM_G2)
		# self.detector = cv2.ORB_create(nfeatures=500)
		# self.detector = cv2.AKAZE_create()
		flann_params = dict(
			# FLANN_INDEX_KDTREE = 1, #1
			algorithm=6,  # FLANN_INDEX_LSH,
			table_number=6,  #  12
			key_size=12,  # 20
			multi_probe_level=1)  #2

		self.matcher = cv2.FlannBasedMatcher(
			flann_params, {})  # bug : need to pass empty dict (#1329)

	def add_marker(self, img_path):  # , data=None):
		'''Add a new tracking target.'''
		image = cv2.imread(img_path, 0)
		raw_points, raw_descrs = self.detect_features(image)
		# print "src : {}".format(len(raw_points))
		img2 = cv2.drawKeypoints(image, raw_points, image)
		# cv2.imshow("descriptors", img2)
		# cv2.waitKey(0)
		self.matcher.add([raw_descrs])
		target = PlanarTarget(
			image=image, keypoints=raw_points, descrs=raw_descrs, data=self.data)
		self.targets.append(target)

	def clear(self):
		'''Remove all targets'''
		self.targets = []
		self.matcher.clear()

	def detect_features(self, frame):
		'''detect_features(self, frame) -> keypoints, descrs'''
		keypoints, descrs = self.detector.detectAndCompute(frame, None)
		#print len(keypoints)

		if descrs is None:  # detectAndCompute returns descs=None if not keypoints found
			descrs = []
			# return 
		return (keypoints, descrs)

	def detect(self, frame, vis):
		'''Returns a list of detected TrackedTarget objects'''
		self.frame_kpts, frame_descrs = self.detect_features(frame)
		# for point in self.frame_kpts:
		#     x, y = point.pt
		#     cv2.circle(vis, (int(x), int(y)), 2, (0, 0, 255), -1) # to debug

		if len(self.frame_kpts) < self.MIN_MATCH_COUNT:
			return []

		matches_mad = self.matcher.knnMatch(frame_descrs, k=2)
		# matches = [
		#     m[0] for m in matches
		#     if len(m) == 2 and m[0].distance < m[1].distance * self.DISTANCE
		# ]

		matches = []
		matches_by_id = [[] for _ in range(len(self.targets))]

		for m in matches_mad:
			if len(m) == 2 and m[0].distance < m[1].distance * self.DISTANCE:
				matches.append(m[0])
				matches_by_id[m[0].imgIdx].append(m[0])

		if len(matches) < self.MIN_MATCH_COUNT:
			return []

		# matches_by_id = [[] for _ in range(len(self.targets))]
		# for m in matches:
		#     matches_by_id[m.imgIdx].append(m)
		#print "match"
		#print len(matches)
		tracked = []
		for imgIdx, matches in enumerate(matches_by_id):
			
			if len(matches) < self.MIN_MATCH_COUNT:
				continue
			target = self.targets[imgIdx]
			p0 = [target.keypoints[m.trainIdx].pt for m in matches]
			p1 = [self.frame_kpts[m.queryIdx].pt for m in matches]

			for m in matches:
				x, y = self.frame_kpts[m.queryIdx].pt
				# cv2.circle(vis, (int(x), int(y)), 2,
						#    (0, 0, 255), -1)  # to debug
			h, w = target.image.shape
			meta_data = get_quardrents(p0, p1, w, h)
			if not meta_data:
				continue
			H, quad = meta_data

			track = TrackedTarget(target=target, p0=p0, p1=p1, H=H, quad=quad)
			tracked.append(track)

		tracked.sort(key=lambda t: len(t.p0), reverse=True)
		# vis = self.draw(vis, tracked)
		return tracked

		# return (tracked, vis)
		# try:
		#     if len(tracked[0].p1) < (len(tracked[0].target.keypoints) * 0.10):
		#         return []
		#     else:
		#         return (tracked, vis)
		# except:
		#     return (tracked, vis)
