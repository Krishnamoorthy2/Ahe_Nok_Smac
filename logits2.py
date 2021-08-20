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

class Gasket_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'station2.pb'
        label_lines = [
            "crosshs",
            "washernone",
            "hs",
            "handhs",
            "gasketnone",
            "gaskethand",
            "gasket",
            "washer",
            "handwasher"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="Gasket_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        if result == "gasket":
            return True
        else:
            return False

class Adapter_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'adapter.pb'
        label_lines = [
            "adapupper",
            "adaplower",
            "noneupper",
            "nonelower",
            "adaphand"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result=self.main(img)
        self.CreateValidationLog(name ="Adapter_S2_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        if result == "adaphand":
            return True
        else:
            return False

class FilterTower(Counter,ValGen):
    def __init__(self):
        Counter.__init__(self, limit=0)
        self.lower_black = np.array([0, 0, 0])
        self.upper_black = np.array([180, 255, 50])
        
    def main(self, img,topic):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11, 11), 0)
        (_, thresh) = cv2.threshold(blur, 127, 255, cv2.THRESH_TRUNC)
        circles = cv2.HoughCircles(
            thresh, cv2.HOUGH_GRADIENT, 2, 100, param1 = 50, param2 = 30, minRadius = 10, maxRadius = 20)
        try:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                if i[2] != 0:
                    y, x = i[0], i[1]
                    w, h = 10, 10
                    try:
                        img = img[x-w:x+w, y-h:y+h]
                        cv2.imwrite("circle/" + str(time.time()) + ".jpg", img)
                        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                        blur = cv2.GaussianBlur(hsv, (9,9), 0)
                        black = cv2.inRange(hsv, self.lower_black, self.upper_black)
                        n_black_pix = np.sum(black == 255)
                        self.CreateValidationLog(name ="FT",message = str(topic)+" "+str(n_black_pix)+"\n")
                        if n_black_pix >100:
                            if self.check():
                                return True
                        else:
                            return False
                    except Exception as e:
                        print(e)
            return False
        except Exception as e:
            return False

class Washer_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'station2.pb'
        label_lines = [
            "crosshs",
            "washernone",
            "hs",
            "handhs",
            "gasketnone",
            "gaskethand",
            "gasket",
            "washer",
            "handwasher"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="Washer_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        if result == "hs" or result == "crosshs":
            return "no"
        elif result == "washer" and self.acc>=80.0:
            return True
        else:
            return False

class HS_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'station2.pb'
        label_lines = [
            "crosshs",
            "washernone",
            "hs",
            "handhs",
            "gasketnone",
            "gaskethand",
            "gasket",
            "washer",
            "handwasher"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="HS_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        if result == "crosshs":
            return "no"
        elif result == "hs":
            return True
        else:
            return False

stage1 = {
	"Gasket_ML":Gasket_ML(),
	"Adapter_ML":Adapter_ML(),
	"FilterTower":FilterTower(),
	"Washer_ML":Washer_ML(),
	"HS_ML":HS_ML()
	}
