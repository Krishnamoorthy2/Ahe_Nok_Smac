import datetime
import os

class LogGen(object):
    def __init__(self, name):
        self.ErrorLogObject = open("log/"+ name +".txt", "w+")

    def CreateErrorLog(self, error_log_obj, message):
        time_log = datetime.datetime.now()
        time_log = str(time_log).split('.')[0]
        error_log_obj.write(time_log+" "+message+"\n")

class ValGen(object):
    def CreateValidationLog(self,name,message):
        if os.path.exists("log/"+ name +".txt"):
            # print(int(os.path.getsize("log/"+ name +".txt")))
            if int(os.path.getsize("log/"+ name +".txt")) > 1048576:
                os.remove("log/"+ name +".txt")
        else:
            pass
            # print("file not exist")
        self.write_file(name,message)

                
    def write_file(self,name,message):
        time_log = datetime.datetime.now()
        time_log = str(time_log).split('.')[0]
        with open("log/"+ name +".txt", "a+") as f:
            f.write(time_log+" "+str(message))      