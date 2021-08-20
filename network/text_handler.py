# from config import client_ip
import paho.mqtt.subscribe as subscribe
import threading
import time
import sys
import argparse

# from network.publish import jsonDump, send#, send1
# from config import server_ip, station_id
# from config import client_ip, server_ip, client_id
import json
import paho.mqtt.publish as publish
from utils.config import LocalJson, ServerJson
from center import network_handler, traceback
import socket

# from camera.camera import AccessCamera
# ap = argparse.ArgumentParser()

# ap.add_argument("-c", "--cam", required=False,
#                 help="<Camera Source>")

# args = vars(ap.parse_args())

# if args["cam"]:
#     video_src = args["cam"]
#     if len(args["cam"]) == 1:
#         video_src = int(args["cam"])
# else:
#     video_src = 0
def get_ip_address():
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.connect(("8.8.8.8", 80))
   return s.getsockname()[0]

client_ip = get_ip_address()

LocalJson_obj = LocalJson()
LocalJson_obj.load_local_json()
server_ip = LocalJson_obj.server_ip
station_id = LocalJson_obj.station_id

# station_msg = LocalJson_obj.station_msg
# station_msg_pos = LocalJson_obj.station_msg_pos


def jsonDump(val_name,val_order_name, img, val_menthod, val_result, reset=False):
    d = dict(val_name=val_name,val_order_name= val_order_name, val_menthod=val_menthod, input=img, val_result=val_result, reset=reset)
    return json.dumps(d)

def reg_data():
    d = dict(client_ip=client_ip, station_id=station_id)
    return json.dumps(d)

# def send(topic, msg):
#     publish.single(topic, msg, hostname=server_ip, qos=2)

# def send(topic, msg):
#     while True:
#         try:
#             publish.single(topic, msg, hostname=server_ip, qos=2)
#             break
#         except Exception as e:
#             # print("Establishing connectivity")
#             time.sleep(0.2)

class UIheader:
    connect = True

    @classmethod
    def update(cls, value):
        cls.connect = value

    def __init__(self, value):
        self.value = value
        self.update(value)

def sendthread(topic, msg):
    try:
        publish.single(topic, msg, hostname=server_ip, qos=2,auth={"username":"smacar","password":"Welc0me3#"})
        UIheader(True)
        return True
        # break
    except Exception as e:
        network_handler.CreateErrorLog(network_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
        UIheader(False)
        return False

        
def send(topic, msg):
    while True:
        try:
            publish.single(topic, msg, hostname=server_ip, qos=2,auth={"username":"smacar","password":"Welc0me3#"})
            break
        except Exception as e:
            network_handler.CreateErrorLog(network_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
            # print(e)

class restrict :
    skip = True

    @classmethod
    def update(cls, value):
        cls.tracking = value

    def __init__(self, value):
        self.value = value
        self.update(value)

class ContactServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # self._stop_event = threading.Event()
        self.cli_id = client_ip
        self.cli_ip = client_ip
        self.subscribe = subscribe
        self.qos = 2
        init_comm_obj = InitCommunication(
            cli_id=client_ip, cli_ip=client_ip, subscribe=self.subscribe)
        init_comm_obj.start()
        init_comm_obj.contact()
        init_comm_obj.join()
        data = init_comm_obj._get_station_data()
        self.json_data_obj = ServerJson(data)
        # self.cam2=AccessCamera(video_src)
        # self.ui_obj=ui_obj
    


    def __call__(self, nokia_obj):
        self.nokia = nokia_obj

    def get_model_data(self):
        return self.json_data_obj.get_model()

    def get_step_data(self):
        return self.json_data_obj.get_steps()

    def get_msg_data(self):
        msg = self.json_data_obj.station_msg
        msg_pos = self.json_data_obj.station_msg_pos
        return (msg, msg_pos)

    def get_client_id(self):
        return self.json_data_obj.client_id

    def run(self):
        while True:
            m = subscribe.simple(self.cli_id, hostname=self.cli_ip,
                                 retained=False, msg_count=1,auth={"username":"smacar","password":"Welc0me3#"})
            m.payload = m.payload.decode('utf-8')
            try:
                d = json.loads(m.payload)
                # print(d)             
                output = d["output"]
                if self.nokia.val_ord == d["val_order"]:
                    # print("validddddddddddddddddddddddddddddd",self.nokia.val_ord,d["val_order"])
                    if (output == "yes"):
                        if restrict.skip == True:
                        # self.ui_obj.trigger_state(self.nokia.get_id(),"complete")
                            self.nokia._nextStep(operation="yes")
                        else:
                            # print("Restricted...!!!")
                            pass
                    elif output == "no":
                        # self.ui_obj.trigger_state(self.nokia.get_id(),"error")
                        self.nokia._nextStep(operation="no")
                        # self.cam2.status("no")
                    elif output == "ignore":
                        self.nokia._nextStep(operation="ignore")
                    elif output == "exit":
                        break
                else:
                    pass
            except Exception as e:
                network_handler.CreateErrorLog(network_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])


class InitCommunication(threading.Thread):
    def __init__(self, cli_id, cli_ip, subscribe):
        threading.Thread.__init__(self)
        self.cli_id = cli_id
        self.cli_ip = client_ip
        self.subscribe = subscribe
        self.kill_me = False
        self.data = None
        self.socket = socket
        self.topic = "Register"
        self.blah = "\|/-\|/-"

    def _get_station_data(self):
        if self.data:
            return self.data
        else:
            network_handler.CreateErrorLog(network_handler.LogObject, " <type 'smacar.json Data Not Available'>   File \"text_handler.py\", line 182, in <module>")
            raise RuntimeError('Json Data Not Available...')

    def contact(self):
        while not self.kill_me:
            msg = reg_data()
            send(topic=self.topic, msg=msg)
            for l in self.blah:
                sys.stdout.write('\r Waiting for Server  ' + l)
                sys.stdout.flush()
                sys.stdout.write('\b')
                time.sleep(0.2)

    def run(self):
        while not self.kill_me:
            # print self.cli_id
            m = self.subscribe.simple(self.cli_id, hostname=self.cli_ip,
                             retained=False, msg_count=1,auth={"username":"smacar","password":"Welc0me3#"})
            self.data = json.loads(m.payload)
            # with open('temp.json', 'w') as outfile:
            #     json.dump(data, outfile)
            # if m.payload == "keepgoing":
            self.kill_me = True