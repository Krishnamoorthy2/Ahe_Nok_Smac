import threading
import time
import tkinter as tk
from PIL import Image, ImageTk
import os

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

class startsync:
	splash = True

	@classmethod
	def update(cls, value):
		cls.splash = value

	def __init__(self, value):
		self.value = value
		self.update(value)

def splash():
	window = tk.Tk()
	window.title("NOKIA")
	window.overrideredirect(1)
	w = 800
	h = 650
	ws = window.winfo_screenwidth()
	hs = window.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)

	# window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	# path = ui_path+"second_page.png"
	# img = ImageTk.PhotoImage(Image.open(path))
	# panel = tk.Label(window, image = img)
	# panel.pack(side = "bottom", fill = "both", expand = "yes")
	# #print (startsync.splash)
	# window.after(3000, lambda: window.destroy())
	# window.mainloop()


def sync():
	a = threading.Thread(target=splash)
	a.daemon=True
	a.start()

class close:
	startflag = True

	@classmethod
	def update(cls, value):
		cls.startflag = value

	def __init__(self, value):
		self.value = value
		self.update(value)


class nclose:
	status = True

	@classmethod
	def update(cls, value):
		cls.status = value

	def __init__(self, value):
		self.value = value
		self.update(value)