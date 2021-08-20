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


class S3_S4(ML_model,ValGen):
    def __init__(self):
        graph_path = 's3s4.pb'
        label_lines = [
            "trxassembly",
            "filterchassis"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="S3_S4",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        return result

class Mating_template(ML_model,ValGen):
    def __init__(self):
        graph_path = 'matingtemplate.pb'
        label_lines = [
            "nonematingtemplate",
            "matingtemplate"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="Mating_template",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        return result

class Remove_Mating_template(ML_model,ValGen):
    def __init__(self):
        graph_path = 'matingtemplate.pb'
        label_lines = [
            "nonematingtemplate",
            "matingtemplate"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="Mating_template",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        if result == "nonematingtemplate" and self.acc>=70.0:
            return True
        else:
            return False

class Station4_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'screw4.pb'
        label_lines = [
            "beforescrew",
            "handscrew",
            "afterscrew"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="Station4_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        if not result == "afterscrew":
            return "no"
        elif result == "afterscrew" and self.acc>=85.0:
            return result
        return "False"


stage1 = {
	"S3_S4":S3_S4(),
	"Mating_template":Mating_template(),
	"Remove_Mating_template":Remove_Mating_template(),
	"Station4_ML":Station4_ML()
	}