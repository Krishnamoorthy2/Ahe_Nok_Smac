import cv2
import numpy as np
import time
import json
import os

def blob(img):
    cv2.imwrite("crop\\blob_"+str(time.time())+".jpg", img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 65, 2)
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 3
    params.maxThreshold = 255

    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 300

    params.filterByColor = True
    params.blobColor = 0

    params.filterByCircularity = True
    params.minCircularity = 0.7

    params.filterByConvexity = True
    params.minConvexity = 0.7

    params.filterByInertia = True
    params.minInertiaRatio = 0.7

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(thresh)
    if keypoints:
        with open("op.txt","a") as f:
            f.write("blob in concentric\n")
        return 1
    else:
        return 0

def blob_big(img):
    cv2.imwrite("crop\\blob_big"+str(time.time())+".jpg", img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 65, 2)
    
    kernel = np.ones((5,5), np.uint8)
    img_erode = cv2.erode(thresh, kernel, iterations=1) 
    
    params = cv2.SimpleBlobDetector_Params()
        # Change thresholds
    params.minThreshold = 3
    params.maxThreshold = 255

        # Filter by Color
    params.filterByColor = True
    params.blobColor = 255

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(img_erode)
    if keypoints:
        with open("op.txt","a") as f:
            f.write("blob_in big\n")
        return 1
    else:
        return 0

def square_val(img):
    cv2.imwrite("crop\\square_val"+str(time.time())+".jpg", img)
    kernel = np.ones((5,5), np.uint8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 65, 2)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1) 
    _, contours, h = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        _,_,w,h = cv2.boundingRect(cnt)
        ar = float(w)/h
        with open("op.txt","a") as f:
            f.write("area: "+ str(area)+" ar: "+ str(ar)+"\n")
        # print("area: "+ str(area)+" ar: "+ str(ar))
        if 260<area<500 and 0.8<ar<1.4:
            return 1
    return 0

def pixel_val(img):
    cv2.imwrite("crop\\pixel_val"+str(time.time())+".jpg", img)
    green_lower = np.array(np.array([33, 25, 26]))
    green_upper = np.array(np.array([102, 255, 255]))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    green=cv2.inRange(hsv, green_lower, green_upper)
    n_green_pix = np.sum(green == 255)
    with open("op.txt","a") as f:
        f.write("n_green_pix: "+ str(n_green_pix)+"\n")
    # print("n_green_pix: "+ str(n_green_pix))
    if n_green_pix > 600 and n_green_pix < 5000:
        return 1
    else:
        return 0

def feature_calc(img, station_id):
    cv2.imwrite("crop\\feature_calc"+str(time.time())+".jpg", img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    db_images = ['db_S'+station_id+'_v0.jpg', 'db_S'+station_id+'_v1.jpg', 'db_S'+station_id+'_v2.jpg']
    feature_count = 0
    for img1 in db_images:
        img1 = cv2.imread("data\\test\\"+img1, 0)
        feature_count += feature_check(img1, img)
    with open("op.txt","a") as f:
        f.write("len(db_images): "+ str(len(db_images))+"\tfeature_count: "+ str(feature_count)+"\n")
    if len(db_images)==(feature_count):
        return 1
    else:
        return 0

def feature_check(img1, img2):
    try:
        orb = cv2.AKAZE_create(descriptor_size=0, descriptor_channels=3, threshold=0.00001, nOctaves=4, nOctaveLayers=4, diffusivity=0)
        _, des1 = orb.detectAndCompute(img1,None)
        _, des2 = orb.detectAndCompute(img2,None)

        FLANN_INDEX_LSH = 6
        index_params= dict(algorithm = FLANN_INDEX_LSH, table_number = 6, key_size = 12, multi_probe_level = 1)

        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1,des2,k=2)

        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)
        with open("op.txt","a") as f:
            f.write("len(good): "+ str(len(good))+"\n")

        # print("len(good): "+ str(len(good)))
        if 20 <= len(good) <= 500:
            return 1
        elif len(good) > 4000:
            return -1
        else:
            return 0
    except:
        return 0

def db_check(focus):
    with open("smacar.json", "r") as read_file:
        config_data = json.load(read_file)
        station_id = config_data["station_id"]
    # circle1 = blob(focus[600:750, 300:480])   # modified 
    circle1 = blob(focus[590:676, 330:425])  
    # circle2 = blob_big(focus[565:730, 210:330]) #modified  
    circle2 = blob_big(focus[560:640, 244:315])
    # square = square_val(focus[414:490, 0:100])   #modified   
    square = square_val(focus[375:474, 20:100])
    # pixel = pixel_val(focus[655:, :455])

    # path = "crop"

    # try:  
    #     os.mkdir(path)
    # except OSError:  
    #     print ("crop folder creation %s failed" % path)
    # else:  
    #     print ("Successfully created the crop folder %s " % path)

    # feature = feature_calc(focus, station_id)
    feature=1
    if circle1 and circle2:
        print("circles found")                          #changed
        with open("validate.txt","w+") as f:                    #cmt
            f.write("both circles found\n")                       #cmt
        if square:
            print("square found")
            with open("validate.txt","a+") as f:
                f.write("square found\n")
            if feature == 1:
                print("features matched")
                dirname="data\\db_"+station_id
                with open("validate.txt","a+") as f:
                    f.write("feature is true\n")
                
                 
                if not os.path.exists(dirname):
                    os.mkdir(dirname)
                    cv2.imwrite(dirname+""+"\\"+"temp.jpg", focus)
                    # print("dbbbbbbbbbbbbbbbbbbbbbbbbb")
                else:
                    cv2.imwrite("data\\db_"+station_id+"\\temp.jpg", focus)
                    # print("faillllllllllllllllllllllllllllllllll")
                return True
            elif feature == -1:
                return True
            else:
                print("feature matching algorithm failed")
        else:
            print("square not found")
    else:
        print("circles not found")
        return False
    # cv2.imwrite("data\\db_"+str(station_id)+"\\temp.jpg", focus)
    # return True
        