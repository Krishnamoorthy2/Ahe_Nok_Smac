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
        stage1["Screw_Main"].result = [0]*24
        result = self.main(img)
        print("dc",result)
        self.CreateValidationLog(name ="DC_RET_ML",message = str(topic)+" "+str(result)+" "+str(self.acc)+"\n")
        if result == "dc":
            if self.acc >= 50.0:
                # print("r",result)
                return result
            else:
                return "nonedc"     
        return result


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
        result = self.main(img)
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
        result = self.main(img)
        if result == "pa54" or result == "pa53":
            res1=stage1["PA"].main_54(img, topic)
            if res1 == "pa53":
                return "no"
            elif res1 == "pa54":
                return True
            else:
                return False
        else:
            return False

    def vali_53rotate(self, img,topic):
        rows,cols,_ = img.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
        dst = cv2.warpAffine(img,M,(cols,rows))
        result = self.main(dst)
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
            res1=stage1["PA"].main_54(dst, topic)
            if res1 == "pa53":
                return "no"
            elif res1 == "pa54":
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


class Screw_Lower_Contour():
    def __init__(self):
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

class Screw_FT():
    def __init__(self):

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

class Screw_10():
    def __init__(self):

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

class Screw_20():
    def __init__(self):
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

class Screw_21():
    def __init__(self):
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

class Screw_23():
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

class Screw_Main(ValGen):
    def __init__(self):
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

stage1 = {
    "dc_ret_ml":dc_ret_ml(),
    "MlStage1":MlStage1(),
    "Ml_PA":Ml_PA(),
    "PA":PA(),
    "Screw_Main":Screw_Main(),
    "Screw_Lower_Contour" : Screw_Lower_Contour(),
    "Screw_FT":Screw_FT(),
    "Screw_23" : Screw_23(),
    "Screw_21" : Screw_21(),
    "Screw_20": Screw_20(),
    "Screw_10": Screw_10(), 
    "TC_ML":TC_ML(),
    }

