# version 2.0.14
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
import json
import time
import threading
import numpy as np
import cv2
from business.logits import stage1
from log_generator import LogGen
import socket
import traceback

error_handler = LogGen("server_log")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = (s.getsockname()[0])



def jsonDump(output,val_order):
    d = dict(output = output,val_order = val_order)
    return json.dumps(d)

def sendThread(cli_ip, msg="no"):
    try:
        publish.single(cli_ip, msg, qos=2, hostname=cli_ip,auth={"username":"smacar","password":"Welc0me3#"})
    except Exception as e:
        error_handler.CreateErrorLog(error_handler.ErrorLogObject, str(cli_ip)+ " "+str(type(e))+" "+traceback.format_exc().splitlines()[1])
        # print("Establishing connectivity")


def send(cli_ip, msg):
    while True:
        try:
            publish.single(cli_ip, msg, qos=2, hostname=cli_ip,auth={"username":"smacar","password":"Welc0me3#"})
            break
        except Exception as e:
            error_handler.CreateErrorLog(error_handler.ErrorLogObject, str(cli_ip)+ " "+str(type(e))+" "+traceback.format_exc().splitlines()[1])
            # print("Establishing connectivity")
            time.sleep(0.2)


class NokiaLogic(object):
    def __init__(self):
        # self.duration = 15
        self.cnt=0
        self.count = {}

    def _reset_board(self, idx):
        self.count[idx] = 0
    
    def decode_img(self, encoded_data, cli_ip):
        import base64
        nparr = np.fromstring(base64.b64decode(encoded_data), dtype=np.uint8)
        try:
            return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            error_handler.CreateErrorLog(error_handler.ErrorLogObject, str(cli_ip)+ " "+str(type(e))+" "+traceback.format_exc().splitlines()[1])

    def main(self, data, topic):
        val_order_name = data["val_order_name"]
        val_name = data["val_name"]
        val_menthod = data["val_menthod"]
        val_result = data["val_result"]
        # print(("called : {}").format(val_name))
        image = self.decode_img(data["input"],topic)
        obj = stage1[val_name]
        result = getattr(obj, val_menthod)(image,topic)
        # print("result",result)
        if result == val_result:
            send(topic, jsonDump(output ="yes",val_order = val_order_name))
            # print("[INFO] result Yes!!")
        elif result == "no":
            send(topic, jsonDump(output ="no",val_order = val_order_name))
            # print("[INFO] result Cross")
        else:
            send(topic, jsonDump(output ="ignore",val_order = val_order_name))
            # print("[INFO] result No")


class server:
    def __init__(self):
        self.nokia = NokiaLogic()

    def ValidationThread(self,cli_ip, payload, topic):
        print("support thread is start")
        try:
            self.nokia.main(json.loads(payload), cli_ip)
        except Exception as e:
            error_handler.CreateErrorLog(error_handler.ErrorLogObject, str(cli_ip)+ " "+str(type(e))+" "+traceback.format_exc().splitlines()[1])
 
 


    def clientThread(self,cli_ip, cli_id):
        while True:
            try:
                print ("client thread is start")
                m = subscribe.simple(cli_id, hostname=server_ip,
                                    retained=False, msg_count=1, auth={"username":"smacar","password":"Welc0me3#"})
                m.payload = m.payload.decode('utf-8')
                if(m.payload == "isALive"):
                    print("working")
                    try:
                        sendThread(cli_ip, "keepgoing",
                                hostname=cli_id, auth={"username":"smacar","password":"Welc0me3#"})
                    except Exception as e:
                        pass
                elif m.payload == "exit":
                    print("exit command")
                    send(cli_ip, "exit")
                    break
                elif m.payload == "skip":
                    print("skip")
                elif m.payload == "yes":
                    send(cli_ip, "yes")
                else:
                    tmp_thread = threading.Thread(
                        target=self.ValidationThread, args=(cli_ip, m.payload, m.topic))
                    tmp_thread.daemon = True
                    tmp_thread.start()
            except Exception as e:
                error_handler.CreateErrorLog(error_handler.ErrorLogObject, str(cli_ip)+ " "+str(type(e))+" "+traceback.format_exc().splitlines()[1])

    def server_func(self):
        with open('id.json') as f:
            l = json.load(f)
        while True:
            try:
                print ("server main thread is start")
                m = subscribe.simple("Register", hostname=server_ip,
                                    retained=False, msg_count=1, auth={"username":"smacar","password":"Welc0me3#"})
                m.payload = m.payload.decode('utf-8')
                d = json.loads(m.payload)
                print(d['client_ip'],type(d['client_ip']))
                clientip_split = d['client_ip'].split(".")
                if d['client_ip'] in l:
                    cli_id = l[(d["client_ip"])]
                    cli_ip = d["client_ip"]
                    a = (d['station_id'])
                    a = (a+".json")
                    with open(a) as f:
                        data = json.load(f)
                    data['client_id'] = cli_id
                    sendThread(d['client_ip'], msg=json.dumps(data))
                    thr = threading.Thread(
                        target=self.clientThread, args=(cli_ip, cli_id))
                    thr.daemon = True
                    thr.start()
                else:
                    id_data = {str(d['client_ip']): str(clientip_split[3])}
                    l.update(id_data)
                    with open("id.json","w") as Jfile:
                        json.dump(l, Jfile)
            except Exception as e:
                error_handler.CreateErrorLog(error_handler.ErrorLogObject, str(cli_ip)+ " "+str(type(e))+" "+traceback.format_exc().splitlines()[1])

if __name__ == '__main__':
    d = server()
    d.server_func()
    error_handler.ErrorLogObject.close()