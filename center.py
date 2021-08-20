import tkinter.messagebox
from PIL import Image, ImageTk
import sys
import smtplib
import tkinter
import json
import os
import requests
import numpy as np
import cv2
from generate_log import LogGen, traceback
from db_collector import App
from entry import close,nclose
#from initial import nclose

if os.name == "nt":  # windows
    mid = "\\"
    front = str(os.getcwd())
    front = front.split('\\')
    s = '\\'
    front = s.join(front) + "\\"
elif os.name == "posix":  # linux
    mid = "/"
    front = ""

ui_path = "data" + mid + "ui" + mid

hardware_handler = LogGen("Hardware_log", "w")
network_handler = LogGen("Network_log", "w")
ui_handler = LogGen("UI_log", "w")

# class close:
#     startflag = True

#     @classmethod
#     def update(cls, value):
#         cls.startflag = value

#     def __init__(self, value):
#         self.value = value
#         self.update(value)


def displaypage(page):
    window = tkinter.Tk()
    # screen_width = window.winfo_screenwidth()
    # screen_height = window.winfo_screenheight()
    # screen_res = str(screen_width)+" "+str(screen_height)
    window.title("NOKIA")
    window.overrideredirect(1)
    w = 800
    h = 650
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    if(page==1):
        path = ui_path+"first_page.png"
    else:
        path = ui_path+"second_page.png"
    img = ImageTk.PhotoImage(Image.open(path))
    panel = tkinter.Label(window, image = img)
    panel.pack(side = "bottom", fill = "both", expand = "yes")
    window.after(2000, lambda: window.destroy())
    window.mainloop()




def root1(master):
    def test1(master):
        sip = sip_Entry.get()
        try:
            with open("smacar.json", "r") as jsonFile:
                data = json.load(jsonFile)
        except:
            network_handler.CreateErrorLog(network_handler.LogObject, " <type 'smacar.json Not Available'>   File \"center.py\", line 117, in <module>")
        response = os.system("ping " + sip)
        if (response == 0):
            data['server_ip']=sip
            with open("smacar.json", "w") as jsonFile:
                json.dump(data, jsonFile)
            master.destroy()
            start(2)
        else:
            tkinter.messagebox.showerror("Error","Please enter proper server IP")
            root1(master)
            #master.destroy()  
        
        
    master.destroy()
    root = tkinter.Tk()
    def on_closing():
        #close(False)
        root.destroy()
        start(2)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    try:
        with open("smacar.json", "r") as jsonFile:
            data = json.load(jsonFile)
    except:
        network_handler.CreateErrorLog(network_handler.LogObject, " <type 'smacar.json Not Available'>   File \"center.py\", line 117, in <module>")
    serverip=data['server_ip']
    root.title("NOKIA | Setting")
    root.iconbitmap(ui_path+'icon-title.ico')
    root.resizable(width=False, height=False)
    w = 800
    h = 650
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    img1 = ImageTk.PhotoImage(Image.open(ui_path+"setting.png"))
    panel1 = tkinter.Label(root, image = img1)
    panel1.pack(side = "bottom", fill = "both", expand = "yes")
    sip_Variable = tkinter.StringVar()
    sip_Entry = tkinter.Entry(root, bd=4, width=28, textvariable=sip_Variable, font="Helvetica 16 italic")
    sip_Entry.insert(tkinter.END,serverip)
    sip_Entry.focus()
    sip_Entry.place(x=250, y=300)
    set_Button = tkinter.Button(root, text="Set", font="Bizon 13 bold",bd=0,borderwidth=0,highlightthickness = 0,bg = "#26E880",width=8,height=2,command=lambda:test1(root))
    #set_Button = tkinter.Button(root, text="Set", font="Bizon 13 bold",bd=0,borderwidth=0,highlightthickness = 0,bg = "#26E880",width=8,height=2,command=lambda:start())
    set_Button.place(x=395, y=364)
    root.mainloop()


def start(screen=1):
    def test(master):
        eid = eid_Entry.get()
        sid = sid_Entry.get()
        # sid = 1
        sid1 = "station"+sid
        if len(sid) == 0 and len(eid) == 0:
            tkinter.messagebox.showinfo("ERROR", "INVALID DATA")
            master.destroy()
            start(2)
        else:
            if len(sid) == 1:
                try:
                    if 1 <= (int(sid)) <= 4:
                        data['station_id']=sid
                        with open("smacar.json", "w") as jsonFile:
                            json.dump(data, jsonFile)
                        master.destroy()
                        # if(int(sid)==1):
                        #     App(tkinter.Tk(), "NOKIA", int(sid))
                        # else:
                        #     pass
                    else:
                        tkinter.messagebox.showinfo("ERROR", "INVALID STATION ID")
                        master.destroy()
                        start(2)
                except:
                    tkinter.messagebox.showinfo("ERROR", "INVALID STATION ID")
                    master.destroy()
                    start(2)
            else:
                tkinter.messagebox.showinfo("ERROR", "INVALID STATION ID")
                master.destroy()
                start(2) 
    if(screen==1):
        displaypage(1)
    else:
        close(True)
        pass
    try:
        with open("smacar.json", "r") as jsonFile:
            data = json.load(jsonFile)
    except:
        network_handler.CreateErrorLog(network_handler.LogObject, " <type 'smacar.json Not Available'>   File \"center.py\", line 117, in <module>")
    hostname = data['server_ip'] 
    # response = os.system("ping " + hostname)
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if cap.isOpened():
        master = tkinter.Tk()    
        def on_closing():
            close(False)
            master.destroy()
            nclose(None)
        master.protocol("WM_DELETE_WINDOW", on_closing)
        master.title("NOKIA | LOGIN")
        master.iconbitmap(ui_path+'icon-title.ico')
        master.resizable(width=False, height=False)
        w = 800
        h = 650
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        img = ImageTk.PhotoImage(Image.open(ui_path+"login.png"))
        panel = tkinter.Label(master, image = img)
        panel.pack(side = "bottom", fill = "both", expand = "yes")
        try:
            with open("smacar.json", "r") as jsonFile:
                data = json.load(jsonFile)
                emp_id=data['emp_id']
                s_id=data['station_id']
        except:
            network_handler.CreateErrorLog(network_handler.LogObject, " <type 'smacar.json Not Available'>   File \"center.py\", line 117, in <module>")
        eid_Variable = tkinter.StringVar()
        eid_Entry = tkinter.Entry(master, width=15, textvariable=eid_Variable, font="Helvetica 16 italic")
        eid_Entry.insert(tkinter.END, emp_id)
        eid_Entry.focus()
        eid_Entry.place(x=300, y=240)
        sid_Variable = tkinter.StringVar()
        sid_Entry = tkinter.Entry(master,width=15, textvariable=sid_Variable, font="Helvetica 16 italic")
        sid_Entry.insert(tkinter.END,s_id)
        sid_Entry.focus()
        sid_Entry.place(x=300, y=330)
        signIn_Button = tkinter.Button(master, text="Sign In", font="Bizon 13 bold",bd=0,borderwidth=0,highlightthickness = 0, bg = "#26E880",width=9,height=2,command=lambda:test(master))
        signIn_Button.place(x=295, y=413)
        setting_Button = tkinter.Button(master, text="Setting", font="Bizon 13 bold",bd=0,borderwidth=0,highlightthickness = 0,bg = "#FFC813",width=9,height=2,command=lambda:root1(master))
        setting_Button.place(x=448, y=413)
        master.mainloop()
    else:
        master = tkinter.Tk()
        hardware_handler.CreateErrorLog(hardware_handler.LogObject, " <type 'Camera not found'>   File \"center.py\", line 157, in <module>")
        tkinter.messagebox.showerror("Error","Please connect camera or network")
        nclose(False)
        master.destroy()

