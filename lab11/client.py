import socket
import pickle
from tkinter import *

HOST = "127.0.0.1"
PORT = 65432

canvas_width = 400
canvas_height = 500

def paint(event):
    colour = "#000000"
    x1, y1 = (event.x - 2), (event.y - 2)
    x2, y2 = (event.x + 2), (event.y + 2)
    picture = w.create_rectangle(x1, y1, x2, y2, fill=colour)
    coordinata = w.coords(picture)
    data = pickle.dumps(coordinata)
    s.send(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    master = Tk()
    master.title("Client")
    w = Canvas(master,
               width=canvas_width,
               height=canvas_height)
    w.pack(expand=YES, fill=BOTH)
    w.bind("<B1-Motion>", paint)
    message = Label(master, text="Press and Drag the mouse to draw")
    message.pack(side=BOTTOM)
    mainloop()
