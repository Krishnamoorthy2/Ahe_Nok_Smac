import os
from PIL import Image, ImageTk
import tkinter
import subprocess
import tkinter.messagebox
from entry import nclose,close
from center import start
import socket
import json
# from nokia import Dicts,Dictz
# from network.text_handler import station_id
from db_collector import App
import paho.mqtt.publish as publish
start()

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


def pub_exit():
    with open("smacar.json", "r") as read_file:
        config_data = json.load(read_file)
        server_ip = config_data["server_ip"]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    channel_id = s.getsockname()[0].split(".")[-1]
    publish.single(channel_id, "exit", hostname=server_ip, qos=2,auth={"username":"smacar","password":"Welc0me3#"})


def loop():
    def test(root,action):
        if(action==1):
            nclose(False)
            root.destroy()
        else:
            nclose(True)
            close(False)
            root.destroy()
            start(2)
    root = tkinter.Tk()
    def on_closing():
        nclose(False)
        root.destroy()
        #start(2)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.iconbitmap(ui_path+'icon-title.ico')
    root.title("NOKIA | ALERT")
    root.resizable(width=False, height=False)
    w = 600
    h = 250
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    img1 = ImageTk.PhotoImage(Image.open(ui_path+"close.png"))
    panel1 = tkinter.Label(root, image = img1)
    panel1.pack(side = "bottom", fill = "both", expand = "yes")
    signIn_Button = tkinter.Button(root, text="Yes", font="Bizon 13 bold",bd=0,borderwidth=0,highlightthickness = 0, bg = "#E83925",width=11,height=2,command=lambda:test(root,1))
    signIn_Button.config(fg='white')
    signIn_Button.place(x=170, y=150)
    setting_Button = tkinter.Button(root, text="No", font="Bizon 13 bold",bd=0,borderwidth=0,highlightthickness = 0,bg = "#35BF2B",width=11,height=2,command=lambda:test(root,2))
    setting_Button.config(fg='white')
    setting_Button.place(x=315, y=150)
    root.mainloop()


def start_initial():
    while True:
        if(nclose.status==True and close.startflag==True):
            print(subprocess.call(['python3','ar_plugin.py']))
            
            nclose(None)
        elif(nclose.status==None):
            loop()
            if(close.startflag==None):
                close(True)
            else:
                pass
        else:
            break


