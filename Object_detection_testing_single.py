import os
import re
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import sys
import collections
sys.path.append("..")
from google.protobuf import reflection, message
import glob
from db_validation import db_check

nn = 0
cntt=0

class ML_detection():
    
    def __init__(self,cv_img): 

        self.MODEL_NAME = 'inference_graph'
        self.image = cv_img
        self.CWD_PATH = os.getcwd()
        self.a=self.CWD_PATH
        self.PATH_TO_CKPT = os.path.join(self.CWD_PATH,'frozen_inference_graph.pb')
        self.NUM_CLASSES = 1
        self.use_display_name = True
        # print(" Constructor")
        self.load_func(self.image)
                    
    def visualization_utils(self, image,boxes, classes, scores, instance_masks=None,instance_boundaries=None, keypoints=None,use_normalized_coordinates=False,max_boxes_to_draw=20,min_score_thresh=.5,agnostic_mode=False,line_thickness=4,groundtruth_box_visualization_color='black',skip_scores=False,skip_labels=False):
        category_index = {1:{'id':1, 'name':'chasis'}}
        box_to_display_str_map = collections.defaultdict(list)
        box_to_color_map = collections.defaultdict(str)
        box_to_instance_masks_map = {}
        box_to_instance_boundaries_map = {}
        box_to_keypoints_map = collections.defaultdict(list)
        if not max_boxes_to_draw:
            max_boxes_to_draw = boxes.shape[0]
        for i in range(0, boxes.shape[0]):
            if scores is None or scores[i] > min_score_thresh:
                box = tuple(boxes[i].tolist())
                if instance_masks is not None:
                    box_to_instance_masks_map[box] = instance_masks[i]
                if instance_boundaries is not None:
                    box_to_instance_boundaries_map[box] = instance_boundaries[i]
                if keypoints is not None:
                    box_to_keypoints_map[box].extend(keypoints[i])
                if scores is None:
                    box_to_color_map[box] = groundtruth_box_visualization_color
                else:
                    display_str = ''
                    if not skip_labels:
                        if not agnostic_mode:
                            if classes[i] in category_index.keys():
                                class_name = category_index[classes[i]]['name']        
                            else:
                                class_name = 'N/A'
                            display_str = str(class_name)                
                    if not skip_scores:
                        if not display_str:
                            display_str = '{}%'.format(int(100*scores[i]))
                        else:
                            display_str = '{}: {}%'.format(display_str, int(100*scores[i]))
                    box_to_display_str_map[box].append(display_str)
                    if agnostic_mode:
                        box_to_color_map[box] = 'DarkOrange'
                    else:
                        box_to_color_map[box] = 'DarkOrange'
        # print(" Visualization_utils")
        
        for box, color in box_to_color_map.items():
            ymin, xmin, ymax, xmax = box
            image_pil = Image.fromarray(np.uint8(image)).convert('RGB')
            im_width, im_height = image_pil.size
            if use_normalized_coordinates:
                (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                            ymin * im_height, ymax * im_height)
                print("iff",left, top, right, bottom)
                crop = image_pil.crop((left, top, right, bottom))                
            else:
                (left, right, top, bottom) = (xmin, xmax, ymin, ymax)
                print("else",left, top, right, bottom)
            
            #####save ML image
            if crop is not None:
                print(" Got crop from ML ")
                convert_cv = np.array(crop)
                convert_cv = cv2.resize(convert_cv, (455,789))
                

            # define the name of the directory to be created
            # if path is None:
                # path = "ml"

                # try:  
                #     os.mkdir(path)
                # except OSError:  
                #     # print _
                #     print ("Creation of the directory %s failed" % path)
                # else:  
                #     # print _
                #     print ("Successfully created the directory %s " % path)

                global cntt

                cv2.imwrite("ml\\frame_%d.jpg" % cntt, convert_cv)
                # print("ml image has been saved to the ml folder.")
                cntt += 1 


                nv = db_check(convert_cv)
                print("Db check result ",nv)
                global nn
                nn = nv
                if nv :
                    # changed for station 2 db capture
                    top = cv2.imread('top_cover.jpg')
                    frame = convert_cv
                    img = top
                    h, w, _ = img.shape
                    x, y = 0, 3
                    frame[x:x+h, y:y+w] = img[:, :]
                    focus = frame
                    # focus = self.apply_img(focus, self.top, 0, 3)                
                    cv2.imwrite("data\\db_2\\temp.jpg", focus)
                    cv2.imwrite("data\\db_3\\db_S3_v0.jpg", focus)
                    # changed for station 2 db capture
                else :
                    print('Db check failed !!!!!!!!!!!!!')
            else:
                print(" Crop from ML not found ")

    def load_func(self,image):
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            sess = tf.Session(graph=detection_graph)
        image_tensor       = detection_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes    = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores   = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes  = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections     = detection_graph.get_tensor_by_name('num_detections:0')
        image_expanded     = np.expand_dims(image, axis=0)
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})
        # print("load function")
        # print(" Image_tensor",type(image_tensor),' Detection_boxes',type(detection_boxes),' Detection_scores',type(detection_scores),' Num_detections',type(num_detections),' Image_expanded',type(image_expanded))
        self.visualization_utils(image, np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores), use_normalized_coordinates=True, line_thickness=8, min_score_thresh=0.98)

import cv2

def ob(cam):

    obj = ML_detection(cam)
    if nn :
        print("Db check final resultttt",nn)
        return nn
        
    




    


