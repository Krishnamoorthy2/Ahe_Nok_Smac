import datetime
import traceback

class LogGen(object):
    def __init__(self, name, mode):
        self.LogObject = open("log/"+ name +".txt", mode+"+")
    
    def CreateErrorLog(self, error_log_obj, message):
        time_log = datetime.datetime.now()
        time_log = str(time_log).split('.')[0]
        error_log_obj.write(time_log+" "+message+"\n")