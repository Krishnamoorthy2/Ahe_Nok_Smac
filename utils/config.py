import collections
import json
import os
from center import network_handler, traceback

debug = True
testLocal = True
stat = 1
# json_file = "nokia.json"

# testLocal = True
# json_file = "test.json"

"""Structure for Payload"""
Data = collections.namedtuple('Data', 'target, p0, p1, H, quad')
Step = collections.namedtuple(
	'Step', 'id, val_name, val_order_name, val_main, ctr_pos_3D, ctr_pos, patch, mask, val_result, val_dur, val_thr, msg, msg_pos, three_d')
Obj = collections.namedtuple('Obj', 'name, path, shaders, init_size')
Obj_prop = collections.namedtuple(
	'Obj_prop', 'name, shader, animation, base, bump')


"""Path for Platform"""
if os.name == "nt":  # windows
	mid = "\\"
	front = str(os.getcwd())
	front = front.split('\\')
	s = '\\'
	front = s.join(front) + "\\"
elif os.name == "posix":  # linux
	mid = "/"
	front = ""

rootDir = "data" + mid + "db_"
assets_path = front + "data" + mid + "asset" + mid

"""UI Assets"""
ui_path = "data" + mid + "asset" + mid + "UI" + mid


# """Load Json for Payload"""
# with open(json_file, "r") as read_file:
#     config_data = json.load(read_file)

# """Load Json for Payload"""
# with open(json_file, "r") as read_file:
#     smacar_client = json.load(read_file)
#     station_id = smacar_client["station_id"]
#     server_ip = smacar_client["server_ip"]


# client_id = config_data["client_id"]
# client_ip = config_data["client_ip"]
# server_id = config_data["server_id"]
# server_ip = config_data["server_ip"]

#prefix
# station_prefix = "station_"
# threed_model_prefix = "3d_model"
# steps_prefix = "steps"

# station_id = station_prefix + config_data["station_id"]

# station_msg = config_data[station_id][0]["station_msg"]
# station_msg_pos = tuple(config_data[station_id][0]["station_msg_pos"])
# station_msg = config_data["station_msg"]
# station_msg_pos = tuple(config_data["station_msg_pos"])

# three_d_data = config_data[station_id][1][threed_model_prefix]
# steps_data = config_data[station_id][2][steps_prefix]
# three_d_data = config_data[threed_model_prefix]
# steps_data = config_data[steps_prefix]


# model_list = {}
# model_properties_list = {}
# data = []

# """3D models to load"""
# for model in three_d_data:
#     model_list[model["name"]] = Obj(name=model["name"], path=assets_path + model["name"] + mid + "object.obj", shaders=None, init_size=(model["init_size"]["x"], model["init_size"]["y"],
#                                                                                                                                          model["init_size"]["z"], model["init_size"]["sx"], model["init_size"]["sy"], model["init_size"]["sz"], model["init_size"]["rx"], model["init_size"]["ry"], model["init_size"]["rz"]))
#     if model["base"]:
#         model["base"] = assets_path + model["name"] + mid + "base.png"
#     if model["bump"]:
#         model["bump"] = assets_path + model["name"] + mid + "bump.png"
#     model_properties_list[model["name"]] = Obj_prop(name=model["name"], shader=model["shader"],
#                                                     animation = model["anmination"],
#                                                     base=model["base"], bump=model["bump"])


# """Steps to validate
# """

# for step in steps_data:
#     three_d = None
#     if not step["val_name"] == "Text":
#         three_d = model_properties_list[step["three_d"]]
#     data.append(
#         Step(
#             id=step["id"],
#             val_name=step["val_name"],
#             val_main=step["val_main"], ctr_pos_3D=step["ctr_pos_3D"],
#             ctr_pos=step["ctr_pos"], patch=step["patch"],
#             mask=step["mask"], val_result=step["val_result"],
#             val_thr=step["val_thr"], val_dur=step["val_dur"],
#             msg=step["msg"], msg_pos=step["msg_pos"],
#             three_d=three_d))

class LocalJson(object):
	def __init__(self):
		self.local_json_file = "smacar.json"
		self.text_json_file = "text.json"
		self.load_local_json()

	def load_local_json(self):
		"""Load Json from local"""
		try:
			with open(self.local_json_file, "r") as read_file:
				smacar_client = json.load(read_file)
				self.station_id = smacar_client["station_id"]
				self.server_ip = smacar_client["server_ip"]
				self.token=smacar_client["token"]

		except:
			network_handler.CreateErrorLog(network_handler.LogObject, " <type 'smacar.json Not Available'>   File \"config.py\", line 117, in <module>")
		self.station_uid = self.station_id
	def text_local_file(self):
		with open(self.text_json_file, "r") as read_file:
			station_text = json.load(read_file)
			self.station = station_text[str("station_"+(self.station_uid))]

				
				
	# 	except:
	# 		network_handler.CreateErrorLog(network_handler.LogObject, " <type 'smacar.json Not Available'>   File \"config.py\", line 117, in <module>")

class ServerJson(object):
	def __init__(self, data):
		self.model_list = {}
		self.model_properties_list = {}
		self.data = []
		self.steps_data = data["steps"]
		self.three_d_data = data["3d_model"]

	# def get_other_info(self, data):
		self.station_msg = data["station_msg"]
		self.station_msg_pos = tuple(data["station_msg_pos"])
		self.version = data["version"]
		self.client_id = data["client_id"]


	def get_model(self):
		"""3D models to load"""
		for model in self.three_d_data:
			self.model_list[model["name"]] = Obj(
				name=model["name"], shaders=None,
				path=assets_path + model["name"] + mid + "object.pkl",
				init_size=(model["init_size"]["x"], model["init_size"]["y"],
				model["init_size"]["z"], model["init_size"]["sx"], model["init_size"]["sy"], model["init_size"]["sz"], model["init_size"]["rx"], model["init_size"]["ry"], model["init_size"]["rz"]))
			if model["base"]:
				model["base"] = assets_path + model["name"] + mid + "base.png"
			if model["bump"]:
				model["bump"] = assets_path + model["name"] + mid + "bump.png"
			self.model_properties_list[model["name"]] = Obj_prop(
				name=model["name"], shader=model["shader"],
				animation=model["anmination"],
				base=model["base"], bump=model["bump"])
		return self.model_list

	def get_steps(self):
		"""Steps to validate"""
		for step in self.steps_data:
			three_d = None
			if not (step["val_name"]).startswith("Text"):
				three_d = self.model_properties_list[step["three_d"]]
			self.data.append(
				Step(
					id=step["id"],
					val_name=step["val_name"],
					val_order_name=step["val_order_name"],
					val_main=step["val_main"], ctr_pos_3D=step["ctr_pos_3D"],
					ctr_pos=step["ctr_pos"], patch=step["patch"],
					mask=step["mask"], val_result=step["val_result"],
					val_thr=step["val_thr"], val_dur=step["val_dur"],
					msg=step["msg"], msg_pos=step["msg_pos"],
					three_d=three_d))


		# del model_properties_list #clean model_properties_list
		return  self.data
