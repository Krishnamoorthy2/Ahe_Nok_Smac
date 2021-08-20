from __future__ import absolute_import, division, print_function, unicode_literals
from render.overlay import DrawImage
from render.py3d import Interface3d
from utils.utils import proper_img, get_scn_points, place_text, get_patch, rotationAngle, place_text1, encode_img, mse

# from network.publish import jsonDump, send  # , send1
from network.text_handler import station_id,restrict
# from network.analytics import restthread
import cv2
from camera.camera import aspectRatio
from utils.config import testLocal,LocalJson
from utils.utils import alert    
import winsound
import time,socket
from center import hardware_handler, ui_handler, traceback
# from logits import stage1
import datetime
import logits1
import threading

LocalJson_obj = LocalJson()
LocalJson_obj.load_local_json()
token = LocalJson_obj.token
sid= LocalJson_obj.station_id
sid=int(sid)


# Dicts = {}
# Dictz = {}
cnt = 0
class trigger:
    tracking = False

    @classmethod
    def update(cls, value):
        cls.tracking = value

    def __init__(self, value):
        self.value = value
        self.update(value)

class pclose:
    status = False

    @classmethod
    def update(cls, value):
        cls.status = value

    def __init__(self, value):
        self.value = value
        self.update(value)


class counter(object):
    def __init__(self, limit):
        self.counter = 0
        self.counter_limit = limit

    def update(self):
        self.counter += 1

    def reset(self):
        self.counter = 0
        # self.counter_limit = 0

    def check(self):
        if self.counter < self.counter_limit:
            self.update()
            return False
        elif self.counter >= self.counter_limit:
            self.reset()
            return True


class FilterSystem(object):
    def __init__(self, msg_pos):
        self.station_msg_pos = msg_pos
        self.publishcount = 0
        self.noop = 0
        self.noop_dur = 240
        self.mse = mse
        self.l = []
        self.adapcount = False

    def wrong(self):
        del self.l[1]

    def reset(self):
        self.l = []
        self.publishcount = 0
        self.noop = 0
        self.adapcount = False
        #Adapter(False)

    def process(self, thr, dur, patch_img):
        self.l.append(patch_img)
        if len(self.l) == 1:
            self.noop = 0
            return True
        elif len(self.l) == 2:
            err = self.mse(self.l)
            # #print err
            del self.l[1]
            if(err > thr):
                # self.noop = 0
                # return True
                self.publishcount += 1
                self.noop = 0
                if(self.publishcount >= dur):
                    self.publishcount = 0
                    return True
                else:
                    return False
            else:
                self.noop += 1
                if(self.noop >= self.noop_dur):
                    #graphite negative validation
                    # place_text(img=img, msg="   No-operation       ")
                    # place_text(img=img, msg="No-operation       ",
                    #            pos=self.station_msg_pos)
                    return False
                else:
                    return False
        else:
            return False

class NokiaLogic(object):

    def __init__(self, py3d_obj, ui_obj, station_id):
        self.py3d_obj = py3d_obj
        self.ui_obj = ui_obj
        self.draw_obj = DrawImage()
        self.current, self.count = 0, 0

        self.wait, self.lock, self.audio_check = False, False, False
        self.one = True

        self.i, self.j = 0, 0
        self.text_counter_obj = counter(limit=0)
        self.display_off_counter_obj = counter(limit=90)
        self.display_on_counter_obj = counter(limit=90)
        self.color  = (165, 77, 25)

        self.sid = station_id  #station id
        self.val_ord = None

    def pass_data(self, msg_data, client_id):
        self.station_msg = msg_data[0]
        self.station_msg_pos = msg_data[1]
        self.client_id = client_id
        self.filter_obj = FilterSystem(msg_pos=self.station_msg_pos)

    def __call__(self, payload):
        self.h, self.w = payload.target.image.shape
        self.h = int(self.h*aspectRatio)
        self.w = int(self.w*aspectRatio)
        self.draw_obj(self.w, self.h)
        self.payload = payload.target.data

    def ui_trigger(self,operation):
        print (operation)
        try:
            a = self.get_id()
            # print("id",a)
            if a > 100:
                if self.ui_obj.btns[self.ui_obj.get_parent(a)]['child'] <= 8:
                    # #print("multisub")
                    self.ui_obj.update_multisubstep(a, operation)
                else:
                    # #print("sub")
                    self.ui_obj.update_substep(a, operation)                    
                # self.ui_obj.update_substep(a, operation)                    
            else:
                # #print("main")
                self.ui_obj.update_mainstep(a, operation)

        except Exception as e:
            ui_handler.CreateErrorLog(ui_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
    
    def _nextStep(self, operation="skip"):
        ##print (self.get_id())
        # print("selffffffffffffffffffffffffffffffffffffff waaaaaaaaaaaaaaaaaaaaaaaaaaaiiiiiiiiiiiiiitttttttttttttttt",self.wait)
        gname = self.payload[self.current].val_name
        op = operation
        g =gname
        
        # if ( ( ( (op == "yes") and (g == "MlStage1") ) or ( (op == "yes") and (g == "Ml_PA") ) or ( (op == "yes") and (g == "Washer_ML") ) )    or \
            #   ( ( (op == "skip" ) and (g != "Ml_PA") )   and  ( (op == "skip" ) and (g != "MlStage1") ) and ( (op == "skip" ) and (g != "Washer_ML") ) )   or   (op == "yes") ) :
        if ( ( (op == "yes" ) and (g != "Text_connectors") ) and  (operation == "yes") or (operation == "skip") ):
            # print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM in")
            if(self.wait==True and operation == "skip"):

                # print (self.wait)
                # print ("___________________________________________________________i am changing")
                restrict(False)
            # if ( ( (operation == "yes") and (gname == "MlStage1") ) or ( (operation == "yes") and (gname == "Ml_PA") ) or ( (operation == "yes") and (gname == "Washer_ML") )   or (operation=="skip")):
            #     pass

            else:
                pass
            self.ui_trigger("complete")
            self.color = (165,77,25)
            try:
                self.current_id = self.get_id()
            except Exception as e:
                ui_handler.CreateErrorLog(ui_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
            try:
                if self.current_id > 100:
                    parent = self.ui_obj.get_parent(self.current_id)
                    if self.current_id == (self.ui_obj.station*10000) + (parent*100) + self.ui_obj.btns[parent]['child']:
                        self.wait = True
                        self.lock = True
                    else:
                        if self.lock == False:
                            self.wait = False
                            # alert("right")
                            if(operation=="yes"):
                                status="done"
                            elif(operation=="skip"):
                                status="skip"
                            # payload={"substep_id":self.current_id,"status":status,"token":token}
                            # restthread("substep",payload)
                            self.current += 1
                            # print('counter',current)
                elif self.current_id < 100:
                    if self.lock == False:
                        self.wait = False
                        # alert("right")
                        if(operation=="yes"):
                            status="done"
                        elif(operation=="skip"):
                            status="skip"
                        else:
                            pass
                        if((sid==1 and (self.current_id in (4,8,9))) or (sid==2 and (self.current_id in (5, 6))) or (sid==3 and (self.current_id in (2,6,9))) or (sid==4 and (self.current_id == 4))):
                            payload={"step_id":self.current_id,"status":status,"token":token}
                            #print (payload)
                            #payload
                            # restthread("mainstep",payload)
                        else:
                            pass
                        self.current += 1
                        # print('counter',current)
                self.filter_obj.reset()
            except Exception as e:
                pass
        elif operation == "ignore":
            if self.lock == False:
                self.wait = False
            pass
        elif operation == "no":
            # alert("wrong")
            self.ui_trigger("error")
            self.color = (0,0,255)
            self.wait = False
            self.filter_obj.reset()
        self.draw_obj.clear_img()

    def _exit(self):
        if not testLocal:
            pass
            # send(self.client_id, "exit")

    def _reset_board(self):
        self.draw_obj(self.w, self.h)
        self.current, self.count, self.duration = 0, 0, 15

    def get_id(self):
        return self.payload[self.current].id

    def nokia_thread(self, obj, val_main, patch_image, client_ip, val_result ):
        global cnt
        cnt+=1
        print("ccccccccccccccccccccccccccccccccccccccccccccccccccc",cnt, val_main)
        result = getattr(obj, val_main)(patch_image, client_ip)
        result_cp = result
        decis = {val_result:"yes", "no":"no"}
        if result == (val_result or "no"):
            self._nextStep(str(decis[result]))
            print("[INFO] result Yes!!")
        else:
            self._nextStep("ignore")
            print("[INFO] result No")

    def main(self, img, meta_data):
        if(trigger.tracking == True):
            self.ui_obj.update_mainstep(1,"complete")
            if int(self.sid) == 2:
                payload={"step_id":1,"status":"done","token":token}
                # restthread("mainstep",payload)
            trigger(None)
        else:
            pass

        H, quad = meta_data
        demo_angle = rotationAngle(quad)

        if self.current >= 100:
            if self.audio_check == True:
                # alert("complete")
                self.audio_check = False
            self._reset_board()
            self.ui_obj.active_btns[:] = []
            self.ui_obj.id = 1
            self.ui_obj.flag = False
            self.ui_obj.create_activebtns(self.ui_obj.total_steps)
            trigger(False)
            return img
        elif self.current >= len(self.payload):
            self.ui_obj.flag = True
            self.ui_obj.text="completed"
            if self.audio_check == False:
                # alert("complete")
                self.audio_check = True
            self.current += 1
            # send(self.client_id, "exit")
            time.sleep(2)
            pclose(True)
            return img

        elif(self.payload[self.current].val_name.startswith("TextA") and self.text_counter_obj.check()):
            self._nextStep("yes")

        elif(self.payload[self.current].val_name.startswith("3DText") and self.text_counter_obj.check()):
            self._nextStep("yes")

        try:
            to_validate_img = proper_img(img, quad, self.w, self.h)
            patch_w, patch_h = self.payload[self.current].patch
            patch_w = int(patch_w*aspectRatio)  # clean me
            patch_h = int(patch_h*aspectRatio)  # clean me

            y, x = self.payload[self.current].ctr_pos
            y = int(y*aspectRatio)  # clean me
            x = int(x*aspectRatio)  # clean me
            temp = []
            temp1 = [
                [y - patch_h, x - patch_w],
                [y - patch_h, x + patch_w],
                [y + patch_h, x + patch_w],
                [y + patch_h, x - patch_w]
            ]


            patch_image = get_patch(
                img=to_validate_img, x=x, y=y, w=patch_w, h=patch_h, mask=None)


            
            # self.draw_obj._rectangle(  # debug
            #     (y + patch_h, x + patch_w), (y - patch_h, x - patch_w), colour=color)

    #  -----------------------------------------------------------------------------------------------------
            """SERVER"""
            check = self.filter_obj.process(
                thr=self.payload[self.current].val_thr, dur=self.payload[self.current].val_dur, patch_img=patch_image)
            # print ("check---------",check)
            if self.sid=='1':
                from logits1 import stage1
                # print("1--------")
            elif self.sid=='2':
                from logits2 import stage1
            elif self.sid=='3':
                from logits3 import stage1
            elif self.sid=='4':
                from logits4 import stage1      

                 
            if check and not self.wait and testLocal:  #check and not self.wait and not testLocal:
                val_name = self.payload[self.current].val_name
                val_main = self.payload[self.current].val_main
                val_result = self.payload[self.current].val_result
                self.val_ord = self.payload[self.current].val_order_name
                print(("called : {}").format(val_name))
                #print(("____ : {}").format(val_result))

                obj = stage1[val_name]
                hostname=socket.gethostname()
                client_ip=socket.gethostbyname(hostname)
                x = threading.Thread(target=self.nokia_thread, args=(obj, val_main, patch_image, client_ip, val_result, ), daemon=True)
                x.start()

            #     def thred():
            #         # print("ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
            #         # if  ((val_name == 'MlStage1') or (val_name == 'Ml_PA') or (val_name == 'Washer_ML')):  
            #         # if  (val_name != 'Text_connectors') :
            #         try:
                        
            #             obj = stage1[val_name]
                        
            #             print("val___________nam",val_name)
                        
            #             hostname=socket.gethostname()
            #             client_ip=socket.gethostbyname(hostname)
            #             result = getattr(obj, val_main)(patch_image,client_ip)
            #             print("result______________________________",result)  # Ml label expected result result

            #             if result == val_result:
            #                 date = datetime.datetime.now()
            #                 self._nextStep("yes")
            #                 print("[INFO] result Yes!!")
            #                 #Dicts[val_name]='1  {} '.format(date)
            #                 #Dictz[sid]=Dicts

            #                 # print("yesssssssssssssssssssssssssssssssssssssssss ",Dicts)

            #             elif result == "no":
            #                 date = datetime.datetime.now()
            #                 self._nextStep("no")
            #                 print("[INFO] result Cross")
            #                 #Dicts[val_name]='0  {} '.format(date)
            #                 #Dictz[sid]=Dicts
            #                 #print("noooooooooooooooooooooooooooooooooooooooooo ",Dicts)
            #             else:
            #                 date = datetime.datetime.now()
            #                 self._nextStep("ignore")
            #                 print("[INFO] result No")
            #                 # Dicts[val_name]='0  {} '.format(date)
            #                 # Dictz[sid]=Dicts
            #                 # print("ignoreeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee ",Dicts)
                        
            #         except Exception as e:
            #             print("exception",e)
            #             pass

            #     x = threading.Thread(target=thred,args=() )
            #     x.daemon = True
            #     x.start()



            elif self.wait == True and self.lock == True:
                # #print("waiting")
                if self.i < 3:
                    self.i += 1
                elif self.i == 3:
                    self.lock = False
                    self.wait = False
                    self.i = 0
                    self.ui_obj.delete_multistep(self.current_id)
                    # alert("right")
                    if self.current_id > 100:
                        payload={"substep_id":self.current_id, "status":"done" , "token":token}
                        # restthread("substep",payload)
                    elif self.current_id < 100:
                        payload={"step_id":self.current_id,"status":"done","token":token}
                        # restthread("mainstep",payload)
                    else:
                        pass
                    self.current += 1
                    self.filter_obj.reset()
            
    #  -----------------------------------------------------------------------------------------------------
            # """LOCAL"""
            # if check and testLocal:
            #     #print "local validation"
            #     obj = stage1[self.payload[self.current].val_name]
            #     main = self.payload[self.current].val_main
            #     if getattr(obj, main)(patch_image) == self.payload[self.current].val_result:
            #         self._nextStep(operation="done")
            #     else:
            #         self._nextStep(operation="cross")
    # -----------------------------------------------------------------------------------------------------
            try:
                x0, y0 = tuple(self.payload[self.current].ctr_pos_3D)
                x_3d, y_3d = get_scn_points(x0, y0, H)
                for x, y in temp1:
                    x, y = get_scn_points(x, y, H, offset=0)
                    temp.append([x, y])
                self.py3d_obj.place_screw(self.payload[self.current].three_d, x_3d, y_3d, angle=demo_angle)
                
            except Exception as e:
                hardware_handler.CreateErrorLog(hardware_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            try:
                if (int(station_id),self.payload[self.current].id) in [(1,9),(3,30302),(3,2),(4,40202)]:
                    return self.draw_obj.on_scn_place_screws(img, H, temp, self.draw_obj._blink(self.color), station_id, self.payload[self.current].id)
                elif (int(station_id) == 1 or int(station_id)==3) and self.payload[self.current].val_name.startswith("Text_"):
                    return self.draw_obj.on_scn_arrow(img, self.payload[self.current].val_name, H, temp1, temp, self.draw_obj._blink(self.color))                
                elif (int(station_id),self.payload[self.current].id) in [(1,9),(3,4),(4,3)] or \
                    self.payload[self.current].id in range(11001,11025) or \
                    self.payload[self.current].id in range(30401,30420) or \
                    self.payload[self.current].id in range(40301,40322):
                    return self.draw_obj.on_scn_template(img, H, self.payload[self.current].id, station_id, self.draw_obj._blink(self.color))
                else:
                    return self.draw_obj.on_scn(img, H, temp, self.draw_obj._blink(self.color))
            except Exception as e:
                hardware_handler.CreateErrorLog(hardware_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                return img

        except Exception as e:
            hardware_handler.CreateErrorLog(hardware_handler.LogObject, str(type(e))+" "+traceback.format_exc().splitlines()[1])
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return img
import sys
import os        
