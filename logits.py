import cv2
import numpy as np
from time import time
import imutils
from log_generator import ValGen


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

class Text(object):

    def main(self, _):
        stage1["Screw_Main"].result = [0]*24
        return False


class Screw_Lower_Contour(Counter):
    def __init__(self):
        Counter.__init__(self, limit=0)
        self.params = cv2.SimpleBlobDetector_Params()

        self.params.minThreshold = 3
        self.params.maxThreshold = 255

        self.params.filterByArea = True
        self.params.maxArea = 100

        self.params.filterByColor = True
        self.params.blobColor = 0

        self.params.filterByConvexity = True
        self.params.minConvexity = 0.7

        self.params.filterByCircularity = True
        self.params.minCircularity = 0.7

        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.7

        self.detector = cv2.SimpleBlobDetector_create(self.params)
        
        
    def blob(self,img):
        blur = cv2.GaussianBlur(img,(5,5),0)
        keypoints = self.detector.detect(blur)
        if keypoints:
            cv2.imwrite("no_screw/"+str(time.time())+".jpg",img)
            return 0
        else:
            cv2.imwrite("screw/"+str(time.time())+".jpg",img)
            return 1

class Screw_FT(Counter):
    def __init__(self):
        Counter.__init__(self, limit=0)

        self.params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        self.params.minThreshold = 3
        self.params.maxThreshold = 255

        # Filter by Area.
        self.params.filterByArea = True
        # self.params.minArea = 10
        self.params.maxArea = 100

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

    def blob(self,img):
        blur = cv2.GaussianBlur(img,(5,5),0)
        keypoints = self.detector.detect(blur)
        if keypoints:
            cv2.imwrite("no_screw/"+str(time.time())+".jpg",img)
            return 0
        else:
            cv2.imwrite("screw/"+str(time.time())+".jpg",img)
            return 1   

class Screw_10(Counter):
    def __init__(self):
        Counter.__init__(self, limit=0)

        self.params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
        self.params.minThreshold = 3
        self.params.maxThreshold = 255

        # Filter by Area.
        self.params.filterByArea = True
        # self.params.minArea = 10
        self.params.maxArea = 100

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
        self.params.minInertiaRatio = 0.25

        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def blob(self,img):
        blur = cv2.GaussianBlur(img,(5,5),0)
        keypoints = self.detector.detect(blur)
        if keypoints:
            cv2.imwrite("no_screw/"+str(time.time())+".jpg",img)
            return 0
        else:
            cv2.imwrite("screw/"+str(time.time())+".jpg",img)
            return 1

class Screw_20(Counter):
    def __init__(self):
        Counter.__init__(self, limit=0)
        self.params = cv2.SimpleBlobDetector_Params()

        self.params.minThreshold = 3
        self.params.maxThreshold = 255

        self.params.filterByArea = True
        self.params.minArea = 60
        self.params.maxArea = 100

        self.params.filterByColor = True
        self.params.blobColor = 0

        self.params.filterByConvexity = True
        self.params.minConvexity = 0.5

        self.params.filterByCircularity = True
        self.params.minCircularity = 0.5

        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.5

        self.detector = cv2.SimpleBlobDetector_create(self.params)
        
        
    def blob(self,img):
        blur = cv2.GaussianBlur(img,(5,5),1)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
        keypoints = self.detector.detect(thresh)
        if keypoints:
            cv2.imwrite("no_screw/"+str(time.time())+".jpg",img)
            return 0
        else:
            cv2.imwrite("screw/"+str(time.time())+".jpg",img)
            return 1

    def contour(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
        _,contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt,True)
            x,y,w,h = cv2.boundingRect(cnt)
            ar = float(w)/h
            if 0.6<=ar<0.8 and 170<area<300:
                return 0
        return 1

class Screw_21(Counter):
    def __init__(self):
        Counter.__init__(self, limit=0)
        self.params = cv2.SimpleBlobDetector_Params()

        self.params.minThreshold = 3
        self.params.maxThreshold = 255

        self.params.filterByArea = True
        self.params.minArea = 30
        self.params.maxArea = 100

        self.params.filterByColor = True
        self.params.blobColor = 0

        self.params.filterByConvexity = True
        self.params.minConvexity = 0.5

        self.params.filterByCircularity = True
        self.params.minCircularity = 0.5

        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.01

        self.detector = cv2.SimpleBlobDetector_create(self.params)
        
        
    def blob(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(3,3),0)
        ret2,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        keypoints = self.detector.detect(thresh)
        if keypoints:
            cv2.imwrite("no_screw/"+str(time.time())+".jpg",img)
            return 0
        else:
            cv2.imwrite("screw/"+str(time.time())+".jpg",img)
            return 1

class Screw_23(Counter):
    def __init__(self):
        self.lower = np.array([0, 0, 113])
        self.upper = np.array([179, 62, 255])
        
    def contour(self,img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
        _,contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt,True)
            x,y,w,h = cv2.boundingRect(cnt)
            ar = float(w)/h
            if 0.6<=ar<0.75 and 50<area<200:
                crop = img[y:y+h,x:x+w]
                hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
                gray = cv2.inRange(hsv, self.lower, self.upper)
                print(np.sum(gray==0))
                if (np.sum(gray==0)) >85:
                    return 0
        return 1


class Screw_Main(Counter,ValGen):
    def __init__(self):
        Counter.__init__(self, limit=1)
        self.result = [0]*24
        self.screw_FT =  {1:[205, 30], 11:[110,30], 13:[300,30],}
        self.screw_Elevated = {3:[214, 81], 4:[202, 140], 15:[310, 81], 16:[295,140], 9:[103, 140], }#10:[117,82],}
        self.screw_Lower = {5:[215, 274], 6:[195, 273], 7:[120, 273], 8:[97, 273], 17:[290, 273], 18:[311, 273], 19:[23, 273],}
        self.screw_corners = {21:[28,30], 22:[389, 30],}
        self.placed = []

    def cropping(self,src,x,y,id):
        crop = src[y-15:y+15,x-15:x+15]
        cv2.imwrite("screw_crop\\"+str(id)+"_"+str(time.time())+".jpg",crop)
        return crop

    def main(self,img,topic):
        strt = time.time()
        f = open("screw.txt", "w+")
        self.placed = []
        if stage1["TC_ML"].run(img,topic) == "handtc":
            print("remove hands")
            return False
        for screw in self.screw_FT.keys():
            x,y = self.screw_FT.get(screw)
            crop = img[y-30:y+30,x-34:x+34]
            self.result[screw-1] += stage1["Screw_FT"].blob(crop)
            f.write(str(screw)+"\t"+str(self.result[screw-1])+"\n")            
        for screw in self.screw_Elevated.keys():
            x,y = self.screw_Elevated.get(screw)
            crop = img[y-32:y+32,x-32:x+32]
            self.result[screw-1] += stage1["Screw_FT"].blob(crop)
            f.write(str(screw)+"\t"+str(self.result[screw-1])+"\n")            
        for screw in self.screw_Lower.keys():
            x,y = self.screw_Lower.get(screw)
            crop = img[y-15:y+15,x-15:x+15]
            self.result[screw-1] += stage1["Screw_Lower_Contour"].blob(crop)
            f.write(str(screw)+"\t"+str(self.result[screw-1])+"\n")
        # Screw_10
        x, y = 117,82
        crop = img[y-32:y+32,x-32:x+32]
        self.result[10-1] += stage1["Screw_10"].blob(crop)
        f.write("10\t"+str(self.result[10-1])+"\n")
        # Screw_20
        x, y = 30, 80
        crop = img[y-30:y+30,x-30:x+30]
        self.result[20-1] += stage1["Screw_20"].contour(crop)
        print(20,self.result[20-1])
        for screw in self.screw_corners.keys():
            x,y = self.screw_corners.get(screw)
            crop = img[y-25:y+25,x-25:x+25]
            self.result[screw-1] += stage1["Screw_21"].blob(crop)
            f.write(str(screw)+"\t"+str(self.result[screw-1])+"\n")
        # Screw_23
        x, y = 386, 140
        crop = img[y-30:y+30,x-30:x+30]
        self.result[23-1] += stage1["Screw_23"].contour(crop)
        f.write("23\t"+str(self.result[23-1])+"\n")
        # Screw_24
        x, y = 386, 273
        crop = img[y-15:y+15,x-15:x+15]
        self.result[24-1] += stage1["Screw_FT"].blob(crop)
        f.write("24\t"+str(self.result[24-1])+"\n")            
        temp = np.array(self.result)
        checksum = temp >= 2            
        if len(temp[checksum]) == 21 and self.result[24-1]>=2:
            self.result = [0]*24
            return True
        else:
            for i in [i for i,x in enumerate(self.result) if x>=2]:
                self.placed.append(i+1)
                self.CreateValidationLog(name ="TC_Screw",message = str(topic)+" "+str(self.placed)+"\n")
        print("placed : ",self.placed)
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
            # print("Filter tower error",e)
            return False


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

class MlStage1(ML_model,ValGen):
    def __init__(self):
        graph_path = 'station1.pb'
        label_lines = [
            "gs",
            "tc",
            "gsnone",
            "tcnone"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="GS_TC_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        return result

class dc_ret_ml(ML_model,ValGen):
    def __init__(self):
        graph_path = 'dcret.pb'
        label_lines = [
            "nonedc",
            "handdc",
            "dc",
            "worstret",
            "ret",
            "noneret"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img, topic):
        result = self.main(img)
        self.CreateValidationLog(name ="DC_RET_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        if result == "dc":
            if self.acc >= 50.0:
                return result
            else:
                return "nonedc"
        return result

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
        # ValGen.__init__(self, "Station3_ML_log")

    def run(self, img,topic):
        # self.CreateValidationLog("Ip:"+" "+str(topic)+"Station3_ML")
        return self.main(img)

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
        elif result == "washer":
            return True
        else:
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
        elif result == "washer":
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


class Station3_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'shield.pb'
        label_lines = [
            "shield",
            "handshield",
            "shieldcover",
            "noneshieldcover",
            "handshieldcover",
            "noneshield"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="Station3_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        return result


class TC_ML(ML_model,ValGen):
    def __init__(self):
        graph_path = 'handtc.pb'
        label_lines = [
            "handtc",
            "nohandtc"
        ]
        ML_model.__init__(self, graph_path, label_lines)

    def run(self, img,topic):
        result = self.main(img)
        self.CreateValidationLog(name ="TC_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        return result

class Ml_PA(ML_model):
    def __init__(self):
        graph_path = 'PA_Final.pb'
        label_lines = [
           "pa54",
            "gshandpa",
            "pa53"
            ]
        ML_model.__init__(self, graph_path, label_lines)

    def vali_53(self, img,topic):
        #cv2.imwrite("img.jpg",img)
        # rows,cols,_ = img.shape
        # M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
        # dst = cv2.warpAffine(img,M,(cols,rows))
        #cv2.imwrite("dst.jpg",dst)
        result = self.main(img)
        # if result == "pa54" or result == "pa53":
        #     res1=stage1["PA_Blobs"].blob(img)
        #     res2=stage1["PA"].main_53(img)
        #     if res1 == "pa54": #and res2 == "pa54":
        #         return "no"
        #     elif res1 == "pa53":# and res2 == "pa53":
        #         return True
        #     else:
        #         return False
        if result == "pa54" or result == "pa53":
            res1=stage1["PA"].main_53(img, topic)
            if res1=="pa54":
                return "no"
            elif res1=="pa53":
                return True
            else:
                return False
        else:
            return False

    def vali_54(self, img,topic):
        # rows,cols,_ = img.shape
        # M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
        # dst = cv2.warpAffine(img,M,(cols,rows))
        result = self.main(img)
        if result == "pa54" or result == "pa53":
            # res1=stage1["PA_Blobs"].blob(dst)
            res1=stage1["PA"].main_54(img, topic)
            if res1 == "pa53":# and res2 == "pa53":
                return "no"
            elif res1 == "pa54":# and res2 == "pa54":
                return True
            else:
                return False
        else:
            return False

    def vali_53rotate(self, img,topic):
        #cv2.imwrite("img.jpg",img)
        rows,cols,_ = img.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
        dst = cv2.warpAffine(img,M,(cols,rows))
        #cv2.imwrite("dst.jpg",dst)
        result = self.main(dst)
        # if result == "pa54" or result == "pa53":
        #     res1=stage1["PA_Blobs"].blob(img)
        #     res2=stage1["PA"].main_53(img)
        #     if res1 == "pa54": #and res2 == "pa54":
        #         return "no"
        #     elif res1 == "pa53":# and res2 == "pa53":
        #         return True
        #     else:
        #         return False
        if result == "pa54" or result == "pa53":
            res1=stage1["PA"].main_53(dst, topic)
            if res1=="pa54":
                return "no"
            elif res1=="pa53":
                return True
            else:
                return False
        else:
            return False

    def vali_54rotate(self, img,topic):
        rows,cols,_ = img.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
        dst = cv2.warpAffine(img,M,(cols,rows))
        result = self.main(dst)
        if result == "pa54" or result == "pa53":
            # res1=stage1["PA_Blobs"].blob(dst)
            res1=stage1["PA"].main_54(dst, topic)
            if res1 == "pa53":# and res2 == "pa53":
                return "no"
            elif res1 == "pa54":# and res2 == "pa54":
                return True
            else:
                return False
        else:
            return False


class PA(ValGen):
    def __init__(self):
        self.lower_green = np.array([33, 25, 26])
        self.upper_green = np.array([102, 255, 255])
    

    def main_53(self,img, topic):
        #img = cv2.imread(img)
        (h, w) = img.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        raw_img = img[cY-10:h, 0:w]
        gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        (T, threshotsu) = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        threshadap = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,97,1)
        _, cnts, h = cv2.findContours(threshotsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        clone = raw_img.copy()
        for(i, c) in enumerate(cnts):
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
            if 1000<area<1800 and 130<perimeter<180 and len(approx)==4:
                cv2.drawContours(clone, [c], -1, (0, 255, 0), 2)
                (x, y, w, h) = cv2.boundingRect(c)
                crop = threshadap[y-10:y+8,x-30:x-30+30]
                n_black_pix_crop = np.sum(crop == 0)
                self.CreateValidationLog(name ="PA_53",message = str(topic)+" "+str(n_black_pix_crop)+"\n")
                if n_black_pix_crop < 230:
                    return "pa53"
                elif n_black_pix_crop > 290:
                    return "pa54"
                else:
                    return False
    def main_54(self,img, topic):
        #img = cv2.imread(img)
        (h, w) = img.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        raw_img = img[cY-10:h, 0:w]
        gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        (T, threshotsu) = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        threshadap = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,97,1)
        _, cnts, h = cv2.findContours(threshotsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        clone = raw_img.copy()
        for(i, c) in enumerate(cnts):
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
            if 1000<area<1800 and 130<perimeter<180 and len(approx)==4:
                cv2.drawContours(clone, [c], -1, (0, 255, 0), 2)
                (x, y, w, h) = cv2.boundingRect(c)
                crop = threshadap[y-10:y+8,x-30:x-30+30]
                n_black_pix_crop = np.sum(crop == 0)
                self.CreateValidationLog(name ="PA_53",message = str(topic)+" "+str(n_black_pix_crop)+"\n")
                if n_black_pix_crop > 290:
                    return "pa54"
                elif n_black_pix_crop < 230:
                    return "pa53"
                else:
                    return False

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

class DC_Screw(Counter,ValGen):
    def __init__(self):
        Counter.__init__(self, limit=2)
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
        if not keypoints:
            if self.check():
               return True         
        else:
            self.reset()
            print (len(keypoints))
            return False
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


class S4_Screw12(Counter):
    def __init__(self):
        Counter.__init__(self, limit=0)
        
        self.params = cv2.SimpleBlobDetector_Params()

        # Filter by Area.
        self.params.filterByArea = True
        self.params.minArea = 30
        self.params.maxArea = 90

        # # Filter by Color
        self.params.filterByColor = True
        self.params.blobColor = 255

        # Filter by Circularity
        self.params.filterByCircularity = True
        self.params.minCircularity = 0.4

        # # Filter by Convexity
        self.params.filterByConvexity = True
        self.params.minConvexity = 0.5

        # # Filter by Inertia
        self.params.filterByInertia = True
        self.params.minInertiaRatio = 0.5
        
        self.detector = cv2.SimpleBlobDetector_create(self.params)

    def blob(self, img):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        (T, threshInv) = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        keypoints = self.detector.detect(threshInv)
        if keypoints:
            return 0
        return 1              

class Screws_S4(Counter,ValGen):
    def __init__(self):
        Counter.__init__(self, limit=1)
        self.screws_pos = { 
                        1:[276,14],2:[140,720],3:[24,714],4:[27,602],5:[27,492],6:[27,383],
                        7:[27,272],8:[27,160],9:[27,30],10:[90,14],11:[179,14],13:[431,36],
                        14:[429,163],15:[429,272],16:[426,383],17:[426,492],18:[426,602],
                        19:[426,710],21:[254,720]
                        }

        self.result = [0]*21
        
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

    def blob(self,img):
        keypoints = self.detector.detect(img)
        if keypoints:
            return 0
        return 1

    def main(self, img,topic):
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        placed = []
        for s_id in self.screws_pos.keys():
            [x, y] = self.screws_pos[s_id]
            crop = gray[y-14:y+14, x-14:x+14]
            self.result[s_id-1] = self.blob(crop)
            # print(s_id-1,self.result[s_id-1])
        
        #screw_12 : [364,14]
        crop = img[14-14:14+14,364-14:364+14]
        self.result[12-1] = stage1["S4_Screw12"].blob(crop)
        # print(12,self.result[12-1])
        
        #screw_20 : [322,720]
        crop2 = img[720-14:720+14,322-14:322+14]     
        blur = cv2.GaussianBlur(crop2, (5, 5), 0)
        gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)
        self.result[20-1] = self.blob(gray)
        # print(20,self.result[20-1])

        # for i in [i for i,x in enumerate(self.result) if x==1]:
        #     print(i+1)
        
        for i in [i for i,x in enumerate(self.result) if x==1]:
            placed.append(i+1)
            self.CreateValidationLog(name ="S4_Screw",message = str(topic)+" "+str(placed)+"\n")
        
        if sum(self.result) == 21:
            if self.check():
                self.result = [0]*21
                return True
            return False
        else:
            self.reset()
            return False

class TRX(Counter,ValGen):
    def __init__(self):
        Counter.__init__(self, limit=1)
        # ValGen.__init__(self, "screw_s4_log")
        self.lower_green = np.array([33, 25, 26])
        self.upper_green = np.array([102, 255, 255])

    def Pixel_Count(self, img):
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        green = cv2.inRange(hsv, self.lower_green, self.upper_green)
        n_green_pix = np.sum(green == 255)
        return n_green_pix

    def TRX_stat3(self, img,topic):
        crop = img[259:767,16:434]
        try:
            cv2.imwrite("out/"+str(time.time())+".jpg",crop)
        except Exception as e:
            print(e)
        result = self.Pixel_Count(crop)
        print(result)
        self.CreateValidationLog(name ="TRX_Assembly",message = str(topic)+" "+str(result)+"\n")
        if result < 85000:
            return False
        else:
            if self.check():
                return True
            else:
                return False

    def TRX_stat4(self, img,topic):
        crop = img[259:767,16:434]
        result = self.Pixel_Count(crop)
        print(result)
        self.CreateValidationLog(name ="Filter_Chassis",message = str(topic)+" "+str(result)+"\n")
        if result > 10500:
            return False
        else:
            if self.check():
                return True
            else:
                return False

stage1 = {
    "dc_ret_ml":dc_ret_ml(),
    "Text": Text(),
    "Text_barcode" : Text(),
    "Text_connectors" : Text(),
    "MlStage1":MlStage1(),
    "Text_PA" : Text(),
    "PA":PA(),  
    "Screw_FT": Screw_FT(),
    "HS_ML":HS_ML(),
    "Washer_ML":Washer_ML(),
    "Gasket_ML":Gasket_ML(),
    "Adapter_ML":Adapter_ML(),
    "Screw_23" : Screw_23(),
    "Screw_21" : Screw_21(),
    "Screw_20": Screw_20(),
    "Screw_10": Screw_10(),
    "Screw_Main" : Screw_Main(),
    "Screw_Lower_Contour":Screw_Lower_Contour(),
    "FilterTower": FilterTower(),  
    "Station3_adapter_upper":Station3_adapter_upper(),
    "DC_Screw":DC_Screw(),
    "Screws_S3" : Screws_S3(),
    "S3_19" : S3_19(),
    "Station3_ML":Station3_ML(),
    "Screws_S4":Screws_S4(),
    "S4_Screw12":S4_Screw12(),
    "Ml_PA": Ml_PA(),
    "Station4_ML":Station4_ML(),
    "Mating_template":Mating_template(),
    # "Screws_S4_ML":Screws_S4_ML(),
    "Remove_Mating_template":Remove_Mating_template(),
    "TRX":TRX(),
    "TRX_ML":TRX_ML(),
    "TC_ML":TC_ML(),
    "S3_S4":S3_S4(),
    "Trx_Assembly":Trx_Assembly()
}