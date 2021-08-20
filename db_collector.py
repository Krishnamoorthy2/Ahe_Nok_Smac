import tkinter
import tkinter.font
import PIL.Image, PIL.ImageTk
from db_validation import cv2, time, db_check
from entry import close,nclose
 
class App:
    def __init__(self, window, window_title, sid, video_source=0):
        f = open("op.txt","w+")
        f.close()
        self.window = window
        self.window.geometry("+0+0")
        self.window.title(window_title)
        self.window.iconbitmap('data\\ui\\icon-title.ico')
        self.window.resizable(width=False, height=False)
        def on_closing():
            close(False)
            nclose(None)
            self.window.destroy()
        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.video_source = video_source

 
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
    
        # Button that lets the user take a snapshot
        self.btn_snapshot=tkinter.Button(window, font="Helvetica 10 bold", text="SNAPSHOT", width=50, height=5, command=self.snapshot)
        self.btn_snapshot.place(x=1325, y=850)
        # self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
 
        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15

        # My onscreen placements
        self.count = 1
        self.db_ref = cv2.imread("db_ref"+str(sid)+".jpg")
        self.db_ref1 = self.db_ref.copy()
        self.db_ref = cv2.resize(self.db_ref, (278,477))
        # self.db_ref = cv2.cvtColor(self.db_ref, cv2.COLOR_RGB2RGBA)
        self.correct = cv2.imread("correct.png", -1)
        self.correct = cv2.resize(self.correct, (128,128))
        self.wrong = cv2.imread("wrong.png", -1)
        self.wrong = cv2.resize(self.wrong, (128,128))
        # self.correct = cv2.cvtColor(self.correct, cv2.COLOR_RGB2RGBA)
        self.flag = None
        # self.correct = cv2.cvtColor(self.correct, cv2.COLOR_RGB2RGBA)
        self.top = cv2.imread('top_cover.jpg')
        # self.top = cv2.cvtColor(self.top, cv2.COLOR_RGB2RGBA)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.color = (255, 255, 255)
        self.msg = "PLACE THE\nCHASSIS\nWITHIN THE\nHIGHLIGHTED AREA\nAND CLICK\nSNAPSHOT BUTTON"

        self.update()
 
        self.window.mainloop()
 
    def apply_correct(self, frame, img, x,y):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
        h, w, _ = img.shape
        alpha_s = img[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s
        for c in range(0, 3):
            frame[x:x+h, y:y+w, c] = (alpha_s * img[:, :, c] + alpha_l * frame[x:x+h, y:y+w, c])
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        return frame

    def apply_img(self, frame, img, x,y):
        h, w, _ = img.shape
        # alpha_s = img[:, :, 3] / 255.0
        # alpha_l = 1.0 - alpha_s
        # for c in range(0, 3):
        #     frame[x:x+h, y:y+w, c] = (alpha_s * img[:, :, c] + alpha_l * frame[x:x+h, y:y+w, c])
        frame[x:x+h, y:y+w] = img[:, :]
        return frame

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
 
        if ret:
            focus = frame[169:919, 646:1097]
            focus = cv2.resize(focus, (455,789))
            result = db_check(focus)
            if result:
                # cv2.imwrite("data\\db_"+str(station_id)+"\\"+str(time.time())+".jpg", focus)
                focus = self.apply_img(focus, self.top, 0, 3)                      
                cv2.imwrite("data\\db_2\\temp.jpg", focus)
                self.msg = "CHASSIS\nCAPTURED"
                self.flag = True
            else:
                self.flag = False
                self.msg = "PLACE\nAHEGA CHASSIS\nPROPERLY"
            # cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
 
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
 
        if ret:
            focus = frame[169:919, 646:1097]
            focus = cv2.resize(focus, (455,789))
            # focus = cv2.cvtColor(focus, cv2.COLOR_RGB2RGBA)
            # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)        
            # frame[:,:,:,] = [223, 148, 105,1]            
            frame[:,:,:] = [145, 65, 18]
            frame = self.apply_img(frame, focus, 169,646)
            frame = self.apply_img(frame, self.db_ref, 90,90)
            if self.flag:
                frame = self.apply_correct(frame, self.correct, 50,1700)
            elif self.flag == False:
                frame = self.apply_correct(frame, self.wrong, 50,1700)

            frame = cv2.putText(frame, "REFERENCE PLACEMENT", (45,60), self.font, 1, self.color, 3, cv2.LINE_AA)
            y0, dy = 300, 75
            for i, line in enumerate(self.msg.split('\n')):
                y = y0 + i*dy
                frame = cv2.putText(frame, line, (1300,y), self.font, 2, self.color, 3, cv2.LINE_AA)
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.screen_width,self.screen_height))
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        
        self.window.after(self.delay, self.update)
        if self.flag:
            self.count += 1
            if self.count > 5:
                self.vid.__del__()
                self.window.destroy()
 
class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(0)
        self.vid.set(3, 1920)
        self.vid.set(4, 1080)

        # self.vid = cv2.VideoCapture(2)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source) 

        # Get video source width and height
        self.width = 1920
        self.height = 1080
 
    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (False, None)
 
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

#App(tkinter.Tk(), "NOKIA")