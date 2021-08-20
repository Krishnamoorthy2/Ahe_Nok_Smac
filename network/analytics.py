from utils.config import LocalJson
import requests
import json
import threading
from center import network_handler, traceback


LocalJson_obj = LocalJson()
LocalJson_obj.load_local_json()
token = LocalJson_obj.token

def restsupport(step,payload):
    if(step=="mainstep"):
        url="https://qa.smacar.com/nokia/api2/?function=mainstep" #global
        # url="http://10.4.11.37/api2/?function=mainstep" #local
        try:
            r = requests.post(url, data=(payload))
        except Exception as e:
            network_handler.CreateErrorLog(network_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
        #print (r.json())
    else:
        url="https://qa.smacar.com/nokia/api2/?function=substep" #global
        # url="http://10.4.11.37/api2/?function=substep" #local
        try:
            r = requests.post(url, data=(payload))
        except Exception as e:
            network_handler.CreateErrorLog(network_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
        
        #print (r.json())
   
def restthread(step,payload):
    c = threading.Thread(target=restsupport,args=(step,payload,))
    c.daemon=True
    c.start()