import cv2
import numpy as np
from time import time
import imutils
from log_generator import ValGen
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time


class ML_model(object):
    def __init__(self, graph_path, label_lines):
        self.start = 0.0
        self.end = 0.0
        self.config = tf.ConfigProto(device_count={'GPU': 0})
        self.label_lines = label_lines

        with tf.gfile.FastGFile(graph_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
        with tf.Graph().as_default() as graph:
            tf.import_graph_def(graph_def, name='')

        self.graph_def = graph

    def main(self, img):
        s = str(time.time())+".jpg"
        self.img_name = s
        cv2.imwrite(s, img)
        try:
            img = tf.gfile.FastGFile(s, 'rb').read()
            with tf.Session(config=self.config, graph=self.graph_def) as sess:
                softmax_tensor = sess.graph.get_tensor_by_name(
                    'final_result:0')
                predictions = sess.run(
                    softmax_tensor, {'DecodeJpeg/contents:0': img})
                top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
                print ("[INFO]  {}- {}%".format(self.label_lines[top_k[0]],
                                                predictions[0][top_k[0]]*100))
                self.acc = (predictions[0][top_k[0]]*100)
                self.score = self.label_lines[top_k[0]] + \
                    " "+str(predictions[0][top_k[0]]*100)
                print("scccccccccccccccccccccccccccc",self.score)
                try:
                    os.remove(s)
                except:
                    pass
                self.end=time.time()
                # print(self.end-self.start)
                return self.label_lines[top_k[0]]

        except:
            pass

class Counter(object):
    def __init__(self, limit):
        self.counter = 0
        self.counter_limit = limit

    def update(self):
        self.counter += 1

    def reset(self):
        self.counter = 0

    def check(self):
        if self.counter < self.counter_limit:
            self.update()
            return False
        elif self.counter >= self.counter_limit:
            self.reset()
            return True

class Trx_Assembly(ML_model,ValGen):
    def __init__(self):
        graph_path = 'station3_new.pb'
        label_lines = [
            "trxtemplate",
            "shield",
            "handshield",
            "nonedc",
            "noneshieldcover",
            "shieldcover",
            "dc",
            "nohandtc",
            "trxassembly",
            "nonetrxtemplate",
            "handtc",
            "nonetrxassembly",
            "noneshield"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        result = self.CreateValidationLog(name ="TRX_ASSEMBLY_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        return result

class DC_Screw_ML(ML_model):
    def __init__(self):
        graph_path = 'dc_screw.pb'
        label_lines = [
            "handscrew",
            "none dcscrew",
            "dc screw"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img):
        return self.main(img)


class DC_Screw(ValGen):
    def __init__(self):
        self.params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        self.params.minThreshold = 3
        self.params.maxThreshold = 255

        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 30
        self.params.maxArea = 60

        # # Filter by Color
        self.params.filterByColor = True
        self.params.blobColor = 0

        # Filter by Circularity
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.5
        # self.params.maxCircularity = 1

        # # Filter by Convexity
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.5

        # # Filter by Inertia
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.5
        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def main(self, img,topic):
        keypoints = self.detector.detect(img)
        self.CreateValidationLog(name ="DC_Screw",message = str(topic)+" "+str(len(keypoints))+"\n")
        ml_result=stage1["DC_Screw_ML"].main(img)
        if not keypoints and ml_result=="dc screw":
               return True         
        else:
            print (len(keypoints))
            return False

class TRX_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'station3.pb'
        label_lines = [
            "nonetrxtemplate",
            "trxtemplate"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="TRX_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        return result

class Screws_S3(Counter,ValGen):
    def __init__(self):
        Counter.__init__(self, limit=2)
        self.screws_pos = {
                1: [31,263], 2: [75,379], 3: [44,401], 4: [112,543], 5:[74,610],
               6: [74,697], 7:[130,693], 8: [189,611], 9: [149,469], 10: [227,263],
               11: [266,380], 12: [300,469], 13: [265,688], 14: [268,746], 15: [345,717],
               16: [421,700], 17: [358,611], 18: [421,551], #19: [425,263], 
            }
        self.result = [0]*19
        
        self.params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        self.params.minThreshold = 3
        self.params.maxThreshold = 255

        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 30
        self.params.maxArea = 60

        # # Filter by Color
        self.params.filterByColor = True
        self.params.blobColor = 0

        # Filter by Circularity
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.5

        # # Filter by Convexity
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.5

        # # Filter by Inertia
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.5
        
        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def blob(self, img):
        keypoints = self.detector.detect(img)
        if keypoints:
            return 0
        else:
            return 1

    def main(self, img,topic):
        self.result = [0]*19
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        placed = []
        for s_id in self.screws_pos.keys():
            [x, y] = self.screws_pos[s_id]
            crop = gray[y-12:y+12, x-12:x+12]
            self.result[s_id-1] = self.blob(crop)
            # print(s_id-1,self.result[s_id-1])

        # 19: [425,263],
        crop = gray[263-12:263+12, 425-12:425+12]
        self.result[19-1] = stage1["S3_19"].main(crop)

        for i in [i for i,x in enumerate(self.result) if x==1]:
            placed.append(i+1)
            self.CreateValidationLog(name ="S3_Screw",message = str(topic)+" "+str(placed)+"\n")
        # print(placed)

        if sum(self.result)==19:
            if self.check():
               return True         
        else:
            self.reset()
            return False

class S3_19(Counter):
    def __init__(self):

        Counter.__init__(self, limit=0)
        self.params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        self.params.minThreshold = 3
        self.params.maxThreshold = 255

        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 30
        self.params.maxArea = 60

        # # Filter by Color
        self.params.filterByColor = True
        self.params.blobColor = 0

        # Filter by Circularity
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.2
        # self.params.maxCircularity = 1

        # # Filter by Convexity
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.2

        # # Filter by Inertia
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.2
        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def main(self, img):
        keypoints = self.detector.detect(img)
        if keypoints:
            print("19 blobbbb")
            return 0  
        else:
            return 1

class ShieldCover_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'shieldcover.pb'
        label_lines = [
            "handshieldcover",
            "noneshieldcover",
            "shieldcover"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="ShieldCover_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        return result

class Station3_adapter_upper(Counter,ValGen):
    def __init__(self):
        Counter.__init__(self, limit=0)
        self.params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        self.params.minThreshold = 5
        self.params.maxThreshold = 255

        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 20
        self.params.maxArea = 50

        # # Filter by Color
        self.params.filterByColor = True
        self.params.blobColor = 0

        # Filter by Circularity
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.3
        # self.params.maxCircularity = 1

        # # Filter by Convexity
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.3

        # # Filter by Inertia
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.008
        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def main(self, img,topic):
        keypoints = self.detector.detect(img)
        self.CreateValidationLog(name ="Adapter_S3",message = str(topic)+" "+str(len(keypoints))+"\n")
        if not keypoints:
            print("no blobb")
            if self.check():
                return True            
        else:
            self.reset()
            return False  
        return False

class Shield_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'shield.pb'
        label_lines = [
            "before shield",
            "after shield",
            "handshield",
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="Shield_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        return result

stage1 = {
    "Trx_Assembly" : Trx_Assembly(),
    "DC_Screw_ML":DC_Screw_ML(),
    "DC_Screw":DC_Screw(),
    "Screws_S3" : Screws_S3(),
    "S3_19" : S3_19(),
    "TRX_ML":TRX_ML(),
    "ShieldCover_ML":ShieldCover_ML(),
    "Station3_adapter_upper":Station3_adapter_upper(),
    "Shield_ML":Shield_ML(),
    }